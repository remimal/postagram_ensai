import subprocess

def get_s3_bucket_id():
  """Retrieves the S3 bucket ID from Terraform output using subprocess."""
  command = ["terraform", "output", "s3_id"]
  output = subprocess.check_output(command).decode('utf-8').strip()
  return output

def main():
  """Main function to get and use the S3 bucket ID."""
  try:
    s3_bucket_id = get_s3_bucket_id()
    # Use the S3 bucket ID here (e.g., for interaction with Boto3)
    print(f"S3 Bucket ID: {s3_bucket_id}")  # Example usage

  except subprocess.CalledProcessError as e:
    print(f"Error retrieving S3 bucket ID: {e}")

if __name__ == "__main__":
  main()


