# Import System Struct Objects

# Import Models
from typing import List

from Models.Gats import Gats
from Models.Graph import Graph
from Tests.GatsGraph import GatsGraph
from Tests.AGatsGraph import AGats

# Import Utility Functions
from Services.ExtractProvDataService import get_tree_from_file_path
from Services.ExtractProvDataService import get_tree_vertices_dictionary
from Services.ExtractProvDataService import get_tree_edges_dictionary
from Services.ExtractProvDataService import filter_edge_dict_by_type_and_label
from Services.ExtractProvDataService import add_edges_to_graph

# Import Utility Constants
from Utils.UtilitiesTestFilePathConstants import UtilitiesTestFilePathConstants

# Constants
ACTIVITY: str = 'Activity'


class LeituraManipulacaoDadosT:
    def __init__(self):
        self.gats: Gats = Gats()

    @staticmethod
    def __read_session(path: str, graph: Graph, file_name: str):
        tree = get_tree_from_file_path(path)
        vertex_dictionary = get_tree_vertices_dictionary(tree)
        edge_dictionary = get_tree_edges_dictionary(tree, vertex_dictionary)
        edge_dictionary_filtered = filter_edge_dict_by_type_and_label(edge_dictionary, ACTIVITY)
        add_edges_to_graph(edge_dictionary_filtered, graph, file_name)

    def __create_gats(self, path: str, file_name: str, loop: int):
        self.__read_session(path, self.gats.graph_gats, file_name)
        session_gats = self.gats
        gats_graph = GatsGraph()

        """return gats_graph.create_gats_graph(session_gats, file_name, loop, True)"""
        return gats_graph.create_gats_graph(session_gats, file_name, loop, False)

    def __add_gats_to_agats(self, gats_list: List[GatsGraph], path: str, file_name: str, loop: int):
        gats_graph = self.__create_gats(path, file_name, loop)
        gats_list.append(gats_graph)
        self.gats.graph_gats.empty_lists()

    def __create_agats(self):
        gats_list: List[GatsGraph] = []
        self.__add_gats_to_agats(gats_list, UtilitiesTestFilePathConstants.NAMED_AREA_PATH_01, 'Single Gats Test 01', 1)
        self.__add_gats_to_agats(gats_list, UtilitiesTestFilePathConstants.NAMED_AREA_PATH_02, 'Single Gats Test 02', 2)
        self.__add_gats_to_agats(gats_list, UtilitiesTestFilePathConstants.NAMED_AREA_PATH_03, 'Single Gats Test 03', 3)

        agats_graph = AGats()
        agats_graph.create_agats(gats_list, 'AGats Test 01')
        agats_graph.print_agats()

    def main(self):
        self.__create_agats()


'''End of Class'''
