import os
import boto3

aws_access_key_id = os.environ["AWS_ACCESS_KEY"]
aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]


def fetch_duckdb_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )

    bucket = os.environ["HERD_KNOWLEDGE_BUCKET"]
    key = os.environ["DUCKDB_S3_KEY"]
    local_path = os.environ["DUCKDB_PATH"]

    folder = os.path.dirname(local_path)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    try:
        s3.download_file(bucket, key, local_path)
    except Exception as e:
        print(f"Failed to download from S3 {e}")

    return local_path
