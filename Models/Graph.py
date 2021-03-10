from typing import Dict, List

from Models.GraphVertex import GraphVertex
from Models.GraphEdge import GraphEdge


class Graph:
    def __init__(self):
        self.edges: Dict[str, GraphEdge] = {}
        self.vertices: Dict[str, GraphVertex] = {}
        self.newEdgeElements: List[str] = []
        self.newVertexElements: List[str] = []
        self.vertices_to_node: Dict[int, str] = {}

    def add_edge(self, source_vertex_region: str, target_vertex_region: str,
                 file_name: str, is_edge_respawn: bool):
        key_value: str = source_vertex_region + '_' + target_vertex_region
        if key_value in self.edges:
            edge = self.edges.get(key_value)
            edge.frequency += 1
            edge.sessions.append(file_name)
        else:
            source = self.__add_vertex(source_vertex_region, self.vertices)
            target = self.__add_vertex(target_vertex_region, self.vertices)
            edge = GraphEdge(source, target, file_name, is_edge_respawn)
            self.edges[key_value] = edge
            self.newEdgeElements.append(key_value)

    def __add_vertex(self, region: str, dictionary_vertex: Dict[str, GraphVertex]):
        if not (region in dictionary_vertex):
            vertex = GraphVertex(region)
            dictionary_vertex[region] = vertex
            self.newVertexElements.append(region)
            return vertex
        else:
            return dictionary_vertex[region]

    def get_edges(self):
        return self.edges

    def empty_lists(self):
        self.newEdgeElements = []
        self.newVertexElements = []

    def add_id_to_vertex(self):
        id_vertex: int = 1
        for region in self.vertices:
            self.vertices_to_node[id_vertex] = region
            id_vertex += 1

    def add_edge_from_file(self, source_vertex_region: str, target_vertex_region: str,
                           file_name: str, is_edge_respawn: bool, edge_frequency: int):

        key_value: str = source_vertex_region + '_' + target_vertex_region
        source = self.__add_vertex(source_vertex_region, self.vertices)
        target = self.__add_vertex(target_vertex_region, self.vertices)
        edge = GraphEdge(source, target, file_name, is_edge_respawn)
        edge.frequency = edge_frequency
        edge.sessions.append(file_name)
        self.edges[key_value] = edge
        self.newEdgeElements.append(key_value)

