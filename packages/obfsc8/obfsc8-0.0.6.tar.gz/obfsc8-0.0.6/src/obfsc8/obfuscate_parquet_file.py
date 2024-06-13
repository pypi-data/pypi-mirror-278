import polars as pl
import io


def obfuscate_parquet_file(parquet_file_object,
                           columns_for_obfuscation,
                           replacement_string):
    """
    For a single Parquet file object input, replaces all values in
    specified columns with a single replacement string value,
    and returns bytes object of transformed Parquet data

    Args:
        parquet_file_object: target Parquet file object
        columns_for_obfuscation: list of target columns
        replacement_string: string to be used to replace
                              target column values
    Returns:
        BytesIO data object
    """
    try:
        parquet_obfuscation_operation = (
            pl.read_parquet(parquet_file_object).lazy()
            .with_columns(pl.col(columns_for_obfuscation)
                          .str.replace_all(r"(?s).*", replacement_string))
        )
        obfuscated_parquet_df = parquet_obfuscation_operation.collect()
        buffer = io.BytesIO()
        obfuscated_parquet_df.write_parquet(buffer)
        buffer.seek(0)

        return buffer

    except Exception as e:
        print(f'Failed to generate BytesIO object from Parquet file: {e}')
