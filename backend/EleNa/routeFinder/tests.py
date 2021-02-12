import osmnx as ox
from django.conf import settings
import pickle as pkl
import math
import requests
import heapq
import copy
from django.test import TestCase
import pickle
from .utilities import calcStraightLineDistance, getClosestMappedNode
from .a_star import getAstarRoute, AStar, getDistanceFromTargetWithElevation, getGroundDistanceAndElevationFromTarget
from .djikstras import findShortestDistance
from .mapAccessor import Graph, Node
from .views import find_route
from django.test.client import RequestFactory
from django.test import Client



class ElenaTests(TestCase):
    def test_calcStraightLineDistance(self):
        infile = open('graph.pkl', 'rb')
        gr = pickle.load(infile)
        infile.close()
        self.assertIs(int(calcStraightLineDistance(gr.nodes[8099446119], gr.nodes[8099446119])), 0)

    def test_getClosestMappedNode(self):
        infile = open('graph.pkl', 'rb')
        gr = pickle.load(infile)
        infile.close()
        closestNode = getClosestMappedNode(gr, gr.nodes[8099446119])
        print(closestNode)
        self.assertIs(gr.nodes[8099446119].latitude, gr.nodes[closestNode].latitude)
        self.assertIs(gr.nodes[8099446119].longitude, gr.nodes[closestNode].longitude)

    def test_getGroundDistanceAndElevationFromTarget(self):
        infile = open('graph.pkl', 'rb')
        gr = pickle.load(infile)
        infile.close()
        # getGroundDistanceAndElevationFromTarget returns a tuple
        groundDistanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(gr, 8099446119)
        self.assertIs(int(groundDistanceFromTarget[8099446119]), 0)
        self.assertIs(int(elevationFromTarget[8099446119]), 0)

    def test_getDistanceFromTargetWithElevation(self):
        # self.assertIs((getDistanceFromTargetWithElevation(2,3)), math.sqrt(13))
        self.assertIs(int(getDistanceFromTargetWithElevation(2,3)), 3)

    def test_AStar_when_target_and_source_both_are_same(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 8099446119
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, target_id, 10000, 10000, 100, -100, 100)
        print(paths, target_distance, target_elevation, distances)
        self.assertIs(int(target_distance), 0)
        self.assertIs(int(target_elevation), 0)
        self.assertIs(paths[0], target_id)

    def test_AStar_when_target_and_source_same(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 0
        source_id = 0
        
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, source_id, 10000, [10000], [100], [-100], [100])
        print(paths, target_distance, target_elevation, distances)
        self.assertIs(int(target_distance), 0)
        self.assertIs(int(target_elevation), 0)

    def test_AStar_when_target_and_source_diff_for_max(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 7278370349
        source_id = 8099446119
        groundDistanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, target_id)
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, source_id, 10000, groundDistanceFromTarget, 1, True, elevationFromTarget)
        self.assertIs(int(target_distance) > 0, True)

    def test_AStar_when_target_and_source_diff_for_min(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 7278370349
        source_id = 7278370352
        groundDistanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, target_id)
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, source_id, 10000, groundDistanceFromTarget, 1, False, elevationFromTarget)
        self.assertIs(int(target_distance), 210)


    def test_getAstarRoute(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 8099446119
        source_id = 8099446119
        maximize_elevation = 10000
        distance_limit = 10000
        iters = 2
        calculatedRoute, best_elevation, best_distance = getAstarRoute(graph, source_id, target_id, maximize_elevation, distance_limit)
        self.assertIs(int(best_elevation), 0)

    def test_dijkstra_findShortestDistance_when_source_dest_same(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 8099446119
        source_id = 8099446119
        _, shortest_distance = findShortestDistance(graph, source_id, target_id)
        self.assertIs(int(shortest_distance), 0)

    def test_dijkstra_findShortestDistance_when_source_des_diff(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 7278370349
        source_id = 8099446119
        _, shortest_distance = findShortestDistance(graph, source_id, target_id)
        self.assertIs(int(shortest_distance)>5965, True)

    def test_graph_init(self):
        g = Graph()
        G = g.initiateGraph()
        self.assertIs(len(G)>0, True)

    def test_getRouteElevation(self):
        g = Graph()
        G = g.initiateGraph()
        self.assertIs(g.getRouteElevation([8099446119]), 0)

    def test_getRouteElevation(self):
        g = Graph()
        G = g.initiateGraph()
        self.assertIs(int(g.getRouteElevation([7278370346,7278370349])), int(3.25))

    def test_Node_addEdge(self):
        n = Node(1,1,1,1)
        self.assertIs(len(n.edges)>0, False)
        n.addEdge(2,2,2)
        self.assertIs(len(n.edges)>0, True)

    def test_Node_removeEdge(self):
        n = Node(1,1,1,1)
        self.assertIs(len(n.edges)>0, False)
        n.addEdge(2,2,2)
        self.assertIs(len(n.edges)>0, True)
        n.removeEdge(2)
        self.assertIs(len(n.edges)>0, False)

    def test_Node_getEdge(self):
        n = Node(1,1,1,1)
        self.assertIs(len(n.edges)>0, False)
        n.addEdge(2,2,2)
        self.assertIs(len(n.edges)>0, True)
        edge = n.getEdge(2)
        self.assertIs(edge.destination, 2)
    
    def test_find_route(self):
        data = {
            "source_latitude": 1,
            "source_longitude": 1,
            "destination_latitude": 0,
            "destination_longitude": 0,
            "percentage": 10,
            "elevation_type": "min",
            "algorithm": "a_star"
        }
        c = Client()
        response = c.post('http://localhost:4200/find_route/', data)
        self.assertEqual(response.status_code, 200)
        
