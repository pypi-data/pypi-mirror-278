import json


def get_columns_to_be_obfuscated(input_json, restricted_fields):
    """
    Extracts names of fields to be obfuscated,
    from "pii_fields" field in input JSON string

    Args:
        input_json: target JSON string
        restricted_fields: list of fields that cannot be overwritten,
                regardless of contents of input_json (default = [])

    Returns:
        List of field names
    """
    try:
        input_params = json.loads(input_json)

        columns_for_obfuscation = input_params["pii_fields"]
        columns_to_be_obfuscated = ([column for column
                                    in columns_for_obfuscation
                                    if column not in restricted_fields])

        return columns_to_be_obfuscated

    except Exception as e:
        print(
            f"Could not extract columns to be obfuscated from JSON input: {e}")
