import os
import pandas as pd
from lmfit import Minimizer, fit_report

from .helpers import *
from .functions import *

class PrimarySolver:
    # Class Constants
    DATA_PATH = "./data/NLData.csv" # Default path to data
    DOCS_PATH = "./docs/" # Default path to save docs
    IMG_PATH = "./img/" # Default path to save images

    REPORT_NAME = "report.txt"
    
    PRINT_ITERS = 100 # Print solve status after this many iterations
    NUM_ITERS = 10 # Iterate solve w/ new randomized weights this many times
    NUM_PARAMS = 7 # Number of parameters in objective function

    def read(self, path=DATA_PATH):
        """
        Import NL data from given CSV file.

        Keyword Arguments:
        path -- the path to the desired data file, defaults to DATA_PATH static var
        """
        # Read CSV
        df = pd.read_csv(path, index_col=0)

        # Format time as datetime object
        df["t"] = df["t"].apply(str_to_datetime)

        # Extract training & validation datasets
        self.char_1_data = df[df["test_name"] == "char_1"]
        self.char_2_data = df[df["test_name"] == "char_2"]
        self.val_data = df[df["test_name"] == "val"]

    def solve(self, char_set="all", method="least_sq"):
        """
        Finds f(x,y,z,p) such that the error ||v-f(x,y,z,p)|| is minimized.

        Utilizes lmfit optimization library (based on SciPy)

        Keyword Arguments:
        char_set   -- the dataset to use, by default utilizes all available training data
        method     -- the least squares minimization method to use, by default Levenberg-Marquardt
                                This was experimentally determined to produce best results

        Returns:
        bestResult -- the best model parameters found through NL least squares minimization
        """

        # Prepare data
        if char_set == "char_1":
            x = self.char_1_data["x"]
            y = self.char_1_data["y"]
            z = self.char_1_data["z"]
            v = self.char_1_data["v"]
        elif char_set == "char_2":
            x = self.char_2_data["x"]
            y = self.char_2_data["y"]
            z = self.char_2_data["z"]
            v = self.char_2_data["v"]
        elif char_set == "all":
            x = pd.concat([self.char_1_data["x"], self.char_2_data["x"]])
            y = pd.concat([self.char_1_data["y"], self.char_2_data["y"]])
            z = pd.concat([self.char_1_data["z"], self.char_2_data["z"]])
            v = pd.concat([self.char_1_data["v"], self.char_2_data["v"]])
        else:
            print("ERROR: Invalid char_set")
            return

        # Perform minimization
        minner = Minimizer(residual_calc, randomize_parameters(), fcn_args=(x, y, z, v))
        self.bestResult = minner.minimize(method=method)
        if not self.bestResult.success:
            print("Error: minimization failed!")
            return
        self.bestSum = np.sum(np.square(residual_calc(self.bestResult.params, x, y, z, v)))

        # Run for a set number of times and return best params found to account 
        # for randomly landing in local min from starting values
        for i in range(self.NUM_ITERS):
            # Print iteration count
            if (i + 1) % self.PRINT_ITERS == 0:
                print("Iteration " + str(i + 1) + " of " +  str(self.NUM_ITERS))

            # Generate new parameters and re-minimize
            minner.params = randomize_parameters()
            result = minner.minimize(method=method)
            if not self.bestResult.success:
                print("Error: minimization failed!")
                return
            sum = np.sum(np.square(residual_calc(result.params, x, y, z, v)))

            # Check if new min is better
            if sum < self.bestSum:
                self.bestSum = sum
                self.bestResult = result
        return self.bestResult

    def validate(self, p=None):
        """
        Calculates resuiduals & returns RSS on validation data

        Keyword Arguments:
        p   -- custom parameters to use, by default will use bestResult.params

        Returns:
        SSR -- sum of squares of residuals from validation data
        """
        if not p:
            if not self.bestResult:
                print("Error: run solve function first!")
                return
            p = self.bestResult.params
        self.valResiduals = residual_calc(p, self.val_data["x"], self.val_data["y"], self.val_data["z"], self.val_data["v"])
        self.SSR = np.sum(np.square(self.valResiduals))
        return self.SSR

    def report(self, char_set="all", printout=False):
        """
        Generates report analyzing success of model optimization

        Keyword Arguments:
        char_set -- the dataset used, by default all available training data
        printout -- Whether to print out the report or not, by default set to False
        """
        # Ensures that both solve() and validate() have been run to correctly generate report
        if not self.bestResult:
            print("Error: run solve function first!")
            return
        if self.valResiduals is None:
            print("Error: run validate function first!")
            return

        # Retrieve correct timestamps
        if char_set == "char_1":
            t = [self.char_1_data["t"]]
        elif char_set == "char_2":
            t = [self.char_2_data["t"]]
        elif char_set == "all":
            t = [self.char_1_data["t"], self.char_2_data["t"]]
        else:
            print("ERROR: Invalid char_set")
            return

        # Generate report text
        if not os.path.exists(self.DOCS_PATH):
            os.mkdir(self.DOCS_PATH)
        file_name = self.DOCS_PATH + char_set + "_" + self.REPORT_NAME
        if not printout:
            with open(file_name, "w") as f:
                print("\nTraining results:", file=f)
                print("------------------------------------------------------", file=f)
                print(fit_report(self.bestResult), file=f)
                print("\nValidation results:", file=f)
                print("------------------------------------------------------", file=f)
                print("# data points      = " + str(len(self.val_data["v"])), file=f)
                print("chi-square         = " + str(self.SSR), file=f)
                print("reduced chi-square = " + str(self.SSR / (len(self.val_data["v"]) - len(self.bestResult.params))), file=f)
            print("Generated report at " + file_name)
        else:
            print("\nTraining results:")
            print("------------------------------------------------------")
            print(fit_report(self.bestResult))
            print("\nValidation results:")
            print("------------------------------------------------------")
            print("# data points      = " + str(len(self.val_data["v"])))
            print("chi-square         = " + str(self.SSR))
            print("reduced chi-square = " + str(self.SSR / (len(self.val_data["v"]) - len(self.bestResult.params))))

        # Generate plots
        if not os.path.exists(self.IMG_PATH):
            os.mkdir(self.IMG_PATH)
        train_img_path = self.IMG_PATH + char_set + "_train_"
        val_img_path = self.IMG_PATH + char_set + "_val_"
        if printout:
            print("\nTraining plots:")
            print("------------------------------------------------------")
        plot_residual_over_time(t, self.bestResult.residual, save_path=train_img_path)
        plot_residual_histogram(self.bestResult.residual, save_path=train_img_path)
        if printout:
            print("\nValidation plots:")
            print("------------------------------------------------------")
        plot_residual_over_time([self.val_data["t"]], self.valResiduals, save_path=val_img_path)
        plot_residual_histogram(self.valResiduals, save_path=val_img_path)
        if not printout:
            print("Generated plots at " + self.IMG_PATH)
