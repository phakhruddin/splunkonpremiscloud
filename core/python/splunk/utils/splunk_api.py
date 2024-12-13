import boto3
import requests


class SplunkManager:
    """
    A class to manage interactions with a Splunk instance via the REST API.

    Attributes:
        base_url (str): The base URL of the Splunk instance.
        auth (tuple): A tuple containing the username and password for authentication.
    """

    def __init__(self, base_url: str, secret_name: str,
                 aws_region: str = "us-east-1"):
        """
        Initializes the SplunkManager with the base URL and authentication details.

        Args:
            base_url (str): The base URL of the Splunk instance.
            secret_name (str): The AWS Secrets Manager secret name containing Splunk credentials.
            aws_region (str): AWS region where the Secrets Manager is located. Defaults to "us-east-1".
        """
        self.base_url = base_url.rstrip("/")
        self.auth = self._get_credentials_from_secrets_manager(
            secret_name, aws_region)

    def _get_credentials_from_secrets_manager(
            self, secret_name: str, aws_region: str) -> tuple:
        """
        Retrieves Splunk credentials from AWS Secrets Manager.

        Args:
            secret_name (str): The name of the secret in AWS Secrets Manager.
            aws_region (str): AWS region where the Secrets Manager is located.

        Returns:
            tuple: A tuple containing the Splunk username and password.
        """
        client = boto3.client("secretsmanager", region_name=aws_region)
        secret_value = client.get_secret_value(SecretId=secret_name)

        # Parse the secret string (assumes the secret is stored in JSON format)
        secret = secret_value["SecretString"]
        secret_dict = eval(secret)  # Convert JSON string to dictionary

        username = secret_dict.get("username")
        password = secret_dict.get("password")

        if not username or not password:
            raise ValueError(
                "Secrets Manager response does not contain 'username' or 'password'.")

        return username, password

    # --- Index Management Methods ---

    def create_index(self, index_name: str, max_size_mb: int = None,
                     home_path: str = None) -> dict:
        """
        Creates a new Splunk index.

        Args:
            index_name (str): Name of the new index.
            max_size_mb (int, optional): Maximum size of the index in MB. Defaults to None.
            home_path (str, optional): Custom home path for the index. Defaults to None.

        Returns:
            dict: Response from the Splunk API.
        """
        index_url = f"{self.base_url}/services/data/indexes"
        payload = {"name": index_name}
        if max_size_mb:
            payload["maxTotalDataSizeMB"] = max_size_mb
        if home_path:
            payload["homePath"] = home_path

        response = requests.post(
            index_url,
            data=payload,
            auth=self.auth,
            verify=False)
        response.raise_for_status()
        return response.json()

    def delete_index(self, index_name: str) -> dict:
        """
        Deletes an existing Splunk index.

        Args:
            index_name (str): Name of the index to delete.

        Returns:
            dict: Response from the Splunk API.
        """
        index_url = f"{self.base_url}/services/data/indexes/{index_name}"
        response = requests.delete(index_url, auth=self.auth, verify=False)
        response.raise_for_status()
        return response.json()

    def list_indexes(self) -> list:
        """
        Lists all Splunk indexes.

        Returns:
            list: A list of indexes and their properties.
        """
        index_url = f"{self.base_url}/services/data/indexes"
        response = requests.get(
            index_url,
            auth=self.auth,
            verify=False,
            params={
                "output_mode": "json"})
        response.raise_for_status()
        return response.json().get("entry", [])

    def get_index_details(self, index_name: str) -> dict:
        """
        Retrieves details of a specific Splunk index.

        Args:
            index_name (str): Name of the index.

        Returns:
            dict: The index details in JSON format.
        """
        index_url = f"{self.base_url}/services/data/indexes/{index_name}"
        response = requests.get(
            index_url,
            auth=self.auth,
            verify=False,
            params={
                "output_mode": "json"})
        response.raise_for_status()
        return response.json()

    # --- Other Methods ---
    # Add your other methods (search, app management, server control, etc.)
    # here.


# Example usage
if __name__ == "__main__":
    # Fetch credentials from AWS Secrets Manager and initialize SplunkManager
    splunk = SplunkManager(
        base_url="https://rest.splunk.example.com",
        secret_name="splunk_admin_credentials",
        # Replace with your Secrets Manager secret name
        aws_region="us-east-1",  # Replace with your AWS region
    )

    # Example: List all indexes
    print("Indexes:", splunk.list_indexes())
