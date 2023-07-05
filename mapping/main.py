'''
This program is intended for visualization of optical characteristics of 
multilayer systems based on VO2. Thus, variations in two layer thicknesses 
(e.g. buffer and antireflection layer) can be displayed graphically with the 
help of a contour plot.

These characteristics are derived from transmission spectra, which are 
available as a so-called "map". The optical characteristics are:
    - Tlum (metallic state)
    - Tlum (semiconducting state)
    - ΔTlum
    - Tsol (metallic state)
    - Tsol (semiconducting state)
    - ΔTsol
    - ΔT@2500nm

The imported files must have the following structure. The first column of the 
file has an empty header and contains the wavelength for which the 
transmission spectra were recorded. The following right columns contain the 
transmission values as a function of the layer thickness, which is the 
header.
        
The values must be separated by commas.

The simulated spectra must start at least at 200nm and end at least at 3000nm.

The spectra describing the two states of VO2 (metallic and semiconducting)
must be included in the file names. Thus, for spectra representing the 
metallic state, "_me_" must be present in the file name. For the 
semiconducting state correspondingly "_sc_". 

Furthermore, the transmission spectra must be saved in ".txt" format.

In addition, the second varied layer thickness must be represented with a 
string of the form "_xnm_", where x is an integer.

An example of what such a file should look like is shown here:

	0	3	6	9	12                      ...
200	4,21	4,73	5,11	5,18	4,90
202	4,05	4,55	4,93	5,03	4,79
204	3,91	4,39	4,77	4,89	4,70
206	3,80	4,26	4,63	4,78	4,62
208	3,70	4,15	4,52	4,68	4,56
210	3,63	4,06	4,42	4,60	4,51
212	3,57	3,98	4,35	4,53	4,47
214	3,53	3,93	4,29	4,49	4,45
216	3,50	3,89	4,25	4,46	4,44
218	3,49	3,88	4,23	4,45	4,45
220	3,50	3,88	4,22	4,45	4,47
...

'''
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './init/')

import warnings
# PerformanceWarning: DataFrame is highly fragmented.  This is usually the 
# result of calling `frame.insert` many times, which has poor performance.
warnings.filterwarnings("ignore")


from order_save import order_and_save_result
from plotting import plot

need_calculation = True

# Calculation and sorting is only performed if Bool is set as True.
if need_calculation == True:
    order_and_save_result()

plot()