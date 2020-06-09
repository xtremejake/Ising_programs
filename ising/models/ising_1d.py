import os
import time
import json
import numpy as np
import pandas as pd
import copy
import lmfit


class IsingModel:
    """Fits a 1D ising model to protein folding/unfolding transitions"""

    def __init__(self, fitting_functions, construct_names):
        # fitting functions can be supplied as a dictionary or a filepath
        if not isinstance(fitting_functions, dict):
            if os.path.exists(fitting_functions):  # read from file
                fitting_functions = self._load_fitting_functions(
                    fitting_functions
                )
        self.compiled_fitting_functions = self.compile_fraction_folded_expressions(
            construct_names, fitting_functions
        )
        self.RT = 0.001987 * 298.15  # R in kcal/mol/K, T in Kelvin.

    def fitting_function(self, params, denat, frac_folded, melt):
        """The function to fit to the folding/unfolding transitions
        Accepts:
        Returns:
        """
        af = params["af_{}".format(melt)].value
        bf = params["bf_{}".format(melt)].value
        au = params["au_{}".format(melt)].value
        bu = params["bu_{}".format(melt)].value

        # is it necessary to have these here?
        dGN = params["dGN"].value
        dGR = params["dGR"].value
        dGC = params["dGC"].value
        dGinter = params["dGinter"].value
        mi = params["mi"].value
        return ((af * denat) + bf) * frac_folded + (
            ((au * denat) + bu) * (1 - frac_folded)
        )

    # Objective function creates an array of residuals to be used by lmfit minimize.
    def objective(self, params):
        resid_dict = {}

        # these might not be necessary as they would be in the global namespace
        dGN = params["dGN"].value
        dGR = params["dGR"].value
        dGC = params["dGC"].value
        dGinter = params["dGinter"].value
        mi = params["mi"].value
        for melt in self.melt_names:
            ff_melt_key = "_".join(
                melt.split("_")[:-1]
            )  # prevents error if more than double digit exp #
            denat = self.melt_data_dict[melt][
                :, 0
            ]  # A numpy array of type str
            norm_sig = self.melt_data_dict[melt][
                :, 1
            ]  # A numpy array of type str
            denat = denat.astype(float)  # A numpy array of type float
            norm_sig = norm_sig.astype(float)  # A numpy array of type float

            string_to_eval = self.compiled_fitting_functions[
                ff_melt_key + "_comp_ff"
            ]
            frac_folded = eval(string_to_eval)

            # frac_folded name gets associated for use in fitting_function call in frac_folded_string assignment above.
            af = params["af_{}".format(melt)].value
            bf = params["bf_{}".format(melt)].value
            au = params["au_{}".format(melt)].value
            bu = params["bu_{}".format(melt)].value
            resid = norm_sig - self.fitting_function(
                params, denat, frac_folded, melt
            )
            resid_dict[melt + "_resid"] = resid
        residuals = np.concatenate(list(resid_dict.values()))
        return residuals

    def fit(self, xy, init_guesses):
        """Fits the data to a 1D Ising model. Supplied fitting_functions on __init__ describe the type of
        model to fit to the data (e.g. Homopolymer/Heteropolymer)

        Accepts:
            - xy - {str:np.array()} - a dictionary of np.array()'s of each melt
            - init_guesses - lmfit.Parameters() object containing the initial guesses for thermodynamic parameters
        Returns:
        """
        # define the melts to use
        self.melt_data_dict = xy
        self.melt_names = list(self.melt_data_dict.keys())

        if not isinstance(init_guesses, lmfit.Parameters):
            raise TypeError(
                f"Supplied init_guesses: {init_guesses} are not of type lmfit.Parameters"
            )
        # Next, baseline parameters.  These are local.
        for melt in self.melt_names:
            init_guesses.add("af_{}".format(melt), value=0.02)
            init_guesses.add("bf_{}".format(melt), value=1)
            init_guesses.add("au_{}".format(melt), value=0.0)
            init_guesses.add("bu_{}".format(melt), value=0.0)

        # Transfers init_guesses to params for fitting, but init_guesses are maintained.
        params = copy.deepcopy(init_guesses)

        # Fit with lmfit
        print("Minimizing...")
        result = lmfit.minimize(self.objective, params)
        print("Complete!")
        print(f"There are a total of {len(self.melt_names)} data sets.")
        print(f"There are {result.ndata} observations.")
        print(f"There are {result.nvarys} fitted parameters.")
        print(f"There are {result.nfree} degrees of freedom. \n".format())
        print(
            "The sum of squared residuals (SSR) is: {0:7.4f}".format(
                result.chisqr
            )
        )
        print("The reduced SSR (SSR/DOF): {0:8.6f} \n".format(result.redchi))
        self.result = result
        return result

    def best_fit_params(self):
        """Prints the best fit parameters"""
        if not self.result:
            raise AttributeError(
                "No results yet! Perform a .fit() with data to obtain best fit parameters"
            )
        param_df = pd.DataFrame(
            [
                (k, self.result.params[k].value, self.result.params[k].stderr)
                for k, v in self.result.params.items()
                if not k.startswith("a") and not k.startswith("b")
            ],
            columns=["Parameter", "Value", "StdErr"],
        )
        return param_df

    def compile_fraction_folded_expressions(
        self, construct_names, frac_folded_dict
    ):
        """Compiles the fraction folded expressions for faster fitting and retrieval

        Accepts: None
        Returns: {str: <compiled function>} dictionary of construct name to fitting function map
        """
        # Compile fraction folded expressions.
        comp_frac_folded_dict = {}
        for construct in construct_names:
            frac_folded_string = frac_folded_dict[construct + "_frac_folded"]
            frac_folded_string = frac_folded_string.replace("RT", "self.RT")
            comp_frac_folded = compile(
                frac_folded_string, "{}_comp_ff".format(construct), "eval"
            )
            comp_frac_folded_dict[
                construct + "_comp_ff"
            ] = comp_frac_folded  # comp_frac_folded
        return comp_frac_folded_dict

    def _load_fitting_functions(self, filepath):
        """Loads fitting functions from a filepath location

        Accepts: str - filepath location of fitting functions to use
        Returns: dict - dictionary of fitting functions to use
        """
        with open(filepath, "r") as file:
            fitting_functions = json.load(file)
        return fitting_functions
