# TSolLum

TSolLum is a Python package designed to analyze the optical properties of a smart window coating material called vanadium dioxide (VO2). VO2 is utilized in smart windows due to its unique phase transition from a semiconductive state to a metallic state at a specific temperature. This property allows the smart windows to dynamically control the amount of solar radiation and heat entering a room, offering energy-efficient solutions for maintaining comfortable indoor temperatures.

## Purpose

The primary goal of this package is to provide insights into the performance of VO2 smart window coatings in different states and their effectiveness in controlling solar radiation and room temperatures. The key optical properties calculated by the package are as follows:

1. Luminous Transmittance (Tlum): Quantifies the ability of a human eye to see through the coating without distortions in both the semiconductive and metallic phases. The difference (delta) between Tlum values for the two phases provides insights into the coating's visual clarity.

2. Solar Transmittance (Tsol): Assesses how well the coating transmits solar radiation at an incident angle of 37° when in the semiconductive and metallic phases. The delta value for Tsol offers valuable information on the coating's solar energy regulation capability.

3. Transmittance Stroke (TStroke): This parameter is calculated by comparing the transmittance spectra of the coating at 2500nm, which falls within the infrared range. TStroke acts as an indicator of the effectiveness of the smart window in transitioning between the two phases and controlling infrared radiation.

# Mathematical Formlua

$$T_{lum} = \frac{\int_{380nm}^{780nm}{T(\lambda)L(\lambda)g(\lambda)} d\lambda}{\int_{380nm}^{780nm}{L(\lambda)g(\lambda)} d\lambda}$$
$T(\lambda)$ represents the simulated transmission spectrum, $L(\lambda)$ the V-Lambda curve and $g(\lambda)$ the CIE standard illuminant D65.

$$T_{sol} = \frac{\int_{200nm}^{3000nm}{T(\lambda)G(\lambda)} d\lambda}{\int_{200nm}^{3000nm}{G(\lambda)} d\lambda}$$
$T(\lambda)$ represents the simulated transmission spectrum and $G(\lambda)$ the ASTM-G-173 (Global Total Spectral Irradiance. tilt 37°)

The difference between the two states semiconducting and metallic is described as follows:
$$\Delta T_{lum, sol} = T_{lum, sol}(semiconductive) - T_{lum, sol} (metallic)$$

The difference between the two states semiconducting and metallic at a wavelength of 2500nm is called transmittance stroke:
$$\Delta T_{@2500\,nm} = T_{@2500nm}(semiconductive) - T_{@2500nm}(metallic)$$


## Installation

To install TSolLum, use the following command:
```
pip install TSolLum
```

## Input Data Format

The input data for the TSolLum package should be stored in a tab-separated TXT file. The file should contain two columns with the following headers:

    "Wavelength (nm)": This column should store the wavelength values in nanometers (nm).

    "Transmittance (%)": This column should store the corresponding transmittance values in percentage (%).

Please ensure that the input data is organized in ascending order of wavelength and covers the relevant range required for the analysis.

## Usage

```
# Import the TSolLum module for solar and luminous transmittance calculations
import TSolLum

# Read spectral data from tab-separated TXT files for the semiconductive and metallic phases
spectrum_sc = TSolLum.read("path_to_semiconductive_spectrum.txt")
spectrum_me = TSolLum.read("path_to_metallic_spectrum.txt")

# Interpolate the spectral data to fill in missing values and convert to a step size of 1nm
spectrum_sc.interpolate()
spectrum_me.interpolate()

# Calculate luminous transmittance (Tlum) for the semiconductive and metallic spectra
tlum_sc = TSolLum.calculate_tlum(spectrum=spectrum_sc)
tlum_me = TSolLum.calculate_tlum(spectrum=spectrum_me)

# Calculate solar transmittance (Tsol) for the semiconductive and metallic spectra
tsol_sc = TSolLum.calculate_tsol(spectrum=spectrum_sc)
tsol_me = TSolLum.calculate_tsol(spectrum=spectrum_me)

# Calculate the stroke temperature using the semiconductive and metallic spectra
tstroke = TSolLum.calculate_tstroke(semiconductive_spectrum=spectrum_sc,
                                    metallic_spectrum=spectrum_me)
```


## Note

- The accuracy and correctness of the calculated results depend on the implementation of the "TSolLum" module, which handles spectral data processing.
- The calculated values are based on the assumption of specific coating setups and may vary for different VO2 smart window configurations.
- The units and format of the spectral data and results are defined by the "TSolLum" module.
- This module is designed for analyzing the properties of VO2 smart window coatings and may not be applicable for other materials or applications.

## Credits

The program was implemented as part of the following projects at the Institute for Experimental Physics I of the Justus Liebig University Giessen:
- DFG "Kombi VO2" (510965362)
- BMBF "IntelVanaGlas" (03VP09691)

## Author

JoHpt

## License

MIT

## Version

0.1

## Last Updated

07/30/2023
