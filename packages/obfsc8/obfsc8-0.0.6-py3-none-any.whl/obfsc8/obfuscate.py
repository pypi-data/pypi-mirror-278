from .get_s3_bucket_and_key_names \
    import get_s3_bucket_and_key_names
from .get_file_object_from_s3_bucket \
    import get_file_object_from_s3_bucket
from .get_filetype import get_filetype
from .get_columns_to_be_obfuscated \
    import get_columns_to_be_obfuscated
from .obfuscate_csv_file import obfuscate_csv_file
from .obfuscate_parquet_file import obfuscate_parquet_file
from .obfuscate_json_file import obfuscate_json_file


def obfuscate(input_json, restricted_fields=[], replacement_string="***"):
    """
    Replaces all values within specified column/s, in CSV, Parquet or JSON
    file loaded from S3 bucket, with single replacement string, and writes
    resulting file in the same file format as a streamable object

    Args:
        input_json: JSON string detailing "file_to_obfuscate" and "pii_fields"
        , e.g.,
        '{
        "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
        "pii_fields": ["name", "email_address"]
        }'

        restricted_fields: list of fields that cannot be overwritten,
                            regardless of contents of input_json (default = [])

        replacement_string: string to be used to replace all values in the
                            specified PII fields (default = "***")
    Returns:
        BytesIO object containing obfuscated file data
    """

    s3_bucket_name, s3_key_name = get_s3_bucket_and_key_names(input_json)
    retrieved_file_object = (get_file_object_from_s3_bucket
                             (s3_bucket_name, s3_key_name))
    filetype = get_filetype(s3_key_name)
    columns_to_be_obfuscated = (get_columns_to_be_obfuscated
                                (input_json, restricted_fields))

    if filetype == "csv":
        transformed_file_data = (
            obfuscate_csv_file(
                retrieved_file_object,
                columns_to_be_obfuscated,
                replacement_string))

        return transformed_file_data

    elif filetype == 'parquet':
        transformed_file_data = (
            obfuscate_parquet_file(
                retrieved_file_object,
                columns_to_be_obfuscated,
                replacement_string))

        return transformed_file_data

    elif filetype == 'json':
        transformed_file_data = (
            obfuscate_json_file(
                retrieved_file_object,
                columns_to_be_obfuscated,
                replacement_string))

        return transformed_file_data
