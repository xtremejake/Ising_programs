import os
import glob
import json


class BasePreprocessor:
    """Provides basic file manipulation, data formatting/manipulation, and normalization functions"""

    def __init__(
        self,
        input_dir=None,
        output_dir=None,
        project_name=None,
        glob_suffix=None,
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.glob_suffix = glob_suffix
        self.project_name = project_name
        self.glob_path = os.path.join(input_dir, self.glob_suffix)

        # create output directory if it does not already exist
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def glob_filepaths(self):
        """Returns the list of filepaths matching the glob_suffix"""
        files = glob.glob(self.glob_path)
        print(files)
        return files

    def normalize_y_values(self, xy):
        """Normalizes the y values of the signal

        Accepts: np.array(float[])
        Returns: float[]
        """
        maxval = max(xy[:, 1])
        minval = min(xy[:, 1])
        normylist = [
            float(((xy[i, 1] - maxval) / (minval - maxval)))
            for i in range(len(xy))
        ]
        return normylist

    def organize_homopolymer_melts_by_name(self, melts):
        """
        This loop puts melts in order of type (NRxC, NRx, RxC) and length.  This is useful for the
        plotting script below, putting the by_melt legends in a sensible order

        Accepts: str[] - construct names
        Returns: str[] - ordered construct names
        """
        NRClist = []
        NRlist = []
        RClist = []
        melts.sort()  # Puts in order based on length
        for melt in melts:
            if melt[0] == "N":
                if melt[-3] == "C":
                    NRClist.append(melt)
                else:
                    NRlist.append(melt)
            else:
                RClist.append(melt)

        melts = NRClist + NRlist + RClist
        return melts

    def save_construct_names(self, constructs):
        """
        Saves the construct file as a .json to be loaded for input into the partition function generator
        Accepts: str[] - construct names
        Returns: None - saves a .json of construct names to the output directory
        """
        # Write out the results.
        constructs_filename = os.path.join(
            self.output_dir, f"{self.project_name}_constructs.json"
        )
        self._save_json(constructs_filename, constructs)

    def save_melt_names(self, melts):
        """
        Saves the melts
        Accepts: np.array[]- a list of numpy arrays
        Returns: None - saves a .json of construct names to the output directory
        """
        # Write out the results.
        melts_filename = os.path.join(
            self.output_dir, f"{self.project_name}_melts.json"
        )
        self._save_json(melts_filename, melts)

    def _save_json(self, filepath, obj):
        with open(filepath, "w") as file:
            json.dump(obj, file)
