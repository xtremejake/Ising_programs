from ising.data import NRC_DATA_PATH
from ising.preprocessing import AvivCDPreprocessor
import os
import pytest

GLOB_SUFFIX = "*.dat"
PROJECT_NAME = "cANK"


@pytest.fixture(scope="function")
def new_aviv_cd_preprocessor_homopolymer_fixture(tmpdir):
    """Creates a new aviv cd preprocessor fixture with params"""
    preprocessor = AvivCDPreprocessor(
        input_dir=NRC_DATA_PATH,
        output_dir=tmpdir,
        project_name=PROJECT_NAME,
        glob_suffix=GLOB_SUFFIX,
    )
    return preprocessor


def test_homopolymer_preprocessor_initialized_correctly(
    new_aviv_cd_preprocessor_homopolymer_fixture, tmpdir
):
    """Tests if the preprocessor has been initialized correctly"""
    preprocessor = new_aviv_cd_preprocessor_homopolymer_fixture
    assert (
        preprocessor.glob_path == os.path.join(NRC_DATA_PATH, GLOB_SUFFIX)
        and preprocessor.project_name == PROJECT_NAME
        and preprocessor.output_dir == tmpdir
    )


def test_preprocess_homopolymer(
    new_aviv_cd_preprocessor_homopolymer_fixture, tmpdir
):
    """Tests the preprocessing function of the aviv cd module applied to the supplied heteropolymer data"""
    preprocessor = new_aviv_cd_preprocessor_homopolymer_fixture
    (
        den_nsig_const_melt_df,
        organized_melt_names,
        construct_names,
    ) = preprocessor.preprocess()

    expected_organized_melt_names = [
        "N_R_C_1",
        "N_R_C_2",
        "N_R_R_C_1",
        "N_R_R_C_2",
        "N_R_R_R_C_1",
        "N_R_R_R_C_2",
        "N_R_R_1",
        "N_R_R_2",
        "N_R_R_R_1",
        "N_R_R_R_2",
        "N_R_R_R_R_1",
        "N_R_R_R_R_2",
        "R_R_C_1",
        "R_R_C_2",
        "R_R_R_C_1",
        "R_R_R_C_2",
        "R_R_R_R_C_1",
        "R_R_R_R_C_2",
    ]

    expected_construct_names = [
        "R_R_R_C",
        "N_R_C",
        "N_R_R_R",
        "N_R_R",
        "N_R_R_C",
        "R_R_C",
        "N_R_R_R_C",
        "N_R_R_R_R",
        "R_R_R_R_C",
    ]

    expected_df_shape = (499, 4)
    assert (
        tmpdir.join(f"{PROJECT_NAME}_combined_data.csv").exists()
        and organized_melt_names == expected_organized_melt_names
        and construct_names == expected_construct_names
        and den_nsig_const_melt_df.shape == expected_df_shape
    )


@pytest.mark.skip(reason="TODO - too lazy")
def test_extract_cd_signal_from_dat(
    new_aviv_cd_preprocessor_homopolymer_fixture,
):
    """Tests the logic to extract data from aviv .dat files"""
    return None
