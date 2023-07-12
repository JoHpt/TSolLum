"""
This module is used for calculation of optical characteristics of transmission
spectra of VO2 thin film systems.
"""

import pandas as pd
from load_spectra import load_spectra
from scipy.integrate import simpson


def calculate() -> dict:
    """
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
        - ΔT@2500nm.


    Returns
    -------
    Dictionary
        Form of the dictionary:
            {"Bufferthickness_1" : {"Tlum" : metallic, semiconductive, delta},
                                 {"Tsol" : metallic, semiconductive, delta},
                                 {"T@2500nm" : T@2500nm},
            "Bufferthickness_2" : {"Tlum" : metallic, semiconductive, delta},
                                 {"Tsol" : metallic, semiconductive, delta},
                                 {"T@2500nm" : T@2500nm},
            ...
    """
    # Reads in the reference spectra.
    d65 = pd.read_csv(".\\init\\reference_spectra\\d65.txt", sep="\t")
    vlambda = pd.read_csv(".\\init\\reference_spectra\\v-lambda.txt", sep="\t")
    astm_g_173 = pd.read_csv(".\\init\\reference_spectra\\astm_g_173.txt", sep="\t")

    # Loads the simulated spectra.
    map_dict = load_spectra()
    # Reads the keys of the dictionary to iterate over them later.
    keys = list(map_dict.keys())

    # Initializes a new empty dictionary to store the results in it later.
    new_map_dict = {}

    # Iterates over the keys in the map_cit to load the metallic and
    # semiconducting DataFrames.
    for key in keys:
        metallic_map, semiconductive_map = map_dict[key]

        # Checks if the buffer layer thicknesses in the DataFrames are equal.
        # Otherwise a FileExistsError is issued.
        if list(metallic_map) != list(semiconductive_map):
            msg = "Check your simulated data. The mapping is not equaly long."
            raise FileExistsError(msg)

        # A list of buffer layer thicknesses is created to iterate over later.
        buffer_thickness = list(metallic_map)[1:]

        # ==================================================== #
        # ===================Calculate Tlum=================== #
        # ==================================================== #

        # Cuts the spectra for the calculation of Tlum to a wavelength range
        # from 380 to 780nm. The optical characteristics for the metallic and
        # semiconducting states are calculated simultaneously.
        tlum_me = (metallic_map[(metallic_map["Wavelength (nm)"] >= 380) &
                                (metallic_map["Wavelength (nm)"] <= 780)]
                        ).reset_index(drop=True)

        tlum_sc = (semiconductive_map[(semiconductive_map["Wavelength (nm)"] >= 380) &
                                (semiconductive_map["Wavelength (nm)"] <= 780)]
                        ).reset_index(drop=True)

        # Calculates the denominator using the product of the reference
        # spectra D65 and V-lambda. This product is integrated over the entire
        # range using Simpson's rule.
        denominator = simpson(
            d65["CIE Standard Illuminant D65"] * vlambda["spectral sensistivity"],
            x=tlum_me["Wavelength (nm)"], dx=1.0, axis=-1, even="avg")

        # An empty dictionary for the values of Tlum is initialized.
        tlum_dict = {}

        # It is iterated over the buffer layer thickness and Tlum is
        # calculated.
        for thickness in buffer_thickness:

            # Calculates the numerator using the product of the Simulated Spectrum
            # and the D65 and V-Lambda reference spectra. This product is integrated
            # over the entire range using Simpson's rule.

            # This is done for the metallic and semiconductive state of the VO2.
            numerator_metallic = simpson(
                tlum_me[thickness] *
                d65["CIE Standard Illuminant D65"] *
                vlambda["spectral sensistivity"],
                x=tlum_me["Wavelength (nm)"], dx=1.0, axis=-1, even="avg")

            numerator_semiconductive = simpson(
                tlum_sc[thickness] *
                d65["CIE Standard Illuminant D65"] *
                vlambda["spectral sensistivity"],
                x=tlum_sc["Wavelength (nm)"], dx=1.0, axis=-1, even="avg")

            # The fraction of the numerator and denominator is calculated for
            # the metallic and semiconducting state.
            tlum_metallic = numerator_metallic / denominator
            tlum_semiconductive = numerator_semiconductive / denominator

            # The difference between the two states is calculated.
            delta_tlum = tlum_semiconductive - tlum_metallic

            # The calculated characteristics are added to the dictionary.
            tlum_dict[thickness] = tlum_metallic, tlum_semiconductive, delta_tlum

        # ==================================================== #
        # ===================Calculate Tsol=================== #
        # ==================================================== #

        # Cuts the spectra for the calculation of Tsol to a wavelength range
        # from 200 to 3000nm. The optical characteristics for the metallic and
        # semiconducting states are calculated simultaneously.
        tsol_me = (metallic_map[(metallic_map["Wavelength (nm)"] >= 200) &
                                (metallic_map["Wavelength (nm)"] <= 3000)]
                        ).reset_index(drop=True)

        tsol_sc = (semiconductive_map[(semiconductive_map["Wavelength (nm)"] >= 200) &
                                (semiconductive_map["Wavelength (nm)"] <= 3000)]
                        ).reset_index(drop=True)

        # Calculates the denominator using the product of the reference
        # spectrum ASTM-G-173. This product is integrated over the entire
        # range using Simpson's rule.
        denominator = simpson(
            astm_g_173["Global Total Spectral Irradiance. tilt 37Deg"],
            x=tsol_me["Wavelength (nm)"], dx=1.0, axis=-1, even="avg")

        # An empty dictionary for the values of Tsol is initialized.
        tsol_dict = {}

        # It is iterated over the buffer layer thickness and Tsol is
        # calculated.
        for thickness in buffer_thickness:

            # Calculates the numerator using the product of the Simulated Spectrum
            # and ASTM-G-173 reference spectrum. This product is integrated
            # over the entire range using Simpson's rule.

            # This is done for the metallic and semiconductive state of the VO2.
            numerator_metallic = simpson(
                tsol_me[thickness] *
                astm_g_173["Global Total Spectral Irradiance. tilt 37Deg"],
                x=tsol_me["Wavelength (nm)"], dx=1.0, axis=-1, even="avg")

            numerator_semiconductive = simpson(
                tsol_sc[thickness] *
                astm_g_173["Global Total Spectral Irradiance. tilt 37Deg"],
                x=tsol_sc["Wavelength (nm)"], dx=1.0, axis=-1, even="avg")

            # The fraction of the numerator and denominator is calculated for
            # the metallic and semiconducting state.
            tsol_metallic = numerator_metallic / denominator
            tsol_semiconductive = numerator_semiconductive / denominator

            # The difference between the two states is calculated.
            delta_tsol = tsol_semiconductive - tsol_metallic

            # The calculated characteristics are added to the dictionary.
            tsol_dict[thickness] = tsol_metallic, tsol_semiconductive, delta_tsol

        # ===================================================== #
        # ===================Calculate T2500=================== #
        # ===================================================== #

        # An empty dictionary for the values of T@2500 is initialized.
        t2500_dict = {}

        # The spectrum is set to the data point at 2500nm to calculate the
        # difference in transmittance between the semiconducting and
        # metallic states.
        t2500_metallic = metallic_map.loc[(metallic_map["Wavelength (nm)"] == 2500)]
        t2500_semiconductive = semiconductive_map.loc[
            (semiconductive_map["Wavelength (nm)"] == 2500)]

        # It is iterated over the buffer layer thickness and T@2500 is
        # calculated.
        for thickness in buffer_thickness:
            t2500_dict[thickness] = (t2500_semiconductive[thickness] -
                          t2500_metallic[thickness]).values[0]

        # The calculated characteristics are added to the dictionary.
        new_map_dict[key.replace("_me", "")] = tlum_dict, tsol_dict, t2500_dict
    # The dictionary is returned from the function.
    return new_map_dict
