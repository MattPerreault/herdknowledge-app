import os
import boto3


def fetch_duckdb_from_s3():
    s3 = boto3.client("s3")

    bucket = os.environ["HERD_KNOWLEDGE_BUCKET"]
    key = os.environ["DUCKDB_S3_KEY"]
    local_path = os.environ["DUCKDB_PATH"]

    folder = os.path.dirname(local_path)
    if not os.path.exists(folder):
        print(f"📂 Creating directory: {folder}")
        os.makedirs(folder, exist_ok=True)

    try:
        print(f"Downloading DuckDB from s3://{bucket}/{key}")
        s3.download_file(bucket, key, local_path)
        print(f"📦 File size: {os.path.getsize(local_path)} bytes")
    except Exception as e:
        print(f"Failed to download from S3 {e}")

    return local_path
