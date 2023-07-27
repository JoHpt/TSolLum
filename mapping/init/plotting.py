"""This module graphically displays the results of the optical characteristics."""
import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot() -> None:
    """Info
    ----
    The results are displayed graphically and labels and titles are defined
    in the plot.
    """
    # The result maps are read in with the help of glob().
    files = glob.glob(".\\output\\*.txt")

    # The titles of the plots are associated with the file names so
    # that the correct headings are added.
    titles = {
        ".\\output\\deltaT2500nm.txt" : "\u0394T@2500nm",
        ".\\output\\deltaTlum.txt" : "\u0394Tlum",
        ".\\output\\deltaTsol.txt" : "\u0394Tsol",
        ".\\output\\tlum_me.txt" : "Tlum Me",
        ".\\output\\tlum_sc.txt" : "Tlum Sc",
        ".\\output\\tsol_me.txt" : "Tsol Me",
        ".\\output\\tsol_sc.txt" : "Tsol Sc"}

    # It is iterated over the files.
    for file in files:
        data = pd.read_csv(file, sep="\t")

        # The anti-reflective coating thicknesses are specified in a list.
        ar_thickness = [float(x) for x in list(data)[1:]]
        # The same for the buffer layer thickness.
        buffer_thickness = list(data["Unnamed: 0"])

        # The axes are set and a grid for the plot is defined.
        x = buffer_thickness
        y = ar_thickness
        X, Y = np.meshgrid(x, y)

        # The meshgrid is converted to a list.
        X = X.tolist()
        Y = Y.tolist()
        # The Z data is extracted from the DataFrame and added to a list.
        Z = np.transpose(data.drop("Unnamed: 0", axis=1).values).tolist()
        

        # The actual graphing is done and the specifications of the
        # plot are determined.
        plt.contourf(X, Y, Z, cmap="turbo", levels=50)
        plt.colorbar(label="%")
        plt.title(titles[file])
        plt.ylabel("Anti-reflection layer thickness / nm")
        plt.xlabel("Buffer thickness / nm")

        # The plot is saved in the "output" folder.
        data_name = file.split("\\")[-1].split(".")[0]
        plt.savefig(f".\\output\\{data_name}.png", dpi=300)
        plt.close()
