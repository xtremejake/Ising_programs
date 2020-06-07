import numpy as np
import pandas as pd
import os
import time
from .base import BasePreprocessor


class AvivCDPreprocessor(BasePreprocessor):
    """
    Preprocesses .dat files from Aviv CD instruments
    """

    def __init__(
        self,
        input_dir=None,
        output_dir=None,
        project_name=None,
        glob_suffix="*.dat",
    ):
        BasePreprocessor.__init__(
            self,
            input_dir=input_dir,
            output_dir=output_dir,
            project_name=project_name,
            glob_suffix=glob_suffix,
        )

    def preprocess(self):
        """Preprocesses the CD data by extracting the X,Y values, and preparing a pandas dataframe object

        Accepts: None - preprocesses the data according to the structure defined in __init__
        Returns: None - saves the output files needed for 1) generating partition functions and 2) fitting the data
        """
        start = time.time()
        print(
            f"Preprocessing data from:\ninput_path={self.input_dir}\noutput_path={self.output_dir}..."
        )
        # obatin the .dat files
        data_files = self.glob_filepaths()

        # extract cd signal, normalize data, store contruct names
        constructs = []
        melt_filenames = []
        all_dataframes = []
        for num, filename in enumerate(data_files):

            # filename handling
            num += 1
            base = os.path.basename(filename)
            melt_name = base.split(".")[0]

            # Store the names of each construct to map to partition functions
            construct_name = melt_name[:-2]
            if construct_name not in constructs:
                constructs.append(construct_name)

            # Extract the X,Y values
            xyarray = self.extract_cd_signal_from_dat(filename)

            # Normalize the Y-values from 0-1
            normylist = self.normalize_y_values(xyarray)

            # Format melt data for fitting in ising script - build a numpy array to output for Ising fitter.
            melt_array = np.array(
                [
                    [xyarray[i, 0], normylist[i], construct_name, num,]
                    for i in range(len(xyarray))
                ]
            )

            # Columns are denaturant, normalized CD, construct, melt number.
            melt_df = pd.DataFrame(
                melt_array,
                columns=["denat", "signal", "construct_melt", "dataset"],
            )

            # store the dataframes and the melt names
            all_dataframes.append(melt_df)
            melt_filenames.append(melt_name)

        # combine the dataframes into one and save as a .csv
        den_nsig_const_melt_df = pd.concat(all_dataframes)
        den_nsig_const_melt_df.to_csv(
            f"{self.output_dir}{self.project_name}_combined_data.csv",
            index=False,
            header=False,
        )

        # organize the filenames for plotting, etc.
        organized_melt_names = self.organize_melts_by_name(melt_filenames)

        # save melt arrays to be loaded prior to fitting
        np.save(
            f"{self.output_dir}{melt_name}", melt_array
        )  # Writes an npy file to disk

        # save construct names
        self.save_construct_names(constructs)

        # save organized melt names
        self.save_melt_names(organized_melt_names)

        stop = time.time()
        runtime = stop - start
        print(
            f"Preprocessing complete.\nThe elapsed time was {str(runtime)} seconds"
        )
        return den_nsig_const_melt_df, organized_melt_names, constructs

    def extract_cd_signal_from_dat(self, filepath):
        """Extracts the X,Y values (denaturant, CD signal) from an Aviv .dat file
        Accepts:
            -filepath: str the filepath location of the .dat file
        Returns:
            - np.array(float[])
        """
        xylist = []
        with open(filepath, "r") as f:

            # define the beginning and end of the data
            lines = f.read().splitlines()
            begin = 0
            end = 0

            while not lines[begin] == "$DATA":
                begin = begin + 1
            begin = begin + 4

            while not lines[end] == "$ENDDATA":
                end = end + 1

            # extract the [denat] and CD signal
            for row in range(begin, end - 1):
                line = lines[row]
                n = line.split()
                xylist.append([float(n[0]), float(n[1])])
        return np.array(xylist)
