"""This module reads the transmission spectra of the VO2 and prepares them for
the calculation.
"""
import glob
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def load_spectra() -> dict:
    '''Info
    ----
    This function reads the transmission spectra from the folder
    "input_spectra" and prepares them in a dictionary to use them for the
    calculation of the optical characteristics. For this, the string "_me_"
    must be present in the file names for the transmission spectra of the
    metallic state of the VO2 and for the semiconducting transmission spectra
    accordingly "_sc_".


    Returns
    -------
    Dictionary
        Form of the dictionary:
            {"Filename" : metallic DataFrame, semiconductive DataFrame,
             ...}
    '''
    # Reads the spectra with the help of the glob module.
    simulated_spectra = glob.glob("./input_spectra/*.txt")

    # Separates the spectra into two groups describing the metallic
    # and semiconducting states.
    metallic_spectra = sorted([i for i in simulated_spectra if "_me_" in i])
    semiconductive_spectra = sorted([i for i in simulated_spectra if "_sc_" in i])

    # Verifies that the same number of dat is present, since a semiconducting
    # and metallic transmission spectrum must be present for each layer
    # system of VO2.
    if len(metallic_spectra) != len(semiconductive_spectra):
        msg = "Check your folder with the simulated spectra. There are not equally spectra for metallic and semiconducting states."
        raise FileNotFoundError(msg)

    # Initializes an empty dictionary and iterates over the lists containing
    # the data for the metallic and semiconducting states.
    spectra = {}
    for metallic, semiconductive in zip(metallic_spectra, semiconductive_spectra):

        # Checks if the names are the same without the specification string
        # ("_me_" or "_sc_"). A calculation of the characteristics from
        # different sample series is not useful.
        if metallic.replace("_me_", "") != semiconductive.replace("_sc_", ""):
            msg = "Check the file names and remember to name the metallic and semiconducting states the same, with the difference of '_me_' or '_sc_'."
            raise NameError(msg)

        # Reads the data for the metallic state into a DataFrame.
        metallic_spec = pd.read_csv(metallic, sep="\t", decimal=",").dropna(axis=1)
        # Renames the empty header of the file to "Wavelength (nm)" to have a
        # clear differentiation in the further preparation.
        metallic_spec = metallic_spec.rename(columns={metallic_spec.columns[0]: "Wavelength (nm)"})

        # Determines the wavelength range of the spectrum and calculates
        # a step size of 1nm.
        start = int(metallic_spec["Wavelength (nm)"].iloc[0])
        end = int(metallic_spec["Wavelength (nm)"].iloc[-1])
        steps = end - start + 1

        # A new empty DataFrame is initialized to store the interpolated
        # spectra.
        new_metallic_spec = pd.DataFrame({})
        new_metallic_spec["Wavelength (nm)"] = np.linspace(start, end, steps)

        # Calculation of the linear interpolation for all columns describing
        # the transmission at the respective layer thickness.
        for data in list(metallic_spec)[1:]:
            interp = interp1d(
                metallic_spec["Wavelength (nm)"],
                metallic_spec[data])
            new_metallic_spec[data] = interp(np.linspace(start, end, steps))

        # The same is done for the semiconducting states and their
        # transmission spectra.
        semiconductive_spec = pd.read_csv(semiconductive, sep="\t", decimal=",").dropna(axis=1)
        semiconductive_spec = semiconductive_spec.rename(columns={semiconductive_spec.columns[0]: "Wavelength (nm)"})

        start = int(semiconductive_spec["Wavelength (nm)"].iloc[0])
        end = int(semiconductive_spec["Wavelength (nm)"].iloc[-1])
        steps = end - start + 1

        new_semiconductive_spec = pd.DataFrame({})
        new_semiconductive_spec["Wavelength (nm)"] = np.linspace(start, end, steps)

        for data in list(semiconductive_spec)[1:]:
            interp = interp1d(
                semiconductive_spec["Wavelength (nm)"],
                semiconductive_spec[data])
            new_semiconductive_spec[data] = interp(np.linspace(start, end, steps))

        # The dictionary is filled with the DataFrames for the transmission of
        # the metallic and semiconducting states. The key to the DataFrames is
        # also the file name without direct path and file extension.
        spectra[metallic.split("\\")[-1].split(".")[0]] = new_metallic_spec, new_semiconductive_spec

    print("Spectra are successfully imported!")
    # The dictionary is returned from the function.
    return spectra
