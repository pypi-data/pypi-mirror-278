import os
import sys

def get_aws_credentials():
    print("Please enter your AWS credentials.")
    aws_access_key_id = input("AWS Access Key ID: ")
    aws_secret_access_key = input("AWS Secret Access Key: ")
    aws_default_region = input("AWS Default Region (e.g., us-east-1): ")

    return aws_access_key_id, aws_secret_access_key, aws_default_region

def save_aws_credentials(aws_access_key_id, aws_secret_access_key, aws_default_region):
    aws_credentials_content = f"""
[default]
aws_access_key_id = {aws_access_key_id}
aws_secret_access_key = {aws_secret_access_key}
region = {aws_default_region}
    """

    aws_credentials_path = os.path.expanduser("~/.aws/credentials")
    aws_config_path = os.path.expanduser("~/.aws/config")

    os.makedirs(os.path.dirname(aws_credentials_path), exist_ok=True)
    os.makedirs(os.path.dirname(aws_config_path), exist_ok=True)

    with open(aws_credentials_path, 'w') as credentials_file:
        credentials_file.write(aws_credentials_content)

    aws_config_content = f"""
[default]
region = {aws_default_region}
    """

    with open(aws_config_path, 'w') as config_file:
        config_file.write(aws_config_content)

    print("AWS credentials saved successfully.")

def main():
    aws_access_key_id, aws_secret_access_key, aws_default_region = get_aws_credentials()
    save_aws_credentials(aws_access_key_id, aws_secret_access_key, aws_default_region)

if __name__ == '__main__':
    main()
