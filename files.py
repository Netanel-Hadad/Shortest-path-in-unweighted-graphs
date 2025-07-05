"""
This file contains the functions for saving and loading saves.
We use the file dialogs feature from tkinter.

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
import graphs
import graphics

def loadSave():
    # open the file dialog and set the path to filePath
    filePath = filedialog.askopenfilename(title="Select Save", filetypes=[("Save File",('*.sav'))])

    """
    state is used for monitoring what we are currently reading from the save file.
    0 = vertecies, 1 = edges, 2 = vertecies objects
    """
    state = 0

    # return values
    V = []
    E = []
    verteciesObjects = []

    # open the save file to read it
    with open(filePath) as file:
        for line in file:
            # handle state changes
            if line == "vertecies:\n":
                continue
            if line == "edges:\n":
                state = 1
                continue
            elif line == "vertecies objects:\n":
                state = 2
                continue

            # reading vertex
            if state == 0:
                V.append(line[:len(line)-1])
            # reading edge
            elif state == 1:
                E.append((line[1:line.find(',')], line[line.find(',')+1:len(line)-2]))
            # reading vertex object
            elif state == 2:
                verteciesObjects.append((graphics.VERTEX_CIRCLE_COLOR, (int(line[1:line.find(',')]), int(line[line.find(',')+1:line.find(')')])), line[line.find(')')+2:len(line)-1]))
    
    return (V, E, verteciesObjects)

            
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