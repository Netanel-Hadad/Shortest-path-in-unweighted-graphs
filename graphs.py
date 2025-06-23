"""
This file contains all the classes related to the graphs
such as edge, vertex and graph
Contaions also the BFS algorithm function
"""

import heapq
import math

# vertex with a unique key
class Vertex:
    # key is a unique value for identifying the vertex

    # defualt creation of a new vertex gives it a key value of zero
    def __init__(self):
        self.key = "default"
        self.edges = set()

    # create a new vertex with given a key value
    def __init__(self, key):
        self.key = key
        self.edges = set()

    # returns the vertex info as a string
    def __str__(self):
        return self.key
    
    # add a new edge to the list of edges starting from this vertex
    def add_edge(self, e):
        self.edges.add(e)

# non directed edge from vertex x to vertex y with a
class Edge:

    # create a new edge with keys for start and end vertices, and a weight
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # returns the edge info as a string
    def __str__(self):
        return "(%s,%s)" % (self.start, self.end)

# directed graph with a vertex set V and an edges set E
class Graph:
    # V is the vertices list
    # E is the edges list

    # create an empty graph
    def __init__(self):
        self.V = set()
        self.E = set()

    # add an existing vertex to the graph
    def add_vertex(self, v):
        self.V.add(v)

    # add an existing edge to the graph
    def add_edge(self, e):
        self.E.add(e)
        # add the new edge to its starting vertex edges list,
        #   we assume that vertex exist.
        for v in self.V:
            if v.key is e.start.key:
                v.add_edge(e)
            elif v.key is e.end.key:
                v.add_edge(Edge(e.end, e.start))

    # remove an existing edge from the graph
    def remove_edge(self, e):
        # remove the edge from its vertex edges list
        e.start.edges.remove(e)
        e.end.edges.remove(e)
        # remove the edge from the graph
        self.E.remove(e)

# run Breadth First Search on a given graph G from a given source vertex s
# return a list of info objects for each vertex in G
# in info we will store a vertex shortest distance from s, if we visited this vertex during the BFS
# and from what vertex we reached the current vertex
def BFS(G, s):

    # vertex info, its distance from the source and if we visited it already during the BFS
    # used for storing this data to be used during the BFS
    # and to return a list as the BFS result
    class info:
        v = None
        previous = None
        dist = float()
        visited = False

        def __init__(self, v, dist, visited):
            self.v = v
            self.dist = dist
            self.visited = visited

    # create a list of all vertecies and their BFS related information
    infoList = []
    for v in G.V:
        if v.key is s.key:
            infoList.append(info(v, 0, True))
        else:
            infoList.append(info(v, float('inf'), False))

    queue = []
    queue.append(s)

    # BFS loop
    while queue:
        s = queue.pop(0)

        # find the current vertex info
        for i in infoList:
            if i.v.key is s.key:
                si = i 

        for e in s.edges:
            # find vertex info
            for i in infoList:
                if i.v.key is e.end.key:
                    end = i
            # check if we visited the vertex already, if no visit
            if end.visited is False or end.dist > (si.dist + 1):
                queue.append(e.end)
                end.visited = True
                end.dist = si.dist + 1
                end.previous = s

    return infoList