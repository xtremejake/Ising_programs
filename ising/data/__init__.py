import pkg_resources
import glob
import os
import pandas as pd

NRC_DATA_PATH = pkg_resources.resource_filename("ising", "data/NRC_data")
PREPROCESSED_NRC_DATA_PATH = pkg_resources.resource_filename(
    "ising", "data/NRC_data/NRC_data_dnmn.csv"
)
T4V_DATA_PATH = pkg_resources.resource_filename(
    "ising", "data/T4V_data/T4Vdata_not_normalized.csv"
)

# data files for preprocessor
homopolymer_data_files = glob.glob(os.path.join(NRC_DATA_PATH, "*.dat"))

# dataframes
df_columns = [
    "denaturant concentration",
    "cd signal",
    "repeat sequence",
    "dataset number",
]
heteropolymer_data = pd.read_csv(T4V_DATA_PATH, names=df_columns)
homopolymer_data = pd.read_csv(PREPROCESSED_NRC_DATA_PATH, names=df_columns)
