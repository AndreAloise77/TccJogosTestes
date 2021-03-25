from typing import Dict, List

# Import Utilities
import Utils.UtilitiesProvConstants
from Interface.GraphVizInterface import GraphVizInterface
# Constants
from Models.Graph.GraphEdge import GraphEdge
from Models.Graph.GraphVertex import GraphVertex
from Models.Provenience.ProvEdge import ProvEdge
from Models.Provenience.ProvVertex import ProvVertex

UTILITIES_CONSTANTS = Utils.UtilitiesProvConstants.UtilitiesProvConstants
UNDERSCORE: str = '_'


class Graph(GraphVizInterface):
    def __init__(self):
        self.edges: Dict[str, GraphEdge] = {}
        self.vertices: Dict[str, GraphVertex] = {}
        self.newEdgeElements: List[str] = []
        self.newVertexElements: List[str] = []
        self.vertices_to_node: Dict[int, str] = {}

    def add_edges_to_graph(self, dict_edge: Dict[str, ProvEdge], file_name: str):
        for key_dict in dict_edge:
            edge = dict_edge[key_dict]
            self.__try_add_edge_to_graph(edge, file_name)

    def __try_add_edge_to_graph(self, edge: ProvEdge, file_name: str):
        source_vertex = edge.source_vertex_id
        source_region = self.__get_region_from_vertex(source_vertex)
        source_label = source_vertex.label_element

        target_vertex = edge.target_vertex_id
        target_region = self.__get_region_from_vertex(target_vertex)
        target_label = target_vertex.label_element

        has_valid_source_region: bool = source_region is not None
        has_valid_target_region: bool = target_region is not None
        has_valid_regions: bool = has_valid_source_region and has_valid_target_region

        if has_valid_regions and (source_region != target_region):
            if source_label != target_label and \
                    (target_label == UTILITIES_CONSTANTS.RESPAWN or source_label == UTILITIES_CONSTANTS.RESPAWN):
                self.__add_edge(target_region, source_region, file_name, True)
            else:
                self.__add_edge(target_region, source_region, file_name, False)

    @staticmethod
    def __get_region_from_vertex(vertex: ProvVertex) -> str:
        region: str = ''
        for attribute in vertex.attributes:
            attribute_name: str = attribute.attribute_name
            if attribute_name == UTILITIES_CONSTANTS.REGION:
                region = attribute.attribute_value
        return region

    def __add_edge(self, source_vertex_region: str, target_vertex_region: str,
                   file_name: str, is_edge_respawn: bool):
        key_value: str = source_vertex_region + UNDERSCORE + target_vertex_region
        if key_value in self.edges:
            edge: GraphEdge = self.edges.get(key_value)
            edge.frequency += 1
            edge.sessions.append(file_name)
        else:
            source: GraphVertex = self.__add_vertex(source_vertex_region, self.vertices)
            target: GraphVertex = self.__add_vertex(target_vertex_region, self.vertices)

            edge: GraphEdge = GraphEdge(source, target, file_name, is_edge_respawn)
            self.edges[key_value] = edge
            self.newEdgeElements.append(key_value)

    def __add_vertex(self, region: str, dictionary_vertex: Dict[str, GraphVertex]):
        if not (region in dictionary_vertex):
            vertex: GraphVertex = GraphVertex(region)
            dictionary_vertex[region] = vertex
            self.newVertexElements.append(region)
            return vertex
        else:
            return dictionary_vertex[region]

    def get_edges(self) -> Dict[str, GraphEdge]:
        return self.edges

    def empty_lists(self):
        self.newEdgeElements = []
        self.newVertexElements = []

    def empty_graph(self):
        self.edges = {}
        self.vertices = {}

    def add_id_to_vertex(self):
        id_vertex: int = 1
        for region in self.vertices:
            self.vertices_to_node[id_vertex] = region
            id_vertex += 1

    def add_edge_from_file(self, source_vertex_region: str, target_vertex_region: str,
                           file_name: str, is_edge_respawn: bool, edge_frequency: int):

        key_value: str = source_vertex_region + UNDERSCORE + target_vertex_region
        source: GraphVertex = self.__add_vertex(source_vertex_region, self.vertices)
        target: GraphVertex = self.__add_vertex(target_vertex_region, self.vertices)

        edge: GraphEdge = GraphEdge(source, target, file_name, is_edge_respawn)
        edge.frequency = edge_frequency
        edge.sessions.append(file_name)

        self.edges[key_value] = edge
        self.newEdgeElements.append(key_value)
