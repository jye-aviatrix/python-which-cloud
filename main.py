import urllib.request
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
        # Add additional handlers as needed
    ]
)

# Use standard urllib request


def send_get_request_with_headers(url, headers):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = response.read().decode("utf-8")
            return data
    except urllib.error.HTTPError as e:
        logging.error("HTTP Error: %s", e.code)
        # print(f"HTTP Error: {e.code}")
    except urllib.error.URLError as e:
        # print(f"URL Error: {e.reason}")
        logging.error("HTTP Error: %s", e.reason)


def is_valid_json(data):
    try:
        if data is not None and data.strip():  # Check if the string is not empty or null
            json_data = json.loads(data)
            return True
    except (json.JSONDecodeError, TypeError):
        pass
    return False

# Check Azure meta data service


def is_azure():
    try:
        url = "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
        custom_headers = {"Metadata": "true"}
        logging.info("Try to check if VM is running in Azure")
        logging.info("Query %s using header %s", url, str(custom_headers))
        response_data = send_get_request_with_headers(
            url, headers=custom_headers)
        # Check to make sure the response is valid json data
        if not is_valid_json(response_data):
            return False
        # Parse response json
        json_data = json.loads(response_data)
        if json_data['compute']['provider'] == "Microsoft.Compute":
            return True
        else:
            return False
    except Exception as e:
        logging.error("Exception occurred: %s", str(e))
        return False


def is_aws():
    try:
        url = "http://169.254.169.254/latest/meta-data/ami-id"
        custom_headers = {}
        logging.info("Try to check if VM is running in AWS")
        logging.info("Query %s", url)
        response_data = send_get_request_with_headers(
            url, headers=custom_headers)
        if isinstance(response_data, str):
            return True
        else:
            return False
    except Exception as e:
        logging.error("Exception occurred: %s", str(e))
        return False


def is_gcp():
    try:
        url = "http://metadata.google.internal/computeMetadata/v1/instance/zone"
        custom_headers = {"Metadata-Flavor": "Google"}
        logging.info("Try to check if VM is running in GCP")
        logging.info("Query %s using header %s", url, custom_headers)
        response_data = send_get_request_with_headers(
            url, headers=custom_headers)
        if isinstance(response_data, str):
            return True
        else:
            return False
    except Exception as e:
        logging.error("Exception occurred: %s", str(e))
        return False


def is_oci():
    # Perform OCI check here
    pass


def is_alicloud():
    # Perform AliCloud check here
    pass


def check_cloud_provider():
    # Perform the checks here
    if is_aws():
        return "aws"
    elif is_azure():
        return "azure"
    elif is_gcp():
        return "gcp"
    elif is_oci():
        return "oci"
    elif is_alicloud():
        return "alicloud"
    else:
        return None  # Return None or handle the case when no provider is detected


# Usage example
cloud_provider = check_cloud_provider()
if cloud_provider:
    print(f"The detected cloud provider is: {cloud_provider}")
else:
    print("No cloud provider detected.")
