import boto3
from botocore.exceptions import ClientError


class EC2Manager:
    """
    A utility class for managing AWS EC2 instances for Splunk deployments.
    """

    def __init__(self, region_name="us-east-1"):
        """
        Initialize the EC2Manager class.

        Args:
            region_name (str): AWS region to use for EC2 operations.
        """
        self.ec2_client = boto3.client("ec2", region_name=region_name)

    def create_instance(self, ami_id, instance_type, key_name, security_group_ids, subnet_id, tags):
        """
        Create an EC2 instance with specified configurations.

        Args:
            ami_id (str): Amazon Machine Image (AMI) ID.
            instance_type (str): EC2 instance type (e.g., t2.micro).
            key_name (str): Key pair name for SSH access.
            security_group_ids (list): List of security group IDs.
            subnet_id (str): Subnet ID for the instance.
            tags (list): List of tags to attach to the instance.

        Returns:
            dict: Details of the created instance.
        """
        try:
            response = self.ec2_client.run_instances(
                ImageId=ami_id,
                InstanceType=instance_type,
                KeyName=key_name,
                SecurityGroupIds=security_group_ids,
                SubnetId=subnet_id,
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": tags
                    }
                ]
            )
            instance = response["Instances"][0]
            print(f"EC2 instance created: {instance['InstanceId']}")
            return instance
        except ClientError as e:
            print(f"Error creating instance: {e}")
            return None

    def list_instances(self, filters=None):
        """
        List EC2 instances based on filters.

        Args:
            filters (list): List of filters for querying instances.

        Returns:
            list: List of instance details.
        """
        try:
            response = self.ec2_client.describe_instances(Filters=filters)
            instances = [
                instance
                for reservation in response["Reservations"]
                for instance in reservation["Instances"]
            ]
            print(f"Found {len(instances)} instances.")
            return instances
        except ClientError as e:
            print(f"Error listing instances: {e}")
            return []

    def start_instance(self, instance_id):
        """
        Start a stopped EC2 instance.

        Args:
            instance_id (str): ID of the instance to start.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} started.")
            return True
        except ClientError as e:
            print(f"Error starting instance {instance_id}: {e}")
            return False

    def stop_instance(self, instance_id):
        """
        Stop a running EC2 instance.

        Args:
            instance_id (str): ID of the instance to stop.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} stopped.")
            return True
        except ClientError as e:
            print(f"Error stopping instance {instance_id}: {e}")
            return False

    def terminate_instance(self, instance_id):
        """
        Terminate an EC2 instance.

        Args:
            instance_id (str): ID of the instance to terminate.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} terminated.")
            return True
        except ClientError as e:
            print(f"Error terminating instance {instance_id}: {e}")
            return False

    def check_tags(self, instance_id, required_tags):
        """
        Check if the specified EC2 instance has required tags.

        Args:
            instance_id (str): ID of the EC2 instance to check.
            required_tags (dict): Dictionary of required tags (key-value pairs).

        Returns:
            bool: True if all required tags are present, False otherwise.
        """
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response["Reservations"][0]["Instances"][0]
            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}

            for key, value in required_tags.items():
                if tags.get(key) != value:
                    print(f"Instance {instance_id} is missing required tag: {key}={value}")
                    return False

            print(f"Instance {instance_id} has all required tags.")
            return True
        except ClientError as e:
            print(f"Error checking tags for instance {instance_id}: {e}")
            return False

    def associate_iam_role(self, instance_id, iam_role_arn):
        """
        Associate an IAM role with an EC2 instance.

        Args:
            instance_id (str): ID of the EC2 instance.
            iam_role_arn (str): ARN of the IAM role to associate.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.ec2_client.associate_iam_instance_profile(
                InstanceId=instance_id,
                IamInstanceProfile={
                    "Arn": iam_role_arn
                }
            )
            print(f"Associated IAM role {iam_role_arn} with instance {instance_id}.")
            return True
        except ClientError as e:
            print(f"Error associating IAM role with instance {instance_id}: {e}")
            return False
