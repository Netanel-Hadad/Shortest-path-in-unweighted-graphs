"""
The file contains classes used for rendering the graph
"""

VERTEX_CIRCLE_RADIUS = 45
VERTEX_CIRCLE_COLOR = (0, 0, 0) # currently black
VERTEX_KEY_TEXT_COLOR = (255, 255, 255) # currently white
VERTEX_KEY_TEXT_SIZE = 48

# represents a vertex as a circle on the screen
class vertexObject:

    # create new vertex object
    def __init__(self, newColor, newPosition, vertexInfo):
        self.color = newColor
        self.position = newPosition
        self.vertexInfo = vertexInfo

# represent an edge as an arrow on the screen
class edgeObject:

    # create new edge object
    def __init__(self, edgeInfo, color):
        self.edgeInfo = edgeInfo
        self.color = color

class buttonObject:

    # create new button object
    def __init__(self, newText, newPosition, newColor):
        self.position = newPosition
        self.text = newText
        self.color = newColor