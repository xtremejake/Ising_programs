import sympy as sp
import json
import numpy as np
import time


class HomopolymerPartitionFunctionGenerator:
    """
    Generates the Partition functions for a homopolymer 1D ising model
    """

    def __init__(
        self, output_dir=None, project_name=None, construct_names=None
    ):

        # open the filenames with the constructs
        # with open(f"{construct_names_path}", "r") as file:
        #    self.constructs = json.load(file)
        self.constructs = construct_names
        self.output_dir = output_dir
        self.project_name = project_name

        # Set parameters for partition function calculation.  Note these are sympy symbols.
        self.RT = sp.Symbol("RT")
        self.dGN = sp.Symbol("dGN")
        self.dGR = sp.Symbol("dGR")
        self.dGC = sp.Symbol("dGC")
        self.mi = sp.Symbol("mi")
        self.denat = sp.Symbol("denat")
        self.Kn = sp.Symbol("Kn")
        self.Kr = sp.Symbol("Kr")
        self.Kc = sp.Symbol("Kc")
        self.dGinter = sp.Symbol("dGinter")
        self.W = sp.Symbol("W")
        self.exp = sp.Function("np.exp")

    def generate_fitting_equations(self):
        """Generates the equations to be used in fitting a 1D homopolymer ising model"""

        start = time.time()

        # define matricies  and end vectors to be used to calculate partition functions
        begin = sp.Matrix([[0, 1]])
        N = sp.Matrix([[(self.Kn * self.W), 1], [self.Kn, 1]])
        R = sp.Matrix([[(self.Kr * self.W), 1], [self.Kr, 1]])
        C = sp.Matrix([[(self.Kc * self.W), 1], [self.Kc, 1]])
        end = sp.Matrix([[1], [1]])

        # Build dictionaries of partition functions, partial derivs with respect
        # to K, and fraction folded.

        q_dict = {}
        dqdKn_dict = {}
        dqdKr_dict = {}
        dqdKc_dict = {}
        frac_folded_dict = {}

        # Number of repeats of each type.  Seems like they should be floats, but
        # I get an error in the matrix multiplication (q_dict) if they are declared to be.

        for construct in self.constructs:

            # Make partition function dictionary and expressions for fraction folded.
            # Note, only one pf is generated per construct, even when there are multiple melts.

            matrixlist = construct.split("_")
            q_dict[construct + "_q"] = begin

            for i in range(0, len(matrixlist)):
                num_Ni = 0
                num_Ri = 0
                num_Ci = 0
                if matrixlist[i] == "N":
                    num_Ni = 1
                if matrixlist[i] == "R":
                    num_Ri = 1
                if matrixlist[i] == "C":
                    num_Ci = 1

                q_dict[construct + "_q"] = (
                    q_dict[construct + "_q"]
                    * np.linalg.matrix_power(N, num_Ni)
                    * np.linalg.matrix_power(R, num_Ri)
                    * np.linalg.matrix_power(C, num_Ci)
                )

            q_dict[construct + "_q"] = q_dict[construct + "_q"] * end

            # Next two lines convert from sp.Matrix to np.array to something else.
            # Not sure the logic here, but it works.

            q_dict[construct + "_q"] = np.array(q_dict[construct + "_q"])
            q_dict[construct + "_q"] = q_dict[construct + "_q"].item(0)

            # Partial derivs wrt Kn dictionary.
            dqdKn_dict[construct + "_dqdKn"] = sp.diff(
                q_dict[construct + "_q"], self.Kn
            )

            # Partial derivs wrt Kr dictionary.
            dqdKr_dict[construct + "_dqdKr"] = sp.diff(
                q_dict[construct + "_q"], self.Kr
            )

            # Partial derivs wrt Kc dictionary.
            dqdKc_dict[construct + "_dqdKc"] = sp.diff(
                q_dict[construct + "_q"], self.Kc
            )

            # Fraction folded dictionary.
            frac_folded_dict[construct + "_frac_folded"] = (
                self.Kn
                / (q_dict[construct + "_q"])
                * dqdKn_dict[construct + "_dqdKn"]
                + self.Kr
                / (q_dict[construct + "_q"])
                * dqdKr_dict[construct + "_dqdKr"]
                + self.Kc
                / (q_dict[construct + "_q"])
                * dqdKc_dict[construct + "_dqdKc"]
            ) / (len(matrixlist))

        # The loop below replaces K's and W's the fraction folded terms in the
        # dictionary with DGs, ms, and denaturant concentrations.  The simplify line
        # is really important for making compact expressions for fraction folded.
        # This simplification greatly speeds up fitting.  The last line
        # converts from a sympy object to a string, to allow for json dump.

        for construct in frac_folded_dict:
            frac_folded_dict[construct] = frac_folded_dict[construct].subs(
                {
                    self.Kn: (
                        self.exp(
                            -((self.dGN + (self.mi * self.denat)) / self.RT)
                        )
                    ),
                    self.Kr: (
                        self.exp(
                            -((self.dGR + (self.mi * self.denat)) / self.RT)
                        )
                    ),
                    self.Kc: (
                        self.exp(
                            -((self.dGC + (self.mi * self.denat)) / self.RT)
                        )
                    ),
                    self.W: (self.exp(-self.dGinter / self.RT)),
                }
            )
            frac_folded_dict[construct] = sp.simplify(
                frac_folded_dict[construct]
            )
            frac_folded_dict[construct] = str(frac_folded_dict[construct])

        with open(
            f"{self.output_dir}{self.project_name}_frac_folded_dict.json", "w"
        ) as file:
            json.dump(frac_folded_dict, file)

        stop = time.time()
        runtime = stop - start
        print("\nThe elapsed time was " + str(runtime) + " seconds")

        return frac_folded_dict
