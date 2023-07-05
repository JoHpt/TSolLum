'''
This module reads the transmission spectra of the VO2 and prepares them for 
the calculation.
'''
import pandas as pd
import glob
from scipy.interpolate import interp1d
import numpy as np

def load_spectra() -> list:
    '''
    Info
    ----
    This function reads the transmission spectra from the folder 
    "input_spectra" and prepares them in a list to use them for the 
    calculation of the optical properties. For this, the string "_me_" must 
    be present in the file names for the transmission spectra of the metallic 
    state of the VO2 and for the semiconducting transmission spectra 
    accordingly "_sc_".
    
    Returns
    -------
    List
        Form of the list:
            list(DataFrame, DataFrame, ...)
    '''
    # Reads the spectra with the help of the glob module.
    simulated_spectra = glob.glob('./input_spectra/*.txt')
    
    # Separates the spectra into two groups describing the metallic 
    # and semiconducting states.
    metallic_spectra = sorted([i for i in simulated_spectra if '_me_' in i])
    semiconductive_spectra = sorted([i for i in simulated_spectra if '_sc_' in i])
    
    # Verifies that the same number of dat is present, since a semiconducting 
    # and metallic transmission spectrum must be present for each layer 
    # system of VO2.
    if len(metallic_spectra) != len(semiconductive_spectra):
        raise FileNotFoundError("Check your folder with the simulated spectra. There are not equally spectra for metallic and semiconducting states.")
    
    # Initializes an empty list and iterates over the lists containing the 
    # data for the metallic and semiconducting states.
    spectra = []
    for metallic, semiconductive in zip(metallic_spectra, semiconductive_spectra):
        
        # Checks if the names are the same without the specification string 
        # ("_me_" or "_sc_"). A calculation of the characteristics from 
        # different sample series is not useful.
        if metallic.replace('_me_', '') != semiconductive.replace('_sc_', ''):
            raise NameError("Check the file names and remember to name the metallic and semiconducting states the same, with the difference of '_me_' or '_sc_'.")
        
        # Reads the data for the metallic state into a DataFrame.
        me = pd.read_csv(metallic, sep="\t", decimal=",")
        # Calculates the linear interpolation.
        me_interp = interp1d(
            me["Wavelength (nm)"], 
            me["Transmittance (%)"])                                                                      
        
        # Determines the wavelength range of the spectrum and calculates 
        # a step size of 1nm.
        start = int(me["Wavelength (nm)"].iloc[0])
        end = int(me["Wavelength (nm)"].iloc[-1])
        steps = end - start + 1
    
        # A DataFrame with the file name and the interpolated wavelength
        # or interpolated transmission is created.
        VO2 = pd.DataFrame({
            "Filename" : metallic.replace('_me_', '').split("\\")[-1].split(".")[0],
            "Wavelength (nm)" : np.linspace(start, end, steps),
            "Transmittance (%) - metallic" : me_interp(np.linspace(start, end, steps))})
    
        # The same is done for the semiconducting transmission spectra.
        sc = pd.read_csv(semiconductive, sep="\t", decimal=",")
        sc_interp = interp1d(
            sc["Wavelength (nm)"], 
            sc["Transmittance (%)"])                                                                      
    
        start = int(sc["Wavelength (nm)"].iloc[0])
        end = int(sc["Wavelength (nm)"].iloc[-1])
        steps = end - start + 1
        
        VO2["Transmittance (%) - semiconductive"] = sc_interp(np.linspace(start, end, steps))
        
        # The DataFrame is added to a list and returned by the function.
        spectra.append(VO2)
    
    print("Spectra are successfully imported!")
    return spectra