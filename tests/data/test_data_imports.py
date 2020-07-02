import pytest
from ising.data import homopolymer_data
import os

def test_homopolymer_nrc_data():
    """Tests the correct homopolymer NRC data are imported"""
    expected_nrc_filenames = {'R_R_C_1.dat', 'N_R_C_2.dat', 'N_R_R_R_2.dat', 'N_R_R_R_R_2.dat', 'N_R_R_C_2.dat', 'N_R_R_C_1.dat', 'N_R_R_2.dat', 'N_R_R_R_1.dat', 'R_R_R_R_C_1.dat', 'R_R_R_R_C_2.dat', 'N_R_R_R_C_1.dat', 'R_R_R_C_2.dat', 'R_R_C_2.dat', 'N_R_R_R_C_2.dat', 'N_R_R_1.dat', 'N_R_C_1.dat', 'N_R_R_R_R_1.dat', 'R_R_R_C_1.dat'}
    imported_nrc_filenames = set([os.path.basename(item) for item in homopolymer_data])
    assert imported_nrc_filenames == expected_nrc_filenames
