import sys
assert sys.version_info >= (3,), "This script is designed to run on Python 3 and above."

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
timeout=2 # Default timeout 2 seconds
def send_get_request_with_headers(url, headers, timeout=timeout):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            return data
    except urllib.error.HTTPError as e:
        logging.error("HTTP Error: %s", e.code)
        # print(f"HTTP Error: {e.code}")
    except urllib.error.URLError as e:
        # print(f"URL Error: {e.reason}")
        logging.error("HTTP Error: %s", e.reason)

# Check if string is valid json
def is_valid_json(data):
    try:
        if data is not None and data.strip():  # Check if the string is not empty or null
            json_data = json.loads(data)
            return True
    except (json.JSONDecodeError, TypeError):
        pass
    return False

# Check against Azure metadata service
# https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux
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

# Check against AWS metadata service
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
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

# Check against GCP metadata service
# https://cloud.google.com/compute/docs/metadata/overview
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


# Check against OCI metadata service
# https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/gettingmetadata.htm#accessing__linux
def is_oci():
    try:
        url = "http://169.254.169.254/opc/v2/instance/region"
        custom_headers = {"Authorization": "Bearer Oracle"}
        logging.info("Try to check if VM is running in OCI")
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



# Check against Ali Cloud metadata service
# https://www.alibabacloud.com/help/en/elastic-compute-service/latest/view-instance-metadata
def is_aliyun():
    try:
        url = "http://100.100.100.200/latest/meta-data/region-id"
        custom_headers = {}
        logging.info("Try to check if VM is running in AliCloud/AliYun")
        logging.info("Query %s: ", url)
        response_data = send_get_request_with_headers(
            url, headers=custom_headers)
        if isinstance(response_data, str):
            return True
        else:
            return False
    except Exception as e:
        logging.error("Exception occurred: %s", str(e))
        return False


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
    elif is_aliyun():
        return "aliyun"
    else:
        return None  # Return None or handle the case when no provider is detected


# return finding
def main():
    cloud_provider = check_cloud_provider()
    if cloud_provider:
        logging.info("The detected cloud provider is: %s", cloud_provider)
    else:
        logging.info("No cloud provider detected.")
    return cloud_provider


if __name__ == "__main__":
    value = main()
    print(value)
