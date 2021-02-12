from mapAccessor import Graph, Node
from a_star import getAstarRoute
from djikstras import findShortestDistance
import random
import matplotlib.pyplot as plt
import numpy as np

def plot():
    G = Graph()
    shortestDistanceElevations = []
    aStarMinElevations = []
    aStarMaxElevations = []

    for i in range (40):
        print(i)
        sourceTargetPair = random.sample(G.nodes.keys(), 2)
        source = sourceTargetPair[0]
        target = sourceTargetPair[1]
        shortestDistancePath, shortestDistance = findShortestDistance(G, source, target)
        shortestDistancePathElevation = G.getRouteElevation(shortestDistancePath)
        shortestDistanceElevations.append(shortestDistancePathElevation)
        _, maxAstarElevation, _ = getAstarRoute(G, source, target, True, (1.5 * shortestDistance))
        aStarMaxElevations.append(maxAstarElevation)
        _, minAstarElevation, _ = getAstarRoute(G, source, target, False, (1.5 * shortestDistance))
        aStarMinElevations.append(minAstarElevation)
    x = np.arange(40)
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(x, aStarMinElevations, label='Min Elevation')
    ax.plot(x, shortestDistanceElevations, label='Shortest Route Elevation')
    ax.plot(x, aStarMaxElevations, label='Max Elevations')
    plt.title('Route elevation comparison')
    ax.legend()
    plt.show()


plot()