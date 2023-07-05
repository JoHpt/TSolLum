# Introduction

This spectra analysis program is designed to analyze simulated transmission spectra and saves
the results in form of optical parameters like Tlum(Me), Tlum(Sc), Tsol(Me), Tsol(Sc), ΔTlum,
ΔTsol and ΔT@2500nm. It also plots those optical parameters in respect to the given layer thicknesses.

# Mathematical Formlua

$$T_{lum} = \frac{\int_{380\,nm}^{780\,nm}{T(\lambda)L(\lambda)g(\lambda)} d\lambda}{\int_{380\,nm}^{780\,nm}{L(\lambda)g(\lambda)} d\lambda}$$
$T(\lambda)$ represents the simulated transmission spectrum, $L(\lambda)$ the V-Lambda curve and $g(\lambda)$ the CIE standard illuminant D65.

$$T_{sol} = \frac{\int_{200\,nm}^{3000\,nm}{T(\lambda)G(\lambda)} d\lambda}{\int_{200\,nm}^{3000\,nm}{G(\lambda)} d\lambda}$$
$T(\lambda)$ represents the simulated transmission spectrum and $G(\lambda)$ the ASTM-G-173 (Global Total Spectral Irradiance. tilt 37°)

$$\Delta T_{lum, sol} = T_{lum, sol}(semiconductive) - T_{lum, sol} (metallic)\\$$
$$\Delta T_{@2500\,nm} = T_{@2500\,nm}(semiconductive) - T_{@2500\,nm}(metallic)\\$$

# Requirements

- pandas
- numpy
- scipy
- matplotlib

# Installation

1.	Ensure that Python is installed on your system by running python -V in the command line.
2.	Install the required packages by running the following statements in the command line:
- pip install pandas
- pip install numpy
- pip install scipy
- pip install matplotlib

# Usage

1.	Choose the appropriate folder. "mapping" is for the analysis of layer systems where two layer thicknesses have been varied (e.g. buffer and anti-reflective layer). "single spectrum" is for the calculation of one layer system.
2.	Put your simulated spectra into the " input_spectra" folder. The spectra must have the following structure:
	- The .txt file name must contain the state of the VO2 (“_me_“ or “_sc_“ for metallic or semiconductive).
  b.	The first column must represent the wavelength.
  c.	The decimal values are marked with comma.
  d.	For mapping:
    i.	The .txt file name must contain the first/second thickness that was varied just for mapping.
    ii.	The first row of the table must contain the first/second thickness that was varied.
4.	Run the program.
5.	The calculated results will be saved in the "output" folder.
6.	The plots generated by the program will be saved in the " output " folder. The plots are generated automatically

# Note

For more information, such as naming the input spectra or structure of the mapping spectra, see docstrings of the main.py files.

# Credits

The program was implemented as part of the following projects at the Institute for Experimental Physics I of the Justus Liebig University Giessen:
- DFG "Kombi VO2" (510965362)
- BMBF "IntelVanaGlas" (03VP09691)

