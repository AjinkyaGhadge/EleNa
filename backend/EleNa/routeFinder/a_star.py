import math
import heapq


# Returns actual distance between 2 points factoring in co-ordinate distance as well as elevation difference
def getDistanceFromTargetWithElevation(groundDistance, elevationDiff):
	return math.sqrt(math.pow(groundDistance,2) + math.pow(elevationDiff,2))

# Creates memoized dictionaries for distances and elevation differences between all graph nodes and selected destination node
def getGroundDistanceAndElevationFromTarget(graph, target):
	elevationFromTarget = {}
	groundDistanceFromTarget = {}
	for osmid in graph.nodes:
		currentNode = graph.nodes[osmid]
		elevationFromTarget[osmid] = graph.nodes[target].elevation - currentNode.elevation
		groundDistanceFromTarget[osmid] = math.sqrt(math.pow((currentNode.latitude - graph.nodes[target].latitude), 2)
												+ math.pow((currentNode.longitude - graph.nodes[target].longitude), 2))
	return groundDistanceFromTarget, elevationFromTarget

# Performs 1 iteration of A star search based on provided source-target-weight values
def AStar(graph, source, target, permissableDistance, distanceFromTarget, weight, maximize_elevation, elevationFromTarget):
	relativeElevationFromSource = {}
	routeDistanceFromSource = {}
	heuristicScores = {}
	predecessors = {}
	visited = set()
	heuristicScores[source] = 0
	heap = [(0, source)]
	relativeElevationFromSource[source] = 0
	routeDistanceFromSource[source] = 0
	
	while (len(heap) > 0):
		_, currentNode = heapq.heappop(heap)
		if currentNode == target: 
			break

		if currentNode in visited: 
			continue
		
		visited.add(currentNode)
		currentNodeEdges = graph.nodes[currentNode].edges
		for edge in currentNodeEdges:
			
			nextNode = edge.destination
			if nextNode in visited: 
				continue
			
			# Calculating and storing relative Distances and elevations of neighbor node in question
			nextNodeRouteDistance = edge.length + routeDistanceFromSource[currentNode]
			nextNodeRelElevation = edge.elevationGain + relativeElevationFromSource[currentNode]
			predecessors[nextNode] = currentNode
			routeDistanceFromSource[nextNode] = nextNodeRouteDistance
			relativeElevationFromSource[nextNode] = nextNodeRelElevation

			# Calculating heuristic score value based on circumstances
			if not maximize_elevation:
				heuristicScore = nextNodeRelElevation + weight * distanceFromTarget[nextNode]
				if heuristicScore < heuristicScores.get(nextNode, math.inf):
					heuristicScores[nextNode] = heuristicScore
					heapq.heappush(heap, (heuristicScore, nextNode))
			
			else:
				heuristicScore = nextNodeRouteDistance + nextNodeRelElevation - weight * getDistanceFromTargetWithElevation(distanceFromTarget[nextNode], elevationFromTarget[nextNode])
				if heuristicScore > heuristicScores.get(nextNode, -math.inf):
					heuristicScores[nextNode] = heuristicScore
					heapq.heappush(heap, (-heuristicScore, nextNode))

			
	# Backtracking across accepted nodes and constructing the correct route
	route = []
	currentRouteNode = target
	while (currentRouteNode != source):
		route.append(currentRouteNode)
		currentRouteNode = predecessors[currentRouteNode]
	route.append(source)
	return route[::-1], routeDistanceFromSource[target], graph.getRouteElevation(route[::-1]), routeDistanceFromSource[target] <= permissableDistance

def getAstarRoute(graph, source, target, maximize_elevation, permissableDistance):
	# Establishing no. of A* iterations to be performed
	totalIterations = 35
	distanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, target)
	i, low, high = 0, 0, 1000000
	bestRouteElevation = 0 if maximize_elevation else math.inf
	bestRoute = None
	bestRouteDistance = None
	secondBestRoute = None
	secondBestDistance = None
	secondBestElevation = None
	closestToLimit = math.inf
		
	while (i < totalIterations):
		weight = (high + low)/2
		route, distance, elevation, validRoute  = AStar(graph, source, target, permissableDistance, distanceFromTarget, weight, maximize_elevation, elevationFromTarget)
		
		# Finding the route closest to distance limit in case no other route within distance limit can be found
		if (distance - permissableDistance) < closestToLimit:
			secondBestRoute = route
			secondBestDistance = distance
			secondBestElevation = elevation
			closestToLimit = distance - permissableDistance

		# Setting calculated metrics and adjusting optimization weight based on previous iteration and requirements
		if maximize_elevation and validRoute and bestRouteElevation < elevation:
			bestRoute, bestRouteDistance, bestRouteElevation = route, distance, elevation
			high = weight
		elif not maximize_elevation and validRoute and bestRouteElevation > elevation:
			bestRoute, bestRouteDistance, bestRouteElevation = route, distance, elevation
			high = weight
		
		if not validRoute:
			low = weight			

		i += 1
	
	# Setting metrics to backup values since no valid route could be found
	if bestRoute == None:
		bestRoute, bestRouteDistance, bestRouteElevation = secondBestRoute, secondBestDistance, secondBestElevation

	# Constructing route by converting node IDs to their latitudes and longitudes
	calculatedRoute = []
	for osmid in bestRoute:
		node = graph.G.nodes[osmid]
		calculatedRoute.append([node['y'], node['x']])
	return calculatedRoute, bestRouteElevation, bestRouteDistance




