import pytest
from unittest.mock import patch, MagicMock
from core.python.splunk.deployer import Deployer

# Sample fixture for initializing the Deployer class
@pytest.fixture
def deployer_instance():
    return Deployer(base_url="https://splunk.example.com", auth=("admin", "password"))

# Test: Initialize the Deployer instance
def test_deployer_initialization(deployer_instance):
    assert deployer_instance.base_url == "https://splunk.example.com"
    assert deployer_instance.auth == ("admin", "password")

# Test: Deploy an app successfully
@patch("core.python.splunk.deployer.requests.post")
def test_deploy_app_success(mock_post, deployer_instance):
    # Mock response for successful deployment
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "success"}

    response = deployer_instance.deploy_app(app_name="example_app", version="1.0")
    assert response["status"] == "success"
    mock_post.assert_called_once_with(
        "https://splunk.example.com/apps/deploy",
        json={"app_name": "example_app", "version": "1.0"},
        auth=("admin", "password"),
    )

# Test: Deploy an app with failure
@patch("core.python.splunk.deployer.requests.post")
def test_deploy_app_failure(mock_post, deployer_instance):
    # Mock response for failed deployment
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"status": "failure", "error": "Invalid app"}

    with pytest.raises(Exception, match="Invalid app"):
        deployer_instance.deploy_app(app_name="invalid_app", version="1.0")
    mock_post.assert_called_once_with(
        "https://splunk.example.com/apps/deploy",
        json={"app_name": "invalid_app", "version": "1.0"},
        auth=("admin", "password"),
    )

# Test: Check app status
@patch("core.python.splunk.deployer.requests.get")
def test_check_app_status(mock_get, deployer_instance):
    # Mock response for app status
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"app_name": "example_app", "status": "deployed"}

    status = deployer_instance.check_app_status(app_name="example_app")
    assert status["status"] == "deployed"
    mock_get.assert_called_once_with(
        "https://splunk.example.com/apps/status",
        params={"app_name": "example_app"},
        auth=("admin", "password"),
    )

# Test: Validate invalid base URL
def test_invalid_base_url():
    with pytest.raises(ValueError, match="Invalid base URL"):
        Deployer(base_url="ftp://invalid.url", auth=("admin", "password"))
