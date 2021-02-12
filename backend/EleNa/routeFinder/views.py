from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph, Node
import heapq
import math
from django.http import HttpResponse
import json
from .a_star import getAstarRoute
from .djikstras import findShortestDistance
from .utilities import getClosestMappedNode 

# initializing graph from osmnx
G = Graph()

@csrf_exempt
def find_route(request):
	try:
		request = json.loads(request.body.decode("utf-8"))
	except:
		request = {
            "source_latitude": 1,
            "source_longitude": 1,
            "destination_latitude": 0,
            "destination_longitude": 0,
            "percentage": 10,
            "elevation_type": "min",
            "algorithm": "a_star"
        }
		pass
	
	# Extracting request parameters
	sourceLatitude = float(request["source_latitude"])
	sourceLongitude = float(request["source_longitude"])   
	destinationLatitude = float(request["destination_latitude"])
	destinationLongitude = float(request["destination_longitude"])
	percentage = int(request["percentage"])
	elevationType = request["elevation_type"]
	algorithm = request["algorithm"]

	# Creating nodes out of received parameters
	source = Node(sourceLatitude, sourceLongitude, None, None)
	destination = Node(destinationLatitude, destinationLongitude, None, None)

	if elevationType == 'max':
		maximizeElevationGain = True
	else:
		maximizeElevationGain = False
	
	# Finding the mapped node closest to user's click location
	closestSource = getClosestMappedNode(G, source)
	closestDestination = getClosestMappedNode(G, destination)

	# Retrieving djikstra's shortest distance 
	_ , shortest_distance = findShortestDistance(G, closestSource, closestDestination)
	data = dict()
	data['shortest_distance'] = shortest_distance 
	data['route'], data['elevation'], data['distance'] = selectAlgorithm(algorithm, source, destination, maximizeElevationGain, percentage, G, shortest_distance, closestSource, closestDestination)
	
	return HttpResponse(json.dumps(data))

# Switch handler in case of future expansion to different algorithms 
def selectAlgorithm(algorithm, source, destination, maximizeElevationGain, percentage, G, shortest_distance, closestSource, closestDestination):
	if algorithm == "a_star":
		permissableDistance = (1 + (percentage/100))*shortest_distance
		return getAstarRoute(G, closestSource, closestDestination, maximizeElevationGain, permissableDistance)

