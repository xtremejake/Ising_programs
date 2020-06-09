import pytest
import os
from ising.data import NRC_DATA_PATH
from ising.preprocessing import AvivCDPreprocessor
from ising.fitting_equations import HomopolymerPartitionFunctionGenerator
from ising.models import IsingModel
import lmfit

OUTPUT_PATH = os.path.join(os.getcwd(), "tests", "test_NRC_output")

# preprocess the .dat files, normalizing y-values
preprocessor = AvivCDPreprocessor(
    input_dir=NRC_DATA_PATH,
    output_dir=OUTPUT_PATH,
    project_name="cANK",
    glob_suffix="*.dat",
)

(
    den_nsig_const_melt_df,
    organized_melt_names,
    construct_names,
) = preprocessor.preprocess()

# generate the homopolymer fitting funtions to be applied
homopolymer_pfg = HomopolymerPartitionFunctionGenerator(
    output_dir=OUTPUT_PATH,
    project_name="cANK",
    construct_names=construct_names,
)
frac_folded_dict = homopolymer_pfg.generate_fitting_equations()

# fit the ising model
model = IsingModel(frac_folded_dict, construct_names)

# CREATE INITIAL GUESSES
# First, thermodynamic parameters.  These are Global.
init_guesses = lmfit.Parameters()
init_guesses.add("dGN", value=6)
init_guesses.add("dGR", value=5)
init_guesses.add("dGC", value=6)
init_guesses.add("dGinter", value=-12)
init_guesses.add("mi", value=1.0)

# prepare and pass data to fit()
data_dict = {}
for name, group in den_nsig_const_melt_df.groupby("construct_melt"):
    const_name = f"{name}_1"
    for exp, group2 in group.groupby("dataset"):
        if const_name in data_dict:
            const_name = f"{name}_2"
        data_dict[const_name] = group2.values

result = model.fit(data_dict, init_guesses)
