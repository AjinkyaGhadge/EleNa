import math

def getClosestMappedNode(graph, source):
    closestNode = None
    minDistance = math.inf
    for osmid in graph.nodes:
        node = graph.nodes[osmid]
        distance = calcStraightLineDistance(source, node)
        if distance < minDistance:
            minDistance = distance
            closestNode = node.osmid
    return closestNode

def calcStraightLineDistance(source, destination):
    return math.sqrt( math.pow((destination.latitude - source.latitude),2) + math.pow((destination.longitude - source.longitude),2))
