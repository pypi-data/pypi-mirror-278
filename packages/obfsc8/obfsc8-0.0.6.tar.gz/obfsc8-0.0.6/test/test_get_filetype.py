import pytest

from obfsc8.src.obfsc8.get_filetype import get_filetype


def test_that_string_returned():
    filename = "new_data/file1.csv"
    result = get_filetype(filename)

    assert isinstance(result, str)


def test_that_csv_returned_with_csv_file_input():
    csv_filename = "new_data/file1.csv"
    result = get_filetype(csv_filename)

    assert result == "csv"


def test_that_parquet_returned_with_parquet_file_input():
    parquet_filename = "new_data/file1.parquet"
    result = get_filetype(parquet_filename)

    assert result == "parquet"


def test_that_json_returned_with_json_file_input():
    parquet_filename = "new_data/file1.json"
    result = get_filetype(parquet_filename)

    assert result == "json"


def test_that_type_error_raised_if_input_filename_not_a_string():
    with pytest.raises(TypeError, match="must be a string"):
        get_filetype(674)


def test_that_value_error_raised_if_period_not_present_in_filename():
    with pytest.raises(ValueError, match="must contain a period"):
        get_filetype("new_data/file1")


def test_that_value_error_raised_if_filetype_not_CSV_Parquet_or_JSON():
    with (pytest.raises
          (ValueError, match="Filetype must be CSV, Parquet or JSON")):
        get_filetype("new_data/file1.jpg")
