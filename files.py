"""
This file contains the functions for saving and loading saves.
Save files format is '.sav'
A .sav file content looks like this:
--- save1.sav ---
vertecies:
(all vertecies info in diffrent lines)
edge:
(all edges info in diffrent lines)
vertecoes objects:
(all vertecies objects info in diffrent lines)
-----------------
"""

import tkinter as tk
from tkinter import filedialog

def loadSave():
    # open the file dialog and set the path to filePath
    filePath = filedialog.askopenfilename(title="Select Save", filetypes=[("Save File",('*.sav'))])

def saveFile(G, verteciesObjects, edgesObjects):
    # open the file dialog and set the path to filePath
    filePath = filedialog.asksaveasfilename(title="Save As", defaultextension=".sav", filetypes=[("Save File", "*.sav")])

    if filePath:
        try:
            with open(filePath, 'w') as file:

                file.write("vertecies:\n")
                for v in G.V:
                    file.write(str(v) + '\n')

                file.write("edges:\n")
                for e in G.E:
                    file.write(str(e) + '\n')

                file.write("vertecies objects:\n")
                for o in verteciesObjects:
                    file.write(str(o.position) + "," + str(o.vertexInfo) + "\n")

            print(f"File saved successfully at: {filePath}")
        except Exception as e:
            print(f"Error saving file: {e}")