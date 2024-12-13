import boto3
from botocore.exceptions import ClientError
import paramiko


class EC2Helper:
    """
    A utility class for managing AWS EC2 instances for Splunk deployments.
    """

    def __init__(self, region_name="us-east-1"):
        """
        Initialize the EC2Helper class.

        Args:
            region_name (str): The AWS region to use.
        """
        self.ec2_client = boto3.client("ec2", region_name=region_name)
        self.ssm_client = boto3.client("ssm", region_name=region_name)

    def check_and_resolve_ssm(self, instance_id, key_path, username="ec2-user"):
        """
        Check if the SSM agent is running on an EC2 instance and resolve it
        by installing and starting the agent if missing.

        Args:
            instance_id (str): The ID of the EC2 instance.
            key_path (str): Path to the private key file for SSH access.
            username (str): SSH username for the instance. Default is 'ec2-user'.

        Returns:
            bool: True if SSM agent is running or successfully resolved, False otherwise.
        """
        try:
            # Get the public IP of the instance
            instance = self.ec2_client.describe_instances(InstanceIds=[instance_id])["Reservations"][0]["Instances"][0]
            public_ip = instance.get("PublicIpAddress")
            if not public_ip:
                print(f"Instance {instance_id} does not have a public IP.")
                return False

            # Check SSM agent status via SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(public_ip, username=username, key_filename=key_path)

            stdin, stdout, stderr = ssh.exec_command("systemctl is-active amazon-ssm-agent")
            status = stdout.read().decode().strip()
            if status == "active":
                print(f"SSM agent is running on instance {instance_id}.")
                ssh.close()
                return True

            print(f"SSM agent is not running on instance {instance_id}. Attempting to resolve...")

            # Install and start the SSM agent
            ssh.exec_command("sudo yum install -y amazon-ssm-agent")
            ssh.exec_command("sudo systemctl enable amazon-ssm-agent")
            ssh.exec_command("sudo systemctl start amazon-ssm-agent")

            stdin, stdout, stderr = ssh.exec_command("systemctl is-active amazon-ssm-agent")
            status = stdout.read().decode().strip()
            ssh.close()

            if status == "active":
                print(f"SSM agent successfully installed and started on instance {instance_id}.")
                return True
            else:
                print(f"Failed to start SSM agent on instance {instance_id}.")
                return False

        except ClientError as e:
            print(f"Error resolving SSM agent on instance {instance_id}: {e}")
            return False
        except paramiko.SSHException as ssh_error:
            print(f"SSH error on instance {instance_id}: {ssh_error}")
            return False
