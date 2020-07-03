import pytest
from ising.data import (
    homopolymer_data_files,
    heteropolymer_data,
    homopolymer_data,
)


@pytest.fixture(scope="module")
def homopolymer_data_fixture():
    """Creates a fixture for the homopolymer data *.dat files"""
    return homopolymer_data_files


@pytest.fixture(scope="module")
def homopolymer_dataframe_fixture():
    """Creates a fixture for the homopolymer dataframe NRC"""
    return homopolymer_data


@pytest.fixture(scope="module")
def heteropolymer_dataframe_fixture():
    """Creates a fixture for the heteropolymer dataframe T4V"""
    return heteropolymer_data
