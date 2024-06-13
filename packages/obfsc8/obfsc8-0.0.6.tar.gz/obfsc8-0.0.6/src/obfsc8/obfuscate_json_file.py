import polars as pl
import io


def obfuscate_json_file(json_file_object,
                        columns_for_obfuscation,
                        replacement_string):
    """
    For a single JSON file object input, replaces all values in
    specified columns with a single replacement string value,
    and returns bytes object of transformed JSON data

    Args:
        json_file_object: target JSON file object
        columns_for_obfuscation: list of target columns
        replacement_string: string to be used to replace
                              target column values
    Returns:
        BytesIO data object
    """
    try:
        json_obfuscation_operation = (
            pl.read_json(json_file_object.read()).lazy()
            .with_columns(pl.col(columns_for_obfuscation)
                          .str.replace_all(r"(?s).*", replacement_string))
        )
        obfuscated_json_df = json_obfuscation_operation.collect()

        buffer = io.BytesIO()
        obfuscated_json_df.write_json(buffer)
        buffer.seek(0)

        return buffer

    except Exception as e:
        print(f'Failed to generate BytesIO object from JSON file: {e}')
