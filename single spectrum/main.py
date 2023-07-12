'''This program is designed for the calculation of optical characteristics for
thin film systems based on VO2. These characteristics are derived from
transmission spectra. The optical characteristics are:
    - Tlum (metallic state)
    - Tlum (semiconducting state)
    - ΔTlum
    - Tsol (metallic state)
    - Tsol (semiconducting state)
    - ΔTsol
    - ΔT@2500nm.

The structure of the header of the spectrum must be as follows:
Wavelength (nm) Transmittance (%).

The values must be separated by commas.

The simulated spectra must start at least at 200nm and end at least at 3000nm.

The spectra describing the two states of VO2 (metallic and semiconducting)
must be included in the file names. Thus, for spectra representing the
metallic state, "_me_" must be present in the file name. For the
semiconducting state correspondingly "_sc_".

Furthermore, the transmission spectra must be saved in ".txt" format.
'''
import sys

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, "./init/")

from calculation import calculate

calculate()
