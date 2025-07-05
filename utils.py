def findVertexByKey(G, k):
    for v in G.V:
        if v.key == k:
            return v