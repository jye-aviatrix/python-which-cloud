# python-which-cloud
This python script uses standard library, runs on IaaS VM in AWS, Azure, GCP, OCI, AliCloud. It will query each cloud provider's metadata service to determine which cloud it's running on

# Return values
The return value could be one of the following:
- aws
- azure
- gcp
- oci
- aliyun


# Issues
- As time of written, some of the cloud service providers (CSP) are releasing v2 of metadata services, such as OCI and AWS. OCI is recommending to retire v1 of metadata service while AWS is keeping both v1 and v2 for now.
- It's a potential risk that the used metadata service URL would change in the future.
- If the VM is not planning to move from one CSP to another, then it would be easier to provide CSP name via user data bootstrapping.
- Ali Cloud would timeout trying to reach other CSP's metadata service, now that the checking is done sequentially based on current market share of each CSP, most other CSP would complete the script sub a second, while Ali Cloud need to wait for up to 8 seconds to get a response, as default timeout for each HTTP command is set to 2 seconds
