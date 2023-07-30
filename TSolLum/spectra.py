"""spectra.py - Module for loading, visualizing and working with Spectra data.

This module contains classes and functions to visualize and manipulate
spectral data, such as transmittance spectra, CIE Standard Illuminant D65,
spectral sensitivity of the human eye (V-lambda), and ASTM G-173 Global Total
Spectral Irradiance.

Classes:
    TransmittanceSpectrum:
        A class to represent transmittance spectra. It provides methods to
        set the wavelength and transmittance data, visualize the spectrum, and
        interpolate missing values.

    D65:
        A class representing the CIE Standard Illuminant D65. It provides a
        method to visualize the D65 data.

    VLambda:
        A class representing the spectral sensitivity of the human eye
        (V-lambda). It provides a method to visualize the V-lambda data.

    ASTM_G_173:
        A class representing ASTM G-173 Global Total Spectral Irradiance.
        It provides a method to visualize the G-173 data.
"""


import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class TransmittanceSpectrum:
    """Class for representing a transmittance spectrum.

    Attributes
    ----------
        wavelength (np.ndarray): np.ndarray to store the wavelengths.
        transmittance (np.ndarray): np.ndarray to store the transmittance values.

    Methods
    -------
        __init__(self): Initializes empty lists for wavelength and transmittance.

        __str__(self): Returns a formatted string representation of the spectrum data.

        set_properties(self, wavelength, transmittance): Sets the wavelength and
        transmittance data.

        show(self): Plots and displays the transmittance spectrum.

        interpolate(self): Interpolates the spectrum data to fill missing values.
    """

    def __init__(self) -> None:
        """Initializes an empty TransmittanceSpectrum object."""
        self.wavelength = np.array([])
        self.transmittance = np.array([])

    def __str__(self) -> str:
        """Returns a formatted string representation of the spectrum data.

        Returns
        -------
            str: Formatted string representing the wavelength and transmittance data.
        """
        return (f"Wavelength\n"
                f"----------\n"
                f"{self.wavelength[0]}, "
                f"{self.wavelength[1]}, "
                f"{self.wavelength[2]} ... "
                f"{self.wavelength[-3]}, "
                f"{self.wavelength[-2]}, "
                f"{self.wavelength[-1]}\n"
                f"\n"
                f"Transmittance\n"
                f"-------------\n"
                f"{self.transmittance[0]}, "
                f"{self.transmittance[1]}, "
                f"{self.transmittance[2]} ... "
                f"{self.transmittance[-3]}, "
                f"{self.transmittance[-2]}, "
                f"{self.transmittance[-1]}"
                f"\n")

    def set_properties(self,
                       wavelength : np.ndarray,
                       transmittance : np.ndarray) -> None:
        """Sets the wavelength and transmittance data.

        Args:
        ----
            wavelength (np.ndarray): List of wavelength values.

            transmittance (np.ndarray): List of transmittance values.

        Returns:
        -------
            None
        """
        # Check if wavelength is of type numpy.ndarray
        if isinstance(wavelength, np.ndarray) is False:
            msg = (f"wavelength is {type(wavelength)} "
                   "but must be np.ndarray.")
            raise TypeError(msg)
        # Check if transmittance is of type numpy.ndarray
        if isinstance(transmittance, np.ndarray) is False:
            msg = (f"transmittance is {type(transmittance)} "
                   "but must be np.ndarray.")
            raise TypeError(msg)

        if len(wavelength) != len(transmittance):
            msg = (f"len(wavelength) ({len(wavelength)}) and len(transmittance)"
                   "({len(transmittance)}) are not the same.")
            raise ValueError(msg)

        self.wavelength = wavelength
        self.transmittance = transmittance

    def show(self) -> None:
        """Plots and displays the transmittance spectrum.

        Returns
        -------
            None
        """
        plt.plot(self.wavelength,
                 self.transmittance,
                 label="Spectrum")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Transmittance (%)")
        plt.legend()
        plt.show()
        plt.close()

    def interpolate(self) -> None:
        """Interpolates the spectrum data to fill missing values.

        Returns
        -------
            None
        """
        # Get the starting wavelength value
        start = int(self.wavelength[0])
        # Get the ending wavelength value
        end = int(self.wavelength[-1])
        # Calculate the number of steps between start and end
        steps = end - start + 1

        # Create an interpolating function
        interp = interp1d(self.wavelength, self.transmittance)

        # Interpolate the data to fill missing values
        self.wavelength = np.linspace(start, end, steps, dtype=int)
        self.transmittance = interp(self.wavelength)

class D65:
    """Class for representing the CIE Standard Illuminant D65.

    Attributes
    ----------
        wavelength (numpy.ndarray): Array of wavelength values.

        csi (numpy.ndarray): Array of CIE Standard Illuminant D65 values.

    Methods
    -------
        show(cls): Plots and displays the CIE Standard Illuminant D65 data.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "D65")

    wavelength = pd.read_csv(
        file_path, sep="\t")["Wavelength (nm)"].values
    csi = pd.read_csv(
        file_path, sep="\t")["CIE Standard Illuminant D65"].values

    @classmethod
    def show(cls) -> None:
        """Plots and displays the CIE Standard Illuminant D65 data.

        Returns
        -------
            None
        """
        plt.plot(cls.wavelength,
                 cls.csi)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("CIE Standard Illuminant D65")
        plt.show()
        plt.close()

class VLambda:
    """Class for representing the spectral sensitivity of the human eye (V-lambda).

    Attributes
    ----------
        wavelength (numpy.ndarray): Array of wavelength values.

        spectral_sensitivity (numpy.ndarray): Array of spectral sensitivity values.

    Methods
    -------
        show(cls): Plots and displays the spectral sensitivity of the human eye
        data (V-lambda).
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "v-lambda")

    wavelength = pd.read_csv(
        file_path, sep="\t")["Wavelength (nm)"].values
    spectral_sensistivity = pd.read_csv(
        file_path, sep="\t")["spectral sensistivity"].values

    @classmethod
    def show(cls) -> None:
        """Plots and displays the spectral sensitivity of the human eye data (V-lambda).

        Returns
        -------
            None
        """
        plt.plot(cls.wavelength,
                 cls.spectral_sensistivity)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("spectral sensistivity of the human eye")
        plt.show()
        plt.close()

class ASTM_G_173:
    """Class for representing ASTM G-173 Global Total Spectral Irradiance.

    Attributes
    ----------
        wavelength (numpy.ndarray): Array of wavelength values.

        spectral_irradiance (numpy.ndarray): Array of Global Total Spectral
        Irradiance values.

    Methods
    -------
        show(cls): Plots and displays the ASTM G-173 Global Total Spectral
        Irradiance data.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "astm_g_173")

    wavelength = pd.read_csv(
        file_path, sep="\t")["Wavelength (nm)"].values
    spectral_irradiance = pd.read_csv(
        file_path, sep="\t")["Global Total Spectral Irradiance. tilt 37Deg"].values

    @classmethod
    def show(cls) -> None:
        """Plots and displays the ASTM G-173 Global Total Spectral Irradiance data.

        Returns
        -------
            None
        """
        plt.plot(cls.wavelength,
                 cls.spectral_irradiance)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Global Total Spectral Irradiance. tilt 37Deg")
        plt.show()
        plt.close()
