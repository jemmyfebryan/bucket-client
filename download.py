import boto3
from tqdm import tqdm
import os

# Configuration
bucket_name = "jemmy_bucket"
object_key = "my_files/Warcraft.zip"           # S3 object key (file name in S3)
destination_path = "downloads/Warcraft.zip"  # Local path to save the file

# Ensure destination folder exists
os.makedirs(os.path.dirname(destination_path), exist_ok=True)

# Create S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("BUCKET_SECRET_KEY"),
    endpoint_url='https://storage.googleapis.com'
)

# Get object metadata (for file size)
response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
file_size = response['ContentLength']

# Setup TQDM progress bar
progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=object_key)

# Callback to update progress
def download_progress(chunk):
    progress.update(chunk)

# Use download_fileobj with callback
with open(destination_path, 'wb') as f:
    s3_client.download_fileobj(
        Bucket=bucket_name,
        Key=object_key,
        Fileobj=f,
        Callback=download_progress
    )

progress.close()
print(f"\nDownloaded to: {destination_path}")
