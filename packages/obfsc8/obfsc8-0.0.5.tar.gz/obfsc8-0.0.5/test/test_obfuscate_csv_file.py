import polars as pl
import polars.testing as pt

from obfsc8.src.obfsc8.obfuscate_csv_file import obfuscate_csv_file
from test_data.test_dataframe import test_dataframe


columns_for_obfuscation = ["name", "email_address"]


def test_that_csv_file_returned_is_not_equivalent_to_the_file_input(
        csv_from_s3):

    buffer = obfuscate_csv_file(
        csv_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_csv(buffer)

    pt.assert_frame_not_equal(test_dataframe, obfuscated_dataframe)


def test_that_all_values_in_non_target_columns_remain_unchanged(csv_from_s3):

    buffer = obfuscate_csv_file(
        csv_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_csv(buffer)

    for column_name in obfuscated_dataframe.columns:
        if column_name not in columns_for_obfuscation:
            original_column_values = test_dataframe.get_column(column_name)
            obfuscated_column_values = (obfuscated_dataframe
                                        .get_column(column_name))

            (pt.assert_series_equal(original_column_values,
                                    obfuscated_column_values))


def test_that_all_values_in_target_columns_made_equal_to_replacement_string(
        csv_from_s3):

    buffer = obfuscate_csv_file(
        csv_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_csv(buffer)

    obfuscated_column_values_list = []
    for column_name in columns_for_obfuscation:
        obfuscated_column_values = (obfuscated_dataframe
                                    .get_column(column_name))
        obfuscated_column_values_list.append(obfuscated_column_values)

    for i in range(1, len(obfuscated_column_values_list)):
        (pt.assert_series_equal(obfuscated_column_values_list[0],
                                obfuscated_column_values_list[i],
                                check_names=False))
    for j in range(0, len(obfuscated_column_values_list[0])):
        assert obfuscated_column_values_list[0][j] == "***"


def test_that_custom_string_leaves_non_target_columns_unchanged(csv_from_s3):

    buffer = obfuscate_csv_file(
        csv_from_s3, columns_for_obfuscation, "??")
    obfuscated_dataframe = pl.read_csv(buffer)

    for column_name in obfuscated_dataframe.columns:
        if column_name not in columns_for_obfuscation:
            original_column_values = test_dataframe.get_column(column_name)
            obfuscated_column_values = (obfuscated_dataframe
                                        .get_column(column_name))

            (pt.assert_series_equal(original_column_values,
                                    obfuscated_column_values))


def test_that_custom_replacement_string_replaces_values_in_target_columns(
        csv_from_s3):

    buffer = obfuscate_csv_file(
        csv_from_s3, columns_for_obfuscation, "??")
    obfuscated_dataframe = pl.read_csv(buffer)

    obfuscated_column_values_list = []
    for column_name in columns_for_obfuscation:
        obfuscated_column_values = (obfuscated_dataframe
                                    .get_column(column_name))
        obfuscated_column_values_list.append(obfuscated_column_values)

    for i in range(1, len(obfuscated_column_values_list)):
        (pt.assert_series_equal(obfuscated_column_values_list[0],
                                obfuscated_column_values_list[i],
                                check_names=False))
    for j in range(0, len(obfuscated_column_values_list[0])):
        assert obfuscated_column_values_list[0][j] == "??"
