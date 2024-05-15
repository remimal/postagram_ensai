# from cdktf import TerraformStack, TerraformOutput
# from dotenv import dotenv_values

# # Get the current Terraform stack
# # stack = TerraformStack()

# # Retrieve the output containing the bucket ID
# bucket_id_output = TerraformOutput(None, "s3_id")

# # Load existing environment variables
# env_vars = dotenv_values(".env")

# # Add or update the S3_BUCKET_ID variable
# env_vars["S3_BUCKET_ID"] = bucket_id_output.value

# # Write the updated environment variables to .env file
# with open(".env", "w") as env_file:
#     for key, value in env_vars.items():
#         env_file.write(f"{key}={value}\n")


# import boto3

# s3_client = boto3.client('s3')

# # Get the bucket by name
# bucket_name = "bucketpostgram"  # Replace with your actual bucket name
# response = s3_client.head_bucket(Bucket=bucket_name)

# # Extract the bucket ID from the response (if bucket exists)
# if 'ResponseMetadata' in response and 'HTTPHeaders' in response['ResponseMetadata']:
#     bucket_id = response['ResponseMetadata']['HTTPHeaders']['x-amz-id-2']
# else:
#     raise Exception(f"Could not retrieve bucket ID for '{bucket_name}'.")

import subprocess

def capture_terraform_output(output_name):
  """Captures the specified Terraform output and returns it as a string."""
  command = ["terraform", "output", output_name]
  output = subprocess.check_output(command).decode('utf-8').strip()
  return output

def store_output_to_file(output_name, filename):
  """Stores the captured output in a file."""
  output = capture_terraform_output(output_name)
  with open(filename, "w") as f:
    f.write(output)

# Example usage
output_name = "s3_id"  # Replace with your output name
filename = "s3_bucket_id.txt"

store_output_to_file(output_name, filename)

