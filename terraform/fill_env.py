import boto3
from dotenv import dotenv_values

# Initialize the S3 client
s3_client = boto3.client('s3')

# Function to get the URL of the S3 bucket
def get_s3_bucket_url(bucket_name):
    try:
        bucket_url = s3_client.generate_presigned_url(
            'get_bucket_location',
            Params={'Bucket': bucket_name}
        )
        return bucket_url
    except Exception as e:
        print(f"Error getting S3 bucket URL: {e}")
        return None

# Fetch S3 bucket URL
bucket_name = 'bucketpostgram'  # Replace with your actual bucket name
s3_url = get_s3_bucket_url(bucket_name)

# Load existing environment variables
env_vars = dotenv_values(".env")

# Add or update the S3_URL variable
env_vars["S3_URL"] = s3_url

# Write the updated environment variables to .env file
with open(".env", "w") as env_file:
    for key, value in env_vars.items():
        env_file.write(f"{key}={value}\n")
