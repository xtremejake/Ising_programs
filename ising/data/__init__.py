import pkg_resources

NRC_DATA_PATH = pkg_resources.resource_filename("ising", "data/NRC_data")
PREPROCESSED_NRC_DATA_PATH = pkg_resources.resource_filename(
    "ising", "data/NRC_data/NRC_data_dnmn.csv"
)
T4V_DATA_PATH = pkg_resources.resource_filename(
    "ising", "data/T4V_data/T4Vdata_not_normalized.csv"
)
