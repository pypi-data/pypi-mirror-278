import boto3


def get_file_object_from_s3_bucket(bucket, key):
    """
    Retrieves file streaming object from S3 bucket

    Args:
        bucket: target S3 bucket
        key:    target S3 file key
    Returns:
        Requested file as streaming object
    """
    try:
        s3 = boto3.client("s3", region_name="eu-west-2")
        get_s3_file_object = s3.get_object(Bucket=bucket, Key=key)["Body"]

        return get_s3_file_object

    except Exception as e:
        print(f"File object retrieval from S3 bucket failed: {e}")
