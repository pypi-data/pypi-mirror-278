import polars.testing as pt
import polars as pl

from test_data.test_dataframe import test_dataframe


def test_that_s3_csv_written_and_retrieved_without_data_change(csv_from_s3):

    csv_file_from_s3_as_df = pl.read_csv(csv_from_s3)

    pt.assert_frame_equal(test_dataframe, csv_file_from_s3_as_df)
