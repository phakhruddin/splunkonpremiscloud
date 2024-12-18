import boto3
from botocore.exceptions import ClientError
import logging
import time
import paramiko
import os
import subprocess


class EC2NodeManager:
    """
    A utility class for managing EC2 instances for Splunk deployment.
    Handles provisioning, SSM agent checks, tagging, and EC2 node configuration.
    """

    def __init__(self, region_name="us-east-1"):
        """
        Initialize the EC2NodeManager class.

        Args:
            region_name (str): AWS region to use for EC2 operations.
        """
        self.ec2_client = boto3.client("ec2", region_name=region_name)
        self.ssm_client = boto3.client("ssm", region_name=region_name)
        self.region = region_name

    def create_instance(self, instance_type, ami_id, key_name,
                        security_group_ids, subnet_id, instance_name, tags=None):
        """
        Provision a new EC2 instance for Splunk deployment.

        Args:
            instance_type (str): Instance type for the EC2 instance.
            ami_id (str): AMI ID for the EC2 instance.
            key_name (str): Key pair name for SSH access.
            security_group_ids (list): List of security group IDs for the EC2 instance.
            subnet_id (str): Subnet ID where the instance will be launched.
            instance_name (str): Name for the EC2 instance.
            tags (dict): Tags to apply to the EC2 instance (default is None).

        Returns:
            str: Instance ID of the created EC2 instance.
        """
        try:
            # Launch the instance
            response = self.ec2_client.run_instances(
                InstanceType=instance_type,
                ImageId=ami_id,
                KeyName=key_name,
                SecurityGroupIds=security_group_ids,
                SubnetId=subnet_id,
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": "Name", "Value": instance_name}] + tags if tags else [{"Key": "Name", "Value": instance_name}]
                    }
                ]
            )
            instance_id = response["Instances"][0]["InstanceId"]
            print(f"Provisioned EC2 instance with ID: {instance_id}")
            return instance_id
        except ClientError as e:
            print(f"Error provisioning EC2 instance: {e}")
            return None

    def check_ssm_agent(self, instance_id):
        """
        Check if SSM agent is installed and running on the EC2 instance.
        If not, install and start it.

        Args:
            instance_id (str): EC2 instance ID to check.

        Returns:
            bool: True if the SSM agent is running, False otherwise.
        """
        try:
            # Use SSM to run the check
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": ["ps -ef | grep amazon-ssm-agent"]},
            )
            command_id = response["Command"]["CommandId"]

            # Wait for the command to complete and check if SSM agent is
            # running
            time.sleep(5)
            result = self.ssm_client.get_command_invocation(
                CommandId=command_id, InstanceId=instance_id
            )
            if "amazon-ssm-agent" in result["StandardOutputContent"]:
                print(
                    f"SSM agent is already running on instance {instance_id}.")
                return True
            else:
                print(
                    f"SSM agent not found on instance {instance_id}, installing...")
                # Install the SSM agent if it's not found
                self.install_ssm_agent(instance_id)
                return False
        except ClientError as e:
            print(f"Error checking SSM agent status: {e}")
            return False

    def install_ssm_agent(self, instance_id):
        """
        Install the SSM agent on the EC2 instance.

        Args:
            instance_id (str): EC2 instance ID to install the SSM agent.
        """
        try:
            # Run the command to install SSM agent
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": [
                        "curl https://amazon-ssm-{0}.s3.amazonaws.com/latest/linux_amd64/amazon-ssm-agent.rpm -o /tmp/amazon-ssm-agent.rpm".format(
                            self.region),
                        "sudo rpm -i /tmp/amazon-ssm-agent.rpm",
                        "sudo systemctl start amazon-ssm-agent"
                    ]
                }
            )
            print(f"SSM agent installation started on instance {instance_id}.")
        except ClientError as e:
            print(f"Error installing SSM agent on instance {instance_id}: {e}")

    def tag_instance(self, instance_id, tags):
        """
        Tag an EC2 instance with the provided tags.

        Args:
            instance_id (str): EC2 instance ID to tag.
            tags (dict): Dictionary of tags to apply to the instance.

        Returns:
            bool: True if tags were successfully applied, False otherwise.
        """
        try:
            self.ec2_client.create_tags(
                Resources=[instance_id],
                Tags=[{"Key": key, "Value": value}
                      for key, value in tags.items()]
            )
            print(f"Successfully applied tags to instance {instance_id}.")
            return True
        except ClientError as e:
            print(f"Error tagging instance {instance_id}: {e}")
            return False

    def configure_splunk(self, instance_id, splunk_conf):
        """
        Configure Splunk on the EC2 instance by sending commands via SSM.

        Args:
            instance_id (str): EC2 instance ID to configure.
            splunk_conf (dict): Dictionary containing Splunk configuration details.

        Returns:
            bool: True if Splunk was configured successfully, False otherwise.
        """
        try:
            # Build the configuration commands based on the splunk_conf
            # parameter
            commands = []
            if "license" in splunk_conf:
                commands.append(
                    f"echo '{splunk_conf['license']}' > /opt/splunk/etc/system/local/license.conf")
            if "index" in splunk_conf:
                commands.append(
                    f"echo '{splunk_conf['index']}' > /opt/splunk/etc/system/local/indexes.conf")
            if "forwarder" in splunk_conf:
                commands.append(
                    f"echo '{splunk_conf['forwarder']}' > /opt/splunk/etc/system/local/inputs.conf")

            # Send the commands to the EC2 instance to configure Splunk
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": commands}
            )
            print(f"Splunk configuration started on instance {instance_id}.")
            return True
        except ClientError as e:
            print(f"Error configuring Splunk on instance {instance_id}: {e}")
            return False


if __name__ == "__main__":
    # Example usage of the EC2NodeManager
    ec2_manager = EC2NodeManager(region_name="us-east-1")

    # Example instance provisioning
    instance_id = ec2_manager.create_instance(
        instance_type="t2.medium",
        ami_id="ami-12345678",  # Replace with a valid AMI ID
        key_name="my-key",
        security_group_ids=["sg-12345678"],
        # Replace with your security group ID
        subnet_id="subnet-12345678",  # Replace with your subnet ID
        instance_name="splunk-instance",
        tags={"app": "splunk", "environment": "production"}
    )

    if instance_id:
        # Check and install SSM agent if necessary
        ec2_manager.check_ssm_agent(instance_id)

        # Example Splunk configuration
        splunk_conf = {
            "license": "your-license-key",
            "index": "[indexer]\nindex = main\n",
            "forwarder": "[input]\nforwarder = true\n"
        }
        ec2_manager.configure_splunk(instance_id, splunk_conf)
