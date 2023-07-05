'''
This module saves the results of the calculation of the optical parameters 
in a ".txt" file in a form with which a graphical representation is 
subsequently realised.
'''
from calculation import calculate
import pandas as pd

def order_and_save_result() -> None:
    '''
    Info
    ----
    This function calls up the calculation of the optical parameters and 
    saves them in various DataFrames in order to prepare them for 
    graphical representation.
    '''
    # Calculated data in the dictionary.
    dicts = calculate()
    
    # The keys are sorted according to the AR layer thickness specified in 
    # the file name.
    files = [key for key in sorted(dicts.keys(), key=lambda 
                                   x: int(x.split("_")[-2][:-2]))]
    
    # Takes the layer thickness and stores it as an integer in a list.
    anti_reflection_thickness = [int(string.split("nm")[0]) for file in files 
                                  for string in file.split("_") if "nm" in string]
    
    # A DataFrame is created for each optical parameter. The layer thickness 
    # of the anti-reflective layer is already specified in an unnamed column.
    result_tlum_me = pd.DataFrame({"" : anti_reflection_thickness})
    result_tlum_sc = pd.DataFrame({"" : anti_reflection_thickness})
    result_delta_tlum = pd.DataFrame({"" : anti_reflection_thickness})
    
    result_tsol_me = pd.DataFrame({"" : anti_reflection_thickness})
    result_tsol_sc = pd.DataFrame({"" : anti_reflection_thickness})
    result_delta_tsol = pd.DataFrame({"" : anti_reflection_thickness})
    
    result_t2500 = pd.DataFrame({"" : anti_reflection_thickness})
    
    # It is iterated over the sorted dictionary keys and the thickness of 
    # the anti-reflective layer.
    for file, ar_thickness in zip(files, anti_reflection_thickness):
        # The results from the dictionary with the respective layer thickness 
        # of the anti-reflective layer are extracted.
        tlum, tsol, t2500 = dicts[file]
        
        # The row index of the corresponding anti-reflective layer thickness 
        # is determined in order to insert values into the respective cell of 
        # the DataFrame later.
        row_index = result_tlum_me[result_tlum_me[""] == ar_thickness].index[0]
        
        # It is iterated over the buffer layer thickness to access the 
        # numerical results of the optical characteristics.
        for buffer_thickness in dicts[file][0]:
            # The optical characteristics are extracted from the dictionary.
            tlum_me, tlum_sc, delta_tlum = tlum[buffer_thickness]
            tsol_me, tsol_sc, delta_tsol = tsol[buffer_thickness]
            delta_t2500 = t2500[buffer_thickness]
            
            # The results of the optical parameters are inserted into 
            # the DataFrame with respect to the row index and the 
            # corresponding column.
            result_tlum_me.loc[row_index, buffer_thickness] = tlum_me
            result_tlum_sc.loc[row_index, buffer_thickness] = tlum_sc
            result_delta_tlum.loc[row_index, buffer_thickness] = delta_tlum
            
            result_tsol_me.loc[row_index, buffer_thickness] = tsol_me
            result_tsol_sc.loc[row_index, buffer_thickness] = tsol_sc
            result_delta_tsol.loc[row_index, buffer_thickness] = delta_tsol
    
            result_t2500.loc[row_index, buffer_thickness] = delta_t2500
        
    # The result maps are saved in the "output" folder.
    result_tlum_me.to_csv(".\\output\\tlum_me.txt", sep="\t", header=True, index=False)
    result_tlum_sc.to_csv(".\\output\\tlum_sc.txt", sep="\t", header=True, index=False)
    result_delta_tlum.to_csv(".\\output\\deltaTlum.txt", sep="\t", header=True, index=False)
    
    result_tsol_me.to_csv(".\\output\\tsol_me.txt", sep="\t", header=True, index=False)
    result_tsol_sc.to_csv(".\\output\\tsol_sc.txt", sep="\t", header=True, index=False)
    result_delta_tsol.to_csv(".\\output\\deltaTsol.txt", sep="\t", header=True, index=False)
    
    result_t2500.to_csv(".\\output\\deltaT2500nm.txt", sep="\t", header=True, index=False)