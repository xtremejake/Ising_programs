import pytest
from ising.data import homopolymer_data

@pytest.fixture(scope="module")
def homopolymer_data_fixture():
    """Creates a fixture for the homopolymer data *.dat files"""
    return homopolymer_data