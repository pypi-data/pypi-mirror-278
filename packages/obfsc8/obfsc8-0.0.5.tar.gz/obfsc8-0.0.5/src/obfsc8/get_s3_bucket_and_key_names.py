import json


def get_s3_bucket_and_key_names(input_json):
    """
    Extracts S3 bucket and key names from "file_to_obfuscate"
    field in input JSON string

    Args:
        input_json: target JSON string

    Returns:
        s3_bucket:  string matching name of S3 bucket
        s3_key:     string matching name of S3 key
    """
    try:
        input_json_as_object = json.loads(input_json)

        input_filename = input_json_as_object["file_to_obfuscate"]
        input_filename_elements = input_filename.split('/')

        s3_bucket = input_filename_elements[2]
        s3_key = ('/').join(input_filename_elements[3:])

        return s3_bucket, s3_key

    except Exception as e:
        print(f'Could not read S3 bucket and key name from JSON: {e}')
