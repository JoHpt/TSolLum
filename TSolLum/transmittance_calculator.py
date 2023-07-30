"""transmittance_calculator.py - Module for calculating various transmittance values.

This module provides functions to calculate the luminous transmittance (Tlum)
and solar transmittance (Tsol) of a given TransmittanceSpectrum. It also offers
a function to calculate the difference in transmittance at 2500 nm (Tstroke)
between two TransmittanceSpectrum objects.

Functions:
    calculate_tlum(spectrum: TransmittanceSpectrum) -> float:
        Calculate the luminous transmittance (Tlum) of a given TransmittanceSpectrum.

    calculate_tsol(spectrum: TransmittanceSpectrum) -> float:
        Calculate the solar transmittance (Tsol) of a given TransmittanceSpectrum.

    calculate_tstroke(semiconductive_spectrum: TransmittanceSpectrum,
                      metallic_spectrum: TransmittanceSpectrum) -> float:
        Calculate the difference in transmittance at 2500 nm (Tstroke) between
        two TransmittanceSpectrum objects.

Note:
    Ensure that the input spectra are of type TransmittanceSpectrum when
    using the functions to avoid exceptions.
"""


import numpy as np
from scipy.integrate import simpson

from .exceptions import TSolLumError
from .spectra import ASTM_G_173, D65, TransmittanceSpectrum, VLambda


def calculate_tlum(spectrum : TransmittanceSpectrum) -> float:
    """Calculate the luminous transmittance (Tlum) of a given TransmittanceSpectrum.

    Parameters
    ----------
        spectrum (TransmittanceSpectrum): The TransmittanceSpectrum object
        representing the spectral transmittance.

    Returns
    -------
        float: The luminous transmittance (Tlum) value.

    Raises
    ------
        TSolLumError: If the input spectrum is not of type TransmittanceSpectrum.
    """
    # Check if spectrum is of type TransmittanceSpectrum
    if isinstance(spectrum, TransmittanceSpectrum) is False:
        msg = (f"spectrum is {type(spectrum)} "
               "but must be TransmittanceSpectrum.")
        raise TSolLumError(msg)

    # Filter out wavelengths within the range of D65 illuminant
    mask = np.logical_and(spectrum.wavelength >= min(D65.wavelength),
                          spectrum.wavelength <= max(D65.wavelength))
    wavelength = spectrum.wavelength[mask]
    transmittance = spectrum.transmittance[mask]

    # Calculate the numerator of the Tlum integral using Simpson's rule
    numerator = simpson(transmittance * D65.csi * VLambda.spectral_sensistivity,
        x=wavelength, dx=1.0, axis=-1, even="avg")

    # Calculate the denominator of the Tlum integral using Simpson's rule
    denominator = simpson(
        D65.csi * VLambda.spectral_sensistivity,
        x=wavelength, dx=1.0, axis=-1, even="avg")

    # Calculate the Tlum value
    return numerator / denominator

def calculate_tsol(spectrum : TransmittanceSpectrum) -> float:
    """Calculate the solar transmittance (Tsol) of a given TransmittanceSpectrum.

    Parameters
    ----------
        spectrum (TransmittanceSpectrum): The TransmittanceSpectrum object
        representing the spectral transmittance.

    Returns
    -------
        float: The solar transmittance (Tsol) value.

    Raises
    ------
        TSolLumError: If the input spectrum is not of type TransmittanceSpectrum.
    """
    # Check if spectrum is of type TransmittanceSpectrum
    if isinstance(spectrum, TransmittanceSpectrum) is False:
        msg = (f"spectrum is {type(spectrum)} "
               "but must be TransmittanceSpectrum.")
        raise TSolLumError(msg)

    # Filter out wavelengths within the range of ASTM G-173 solar irradiance
    mask = np.logical_and(spectrum.wavelength >= min(ASTM_G_173.wavelength),
                          spectrum.wavelength <= max(ASTM_G_173.wavelength))
    wavelength = spectrum.wavelength[mask]
    transmittance = spectrum.transmittance[mask]

    # Calculate the numerator of the Tsol integral using Simpson's rule
    numerator = simpson(transmittance * ASTM_G_173.spectral_irradiance,
        x=wavelength, dx=1.0, axis=-1, even="avg")

    # Calculate the denominator of the Tsol integral using Simpson's rule
    denominator = simpson(ASTM_G_173.spectral_irradiance,
        x=wavelength, dx=1.0, axis=-1, even="avg")

    # Calculate the Tsol value
    return numerator / denominator

def calculate_tstroke(semiconductive_spectrum : TransmittanceSpectrum,
                      metallic_spectrum : TransmittanceSpectrum) -> float:
    """Calculate the difference in transmittance at 2500 nm (Tstroke) between two
    TransmittanceSpectrum objects.

    Parameters
    ----------
        semiconductive_spectrum (TransmittanceSpectrum): The
        TransmittanceSpectrum object representing the semiconductive spectral
        transmittance.

        metallic_spectrum (TransmittanceSpectrum): The TransmittanceSpectrum
        object representing the metallic spectral transmittance.

    Returns
    -------
        float: The difference in transmittance at 2500 nm (Tstroke) between
        the two spectra.

    Raises
    ------
        TSolLumError: If either of the input spectra is not of type
        TransmittanceSpectrum.
    """
    # Check if semiconductive_spectrum is of type TransmittanceSpectrum
    if isinstance(semiconductive_spectrum, TransmittanceSpectrum) is False:
        msg = (f"semiconductive_spectrum is {type(semiconductive_spectrum)} "
               "but must be TransmittanceSpectrum.")
        raise TSolLumError(msg)

    # Check if metallic_spectrum is of type TransmittanceSpectrum
    if isinstance(metallic_spectrum, TransmittanceSpectrum) is False:
        msg = (f"metallic_spectrum is {type(metallic_spectrum)} "
               "but must be TransmittanceSpectrum.")
        raise TSolLumError(msg)

    # Filter out the transmittance values at 2500 nm for both spectra
    mask1 = np.logical_and(semiconductive_spectrum.wavelength == 2500, True)
    semiconductive_transmittance = semiconductive_spectrum.transmittance[mask1]

    mask2 = np.logical_and(metallic_spectrum.wavelength == 2500, True)
    metallic_transmittance = metallic_spectrum.transmittance[mask2]

    # Calculate the difference in transmittance at 2500 nm (Tstroke)
    return (semiconductive_transmittance - metallic_transmittance)[0]
