"""
This file contains different functions for different tasks
"""

# find a vertex in a graph by its key value
def findVertexByKey(G, k):
    for v in G.V:
        if v.key == k:
            return v