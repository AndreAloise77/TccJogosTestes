# Import System Objects
from datetime import datetime
from typing import List
import os

# Import Models
from Models.Gats import Gats
from Models.Graph import Graph
from Tests.GatsGraph import GatsGraph
from Tests.AGatsGraph import AGats

# Import Service
import Services.ExtractProvDataService
import Services.GatsService

# Import Utility Constants
import Utils.UtilitiesIO

# Constants
ACTIVITY: str = 'Activity'
DATE_FORMAT: str = '%Y-%m-%d_%H-%M-%S'
PROV_FILES_DIRECTORY: str = 'Files/ProvFiles'
INVALID_EDGES_FILES_DIRECTORY: str = 'Files/InvalidEdges'
TEST_PROV_FILES_DIRECTORY: str = 'Files/ProvFiles/Test'


class LeituraManipulacaoDadosT:
    def __init__(self):
        self.gats: Gats = Gats()
        self.read_session_time: str = ''

    @staticmethod
    def __read_session(path: str, graph: Graph, file_name: str):
        service = Services.ExtractProvDataService
        # tree = service.get_tree_from_file_path(path)
        tree = service.get_tree_from_filename(path)
        vertex_dictionary = service.get_tree_vertices_dictionary(tree)
        edge_dictionary = service.get_tree_edges_dictionary(tree, vertex_dictionary)
        edge_dictionary_filtered = service.filter_edge_dict_by_type_and_label(edge_dictionary, ACTIVITY)
        service.add_edges_to_graph(edge_dictionary_filtered, graph, file_name)

    def __create_gats(self, path: str, file_name: str, loop: int):
        self.__read_session(path, self.gats.graph_gats, file_name)
        session_gats = self.gats
        gats_graph = GatsGraph()
        gats_graph.set_current_time_to_folder(self.read_session_time)

        # True para exibir cores, False para não exibir as cores
        gats = gats_graph.create_gats_graph(session_gats, file_name, loop, True)
        return gats

    def __add_gats_to_agats(self, gats_list: List[GatsGraph], path: str, file_name: str, loop: int):
        gats_graph = self.__create_gats(path, file_name, loop)
        gats_list.append(gats_graph)
        self.gats.graph_gats.empty_lists()

    def __create_agats_from_file(self, agats_file_name):
        gats_service = Services.GatsService
        self.gats = gats_service.create_gats_form_agats_file(agats_file_name, self.gats)

        session_gats = self.gats
        gats_graph = GatsGraph()
        gats_graph.set_current_time_to_folder(self.read_session_time)

        gats = gats_graph.create_gats_graph(session_gats, agats_file_name, 1, True)
        gats_list: List[GatsGraph] = [gats]

        gats_file_path_list: List[str] = self.__create_gats_file_path_list(TEST_PROV_FILES_DIRECTORY)
        for i in range(len(gats_file_path_list)):
            loop: int = i + 2
            file_name: str = 'Gats Test ' + str(loop)
            self.__add_gats_to_agats(gats_list, gats_file_path_list[i], file_name, loop)

        agats_graph = AGats()
        agats_graph.create_agats(gats_list, agats_file_name)
        agats_graph.export_agats()

    @staticmethod
    def ask_for_invalid_edges_to_user():
        has_invalid_edge: bool = True
        filename = 'invalid_edges.txt'
        file_path_and_name = os.path.join(INVALID_EDGES_FILES_DIRECTORY, filename)
        with open(file_path_and_name, 'a') as file:
            while has_invalid_edge:
                invalid_edge_response = \
                    input("O modelo possui alguma aresta (edge) inválida não informada? (S/s ou N/n): ")

                has_invalid: bool = (invalid_edge_response == 'S') or (invalid_edge_response == 's')
                has_valid: bool = (invalid_edge_response == 'N') or (invalid_edge_response == 'n')

                if has_valid:
                    has_invalid_edge = False

                elif has_invalid:
                    invalid_edge = input("Entre com a aresta (edge) inválida (Ex: Region 01 -> Region 02):")
                    file.write(invalid_edge)
                    file.write('\n')

                else:
                    print("Por favor, entre com uma resposta válida (S/s ou N/n)")

    def __create_agats(self):
        gats_list: List[GatsGraph] = []
        gats_file_path_list: List[str] = self.__create_gats_file_path_list(PROV_FILES_DIRECTORY)
        for i in range(len(gats_file_path_list)):
            loop: int = i + 1
            file_name: str = 'Gats Test ' + str(loop)
            self.__add_gats_to_agats(gats_list, gats_file_path_list[i], file_name, loop)

        agats_graph = AGats()
        agats_graph.create_agats(gats_list, 'AGats Test 01')
        agats_graph.export_agats()
        self.ask_for_invalid_edges_to_user()

    @staticmethod
    def __read_agats_from_file():
        agats_graph_file = AGats()
        agats_graph_file.export_agats_from_file('AGats Test 01')

    @staticmethod
    def __create_gats_file_path_list(directory):
        utilities_io = Utils.UtilitiesIO
        file_path_list: List[str] = utilities_io.get_fullname_from_all_files_in_dir(directory)
        return file_path_list

    def main(self):
        time = datetime.now()
        str_time = time.strftime(DATE_FORMAT)
        self.read_session_time = str_time

        self.__create_agats()
        # self.__create_agats_from_file('AGats Test 01')
        # self.__read_agats_from_file()


'''End of Class'''
