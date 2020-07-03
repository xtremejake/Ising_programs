import pytest
from ising.data import homopolymer_data, heteropolymer_df, homopolymer_df


@pytest.fixture(scope="module")
def homopolymer_data_fixture():
    """Creates a fixture for the homopolymer data *.dat files"""
    return homopolymer_data


@pytest.fixture(scope="module")
def heteropolymer_dataframe_fixture():
    """Creates a fixture for the homopolymer dataframe NRC"""
    return homopolymer_df


@pytest.fixture(scope="module")
def heteropolymer_dataframe_fixture():
    """Creates a fixture for the heteropolymer dataframe T4V"""
    return heteropolymer_df
