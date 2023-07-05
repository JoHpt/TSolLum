'''
This module is used for calculation of optical parameters of transmission 
spectra of VO2 thin film systems.
'''
from load_spectra import load_spectra
import pandas as pd
from scipy.integrate import simpson

def calculate() -> pd.DataFrame:
    '''
    Info
    ----
    The function uses the entered simulated spectra of VO2 and calculates them 
    with the help of the reference spectra:
        - D65
        - V-Lambda
        - ASTM-G-173
    To the optical characteristics:
        - Tlum (metallic state)
        - Tlum (semiconducting state)
        - ΔTlum
        - Tsol (metallic state)
        - Tsol (semiconducting state)
        - ΔTsol
        - ΔT@2500nm
        
    Returns
    -------
    DataFrame
    '''
    
    # Set a file name so that the calculations can be saved.
    filename = input("Please set a filename:")
    
    # An undefined file name leads to a NameError.
    if filename == "":
        raise NameError("Please specify a file name under which the results will be saved.")
    
    # Reads in the reference spectra.
    d65 = pd.read_csv(".\\init\\reference_spectra\\d65.txt", sep="\t")
    vlambda = pd.read_csv(".\\init\\reference_spectra\\v-lambda.txt", sep="\t")
    astm_g_173 = pd.read_csv(".\\init\\reference_spectra\\astm_g_173.txt", sep="\t")
    
    # Loads the simulated spectra.
    spectra = load_spectra()
    
    # Iterates over all spectra.
    for spectra in spectra:
    
        # ==================================================== #
        # ===================Calculate Tlum=================== #
        # ==================================================== #
        
        # Cuts the spectra for the calculation of Tlum to a wavelength range 
        # from 380 to 780nm.
        Tlum_spectra = (spectra[(spectra["Wavelength (nm)"] >= 380) & 
                                (spectra["Wavelength (nm)"] <= 780)]
                        ).reset_index(drop=True)
        
        # Calculates the denominator using the product of the reference 
        # spectra D65 and V-lambda. This product is integrated over the entire 
        # range using Simpson's rule.
        denominator = simpson(
            d65["CIE Standard Illuminant D65"] * vlambda["spectral sensistivity"], 
            x=Tlum_spectra["Wavelength (nm)"], dx=1.0, axis=-1, even='avg')
        
        # Calculates the numerator using the product of the Simulated Spectrum
        # and the D65 and V-Lambda reference spectra. This product is integrated
        # over the entire range using Simpson's rule.
        
        # This is done for the metallic and semiconductive state of the VO2.
        numerator_metallic = simpson(
            Tlum_spectra["Transmittance (%) - metallic"] * 
            d65["CIE Standard Illuminant D65"] * 
            vlambda["spectral sensistivity"], 
            x=Tlum_spectra["Wavelength (nm)"], dx=1.0, axis=-1, even='avg')
        
        numerator_semiconductive = simpson(
            Tlum_spectra["Transmittance (%) - semiconductive"] * 
            d65["CIE Standard Illuminant D65"] * 
            vlambda["spectral sensistivity"], 
            x=Tlum_spectra["Wavelength (nm)"], dx=1.0, axis=-1, even='avg')
        
        # The fraction of the numerator and denominator is calculated for 
        # the metallic and semiconducting state.
        Tlum_metallic = numerator_metallic / denominator
        Tlum_semiconductive = numerator_semiconductive / denominator
        
        # The difference between the two states is calculated.
        deltaTlum = Tlum_semiconductive - Tlum_metallic
        
        # ==================================================== #
        # ===================Calculate Tsol=================== #
        # ==================================================== #
        
        # Cuts the spectra for the calculation of Tsol to a wavelength range 
        # from 200 to 3000nm.
        Tsol_spectra = spectra[(spectra["Wavelength (nm)"] >= 200) & 
                                (spectra["Wavelength (nm)"] <= 3000)]
        
        # Calculates the denominator using the product of the reference 
        # spectrum ASTM-G-173. This product is integrated over the entire 
        # range using Simpson's rule.
        denominator = simpson(
            astm_g_173["Global Total Spectral Irradiance. tilt 37Deg"], 
            x=Tsol_spectra["Wavelength (nm)"], dx=1.0, axis=-1, even='avg')
        
        # Calculates the numerator using the product of the Simulated Spectrum
        # and ASTM-G-173 reference spectrum. This product is integrated
        # over the entire range using Simpson's rule.
        
        # This is done for the metallic and semiconductive state of the VO2.        
        numerator_metallic = simpson(
            Tsol_spectra["Transmittance (%) - metallic"] * 
            astm_g_173["Global Total Spectral Irradiance. tilt 37Deg"], 
            x=Tsol_spectra["Wavelength (nm)"], dx=1.0, axis=-1, even='avg')
        
        numerator_semiconductive = simpson(
            Tsol_spectra["Transmittance (%) - semiconductive"] * 
            astm_g_173["Global Total Spectral Irradiance. tilt 37Deg"], 
            x=Tsol_spectra["Wavelength (nm)"], dx=1.0, axis=-1, even='avg')
        
        # The fraction of the numerator and denominator is calculated for 
        # the metallic and semiconducting state.
        Tsol_metallic = numerator_metallic / denominator
        Tsol_semiconductive = numerator_semiconductive / denominator
        
        # The difference between the two states is calculated.
        deltaTsol = Tsol_semiconductive - Tsol_metallic
        
        # ===================================================== #
        # ===================Calculate T2500=================== #
        # ===================================================== #
        
        # The spectrum is set to the data point at 2500nm to calculate the 
        # difference in transmittance between the semiconducting and 
        # metallic states.
        T2500 = spectra.loc[(spectra["Wavelength (nm)"] == 2500)]
        deltaT2500 = (T2500["Transmittance (%) - semiconductive"] - 
                      T2500["Transmittance (%) - metallic"]).values[0]
        
        # A DataFrame with the calculated characteristics is created.
        results = pd.DataFrame({"Filename" : [spectra["Filename"][0]],
                                "Tlum (metallic)" : [Tlum_metallic],
                                "Tlum (semiconductive)" : [Tlum_semiconductive],
                                "ΔTlum" : [deltaTlum],
                                "Tsol (metallic)" : [Tsol_metallic],
                                "Tsol (semiconductive)" : [Tsol_semiconductive],
                                "ΔTsol" : [deltaTsol],
                                "ΔT@2500" : [deltaT2500]})
        
        # This DataFrame is saved in the "output" folder as ".txt".
        results.to_csv(f".\\output\\{filename}.txt", sep="\t", header=True, index=False, decimal=".")
        return results