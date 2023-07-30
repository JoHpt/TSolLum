"""spectra_reader - Module for reading TransmittanceSpectrum data from a file.

This module provides a function, read_spectrum, to read TransmittanceSpectrum
data from a file and convert it into a TransmittanceSpectrum object.

Functions:
    read_spectrum(filepath: str) -> TransmittanceSpectrum:
        Read TransmittanceSpectrum data from a file and convert it into a
        TransmittanceSpectrum object.

Parameters:
    filepath (str): The path to the file containing TransmittanceSpectrum data.

Returns:
    TransmittanceSpectrum: A TransmittanceSpectrum object containing the
    spectral data.

Raises:
    FileNotFoundError: If the specified file is not found.

    SpectrumError: If the file data is missing the required headers.

Note:
    The input file must be in TSV format with columns named 'Wavelength (nm)'
    and 'Transmittance (%)'.
"""


from io import StringIO

import pandas as pd

from .exceptions import SpectrumError
from .spectra import TransmittanceSpectrum


def read(filepath : str) -> TransmittanceSpectrum:
    """Read TransmittanceSpectrum data from a file and convert it into a
    TransmittanceSpectrum object.

    Parameters
    ----------
        filepath (str): The path to the file containing TransmittanceSpectrum
        data.

    Returns
    -------
        TransmittanceSpectrum: A TransmittanceSpectrum object containing the
        spectral data.

    Raises
    ------
        FileNotFoundError: If the specified file is not found.

        SpectrumError: If the file data is missing the required headers.
    """
    try:
        # Try to open the file specified by 'filepath'
        with open(filepath) as file:
            # Read the content of the file
            data = file.read()

            # Replace commas with dots in the data to ensure consistent decimal format
            data = data.replace(",", ".")

    except FileNotFoundError:
        # If the file is not found, raise a FileNotFoundError with a descriptive message
        msg = f"'{filepath}'"
        raise FileNotFoundError(msg)

    try:
        # Try to use pandas to read it with tab as the separator
        spectrum = pd.read_csv(StringIO(data), sep="\t")

    except Exception:
        msg = f"The spectrum '{filepath}' is not tab-seperated."
        raise SpectrumError(msg)

    # Check if the required headers are present in the data
    if "Wavelength (nm)" not in spectrum:
        # If 'Wavelength (nm)' header is missing, raise a SpectrumError with a
        # descriptive message
        msg = "There is no header named 'Wavelength (nm)'."
        raise SpectrumError(msg)
    if "Transmittance (%)" not in spectrum:
        # If 'Transmittance (%)' header is missing, raise a SpectrumError with
        # a descriptive message
        msg = "There is no header named 'Transmittance (%)'."
        raise SpectrumError(msg)

    # Create a new TransmittanceSpectrum object
    transmittance_spectrum = TransmittanceSpectrum()

    # Set the properties of the TransmittanceSpectrum object using the data
    # from the file
    transmittance_spectrum.set_properties(
        wavelength=spectrum["Wavelength (nm)"].values,
        transmittance=spectrum["Transmittance (%)"].values,
    )

    # Return the TransmittanceSpectrum object with the spectral data
    return transmittance_spectrum
