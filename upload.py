import boto3
from tqdm import tqdm
import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Configuration
file_path = "./Warcraft.zip"
bucket_name = "jemmy_bucket"
# object_name = os.path.basename(file_path)
object_name = "my_files/Warcraft.zip"

# Get file size
file_size = os.path.getsize(file_path)

# Create S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("BUCKET_SECRET_KEY"),
    endpoint_url='https://storage.googleapis.com'
)

# Setup TQDM progress bar
progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=object_name)

# Define progress callback
def upload_progress(chunk):
    progress.update(chunk)

# Upload using the S3 Transfer Manager
from boto3.s3.transfer import TransferConfig

config = TransferConfig(
    multipart_threshold=1024 * 25,  # 25MB
    max_concurrency=4,
    multipart_chunksize=1024 * 25,  # 25MB
    use_threads=True
)

s3_client.upload_file(
    Filename=file_path,
    Bucket=bucket_name,
    Key=object_name,
    Callback=upload_progress,
    Config=config
)

progress.close()
