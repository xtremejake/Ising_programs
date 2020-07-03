import pytest
import pandas as pd
from ising.data import homopolymer_data, heteropolymer_df, homopolymer_df
import os


@pytest.fixture(scope="module")
def expected_dataframe_columns_fixture():
    """Creates a fixture for the expected dataframe columns for heteropolymer and homopolymer"""
    expected_df_columns = set(
        [
            "denaturant concentration",
            "cd signal",
            "repeat sequence",
            "dataset number",
        ]
    )
    return expected_df_columns


def test_homopolymer_nrc_data_import():
    """Tests the correct homopolymer NRC data are imported"""
    expected_nrc_filenames = {
        "R_R_C_1.dat",
        "N_R_C_2.dat",
        "N_R_R_R_2.dat",
        "N_R_R_R_R_2.dat",
        "N_R_R_C_2.dat",
        "N_R_R_C_1.dat",
        "N_R_R_2.dat",
        "N_R_R_R_1.dat",
        "R_R_R_R_C_1.dat",
        "R_R_R_R_C_2.dat",
        "N_R_R_R_C_1.dat",
        "R_R_R_C_2.dat",
        "R_R_C_2.dat",
        "N_R_R_R_C_2.dat",
        "N_R_R_1.dat",
        "N_R_C_1.dat",
        "N_R_R_R_R_1.dat",
        "R_R_R_C_1.dat",
    }
    imported_nrc_filenames = set(
        [os.path.basename(item) for item in homopolymer_data]
    )
    # TODO: test for correct number of datapoints
    assert imported_nrc_filenames == expected_nrc_filenames


def test_heteropolymer_t4v_data_import(expected_dataframe_columns_fixture):
    """Tests the correct heteropolymer data are imported"""
    expected_heteropolymer_df_shape = (558, 4)

    assert (
        isinstance(heteropolymer_df, pd.DataFrame)
        and heteropolymer_df.shape == expected_heteropolymer_df_shape
        and set(heteropolymer_df.columns) == expected_dataframe_columns_fixture
    )


def test_homopolymer_dataframe_import(expected_dataframe_columns_fixture):
    """Tests the correct homopolymer dataframe is imported"""
    expected_homopolymer_df_shape = (499, 4)
    assert (
        isinstance(homopolymer_df, pd.DataFrame)
        and homopolymer_df.shape == expected_homopolymer_df_shape
        and set(homopolymer_df.columns) == expected_dataframe_columns_fixture
    )
