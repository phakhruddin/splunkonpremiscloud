import boto3
from botocore.exceptions import ClientError
import logging


class SplunkDeployer:
    """
    A class to deploy and manage Splunk in AWS environment.
    Handles EC2 provisioning, Splunk installation, configuration,
    and health check for Splunk forwarders, search heads, indexers, and other components.
    """

    def __init__(self, region_name="us-east-1"):
        """
        Initialize the SplunkDeployer class.

        Args:
            region_name (str): AWS region to use for EC2 operations.
        """
        self.ec2_client = boto3.client("ec2", region_name=region_name)
        self.ssm_client = boto3.client("ssm", region_name=region_name)
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.region = region_name
        self.logger = logging.getLogger("SplunkDeployer")
        logging.basicConfig(level=logging.INFO)

    def create_instance(self, instance_type, ami_id, key_name, security_group_ids,
                        subnet_id, instance_name, tags=None):
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
                        "Tags": [{"Key": "Name", "Value": instance_name}] + (tags if tags else [])
                    }
                ]
            )
            instance_id = response["Instances"][0]["InstanceId"]
            self.logger.info(
                f"Provisioned EC2 instance with ID: {instance_id}")
            return instance_id
        except ClientError as e:
            self.logger.error(f"Error provisioning EC2 instance: {e}")
            return None

    def check_ssm_agent(self, instance_id):
        """
        Check if the SSM agent is running on the EC2 instance.
        If not, it installs and starts it.

        Args:
            instance_id (str): EC2 instance ID to check.

        Returns:
            bool: True if the SSM agent is running, False otherwise.
        """
        try:
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": ["systemctl status amazon-ssm-agent"]
                }
            )
            status = response["Command"]["Status"]
            if status == "Success":
                self.logger.info(
                    f"SSM agent is running on instance {instance_id}")
                return True
            else:
                self.logger.warning(
                    f"SSM agent not running on instance {instance_id}. Installing...")
                install_command = "yum install -y amazon-ssm-agent && systemctl start amazon-ssm-agent"
                self.ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={"commands": [install_command]}
                )
                return False
        except ClientError as e:
            self.logger.error(f"Error checking SSM agent: {e}")
            return False

    def deploy_splunk(self, instance_id, splunk_package_url):
        """
        Deploy the Splunk package onto the EC2 instance.

        Args:
            instance_id (str): The EC2 instance ID to deploy Splunk on.
            splunk_package_url (str): URL to the Splunk package to download.

        Returns:
            bool: True if Splunk is successfully installed, False otherwise.
        """
        try:
            install_command = f"wget {splunk_package_url} -O /tmp/splunk.tar.gz && " \
                              f"tar -zxvf /tmp/splunk.tar.gz -C /opt/splunk"
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": [install_command]}
            )
            self.logger.info(f"Response is {response}.")
            self.logger.info(f"Deploying Splunk on instance {instance_id}.")
            return True
        except ClientError as e:
            self.logger.error(f"Error deploying Splunk: {e}")
            return False

    def configure_splunk(self, instance_id, splunk_conf):
        """
        Configure Splunk on the EC2 instance using configuration files.

        Args:
            instance_id (str): EC2 instance ID to configure.
            splunk_conf (dict): Dictionary containing Splunk configurations.

        Returns:
            bool: True if the configuration was applied successfully, False otherwise.
        """
        try:
            config_commands = [
                f"echo '{splunk_conf['forwarder']}' > /opt/splunk/etc/system/local/inputs.conf",
                f"echo '{splunk_conf['search_head']}' > /opt/splunk/etc/system/local/outputs.conf"
            ]
            for command in config_commands:
                response = self.ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={"commands": [command]}
                )
                self.logger.info(
                    f"With response {response} Applied configuration on instance {instance_id}.")
            return True
        except ClientError as e:
            self.logger.error(f"Error configuring Splunk: {e}")
            return False

    def health_check(self, instance_id):
        """
        Perform a health check on the deployed Splunk instance.

        Args:
            instance_id (str): EC2 instance ID to perform health check.

        Returns:
            bool: True if health check passes, False otherwise.
        """
        try:
            response = self.ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": ["/opt/splunk/bin/splunk status"]}
            )
            status = response["Command"]["Status"]
            if status == "Success":
                self.logger.info(f"Splunk instance {instance_id} is healthy.")
                return True
            else:
                self.logger.warning(
                    f"Health check failed for Splunk instance {instance_id}.")
                return False
        except ClientError as e:
            self.logger.error(f"Error performing health check: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    deployer = SplunkDeployer()
    instance_id = deployer.create_instance(
        instance_type="t2.medium",
        ami_id="ami-0abcdef1234567890",
        key_name="my-key-pair",
        security_group_ids=["sg-12345678"],
        subnet_id="subnet-abcde123",
        instance_name="Splunk-Instance",
        tags=[{"Key": "App", "Value": "Splunk"}]
    )

    if instance_id:
        deployer.check_ssm_agent(instance_id)
        deployer.deploy_splunk(
            instance_id,
            "https://download.splunk.com/path/to/splunk.tar.gz")
        splunk_conf = {
            "forwarder": "splunk_forwarder_config_content",
            "search_head": "splunk_search_head_config_content"
        }
        deployer.configure_splunk(instance_id, splunk_conf)
        deployer.health_check(instance_id)
