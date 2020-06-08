import pytest

from ising.data import NRC_DATA_PATH
from ising.preprocessing import AvivCDPreprocessor
from ising.fitting_equations import HomopolymerPartitionFunctionGenerator
import os

OUTPUT_PATH = os.path.join(os.getcwd(), "tests", "test_NRC_output")

preprocessor = AvivCDPreprocessor(
    input_dir=NRC_DATA_PATH,
    output_dir=OUTPUT_PATH,
    project_name="cANK",
    glob_suffix="*.dat",
)

(
    den_nsig_const_melt_df,
    organized_melt_names,
    constructs,
) = preprocessor.preprocess()


homopolymer_pfg = HomopolymerPartitionFunctionGenerator(
    output_dir=OUTPUT_PATH, project_name="cANK", construct_names=constructs
)
frac_folded_dict = homopolymer_pfg.generate_fitting_equations()
