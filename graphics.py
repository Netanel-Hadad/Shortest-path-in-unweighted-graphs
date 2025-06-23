"""
The file contains classes used for rendering the graph
"""

import graphs
import pygame
import math

# represents a vertex as a circle on the screen
class vertexObject:

    # create new vertex object
    def __init__(self, newColor, newPosition, newRadius, vertexInfo):
        self.color = newColor
        self.position = newPosition
        self.radius = newRadius
        self.vertexInfo = vertexInfo

# represent an edge as an arrow on the screen
class edgeObject:

    # create new edge object
    def __init__(self, edgeInfo, color):
        self.edgeInfo = edgeInfo
        self.color = color