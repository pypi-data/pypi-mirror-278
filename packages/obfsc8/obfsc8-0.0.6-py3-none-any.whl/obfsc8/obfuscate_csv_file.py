import polars as pl
import io


def obfuscate_csv_file(csv_file_object,
                       columns_for_obfuscation,
                       replacement_string):
    """
    For a single CSV file object input, replaces all values in
    specified columns with a single replacement string value,
    and returns bytes object of transformed CSV data

    Args:
        csv_file_object: target CSV file object
        columns_for_obfuscation: list of target columns
        replacement_string: string to be used to replace
                              target column values
    Returns:
        BytesIO data object
    """
    try:
        csv_obfuscation_operation = (
            pl.read_csv(csv_file_object).lazy()
            .with_columns(pl.col(columns_for_obfuscation)
                          .str.replace_all(r"(?s).*", replacement_string))
        )
        obfuscated_csv_df = csv_obfuscation_operation.collect()
        buffer = io.BytesIO()
        obfuscated_csv_df.write_csv(buffer)
        buffer.seek(0)

        return buffer

    except Exception as e:
        print(f'Failed to generate BytesIO object from CSV file: {e}')
