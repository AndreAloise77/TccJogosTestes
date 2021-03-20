import os
from datetime import datetime
from typing import Dict, List
# Import Models
from xml.etree.ElementTree import ElementTree

# Import Services
import Services.AGatsService
import Services.ExtractProvDataService
import Services.GatsService
import Utils.UtilitiesFilePathConstants
import Utils.UtilitiesIO
# Import Utils
import Utils.UtilitiesProvConstants
# Import Models
from Models.Graph.AGats import AGats
from Models.Graph.Gats import Gats
from Models.Graph.Graph import Graph
from Models.Provenience.ProvEdge import ProvEdge
from Models.Provenience.ProvVertex import ProvVertex

# CONSTANTS
AGATS_SERVICE = Services.AGatsService
EXTRACT_PROV_DATA_SERVICE = Services.ExtractProvDataService
GATS_SERVICE = Services.GatsService

UTILITIES_CONSTANTS = Utils.UtilitiesProvConstants.UtilitiesProvConstants
UTILITIES_IOS = Utils.UtilitiesIO
UTILITIES_FILE_PATH_CONSTANTS = Utils.UtilitiesFilePathConstants.UtilitiesFilePathConstants

DATE_FORMAT: str = '%Y-%m-%d_%H-%M-%S'
PROV_FILES_DIRECTORY: str = 'Files/ProvFiles'
NEW_PROV_FILES_DIRECTORY: str = 'Files/ProvFiles/New'
EXPORTED_GATS_FILENAME_STRUCTURE: str = 'Gats {} from {}'

HAS_INVALID_EDGES_MESSAGE: str = "O modelo possui alguma aresta (edge) inválida não informada? (S/s ou N/n): "
HAS_INVALID_NODE_EDGES_MESSAGE: str = \
    "Entre com os IDs das regiões (nodes) que possuem uma aresta (edge) inválida (Ex:01 -> 02):"
INVALID_ENTRY_MESSAGE: str = "Por favor, entre com uma resposta válida (S/s ou N/n)"

AGATS_FILENAME: str = 'Agats'
GATS_FILENAME: str = 'Gats'


class DataManipulationService:
    def __init__(self):
        self.graph: Graph = Graph()
        self.read_session_time: str = ''

    def main(self):
        self.create_agats()
        # self.import_agats()

    def create_agats(self):
        self.__set_session_time()
        loop: int = 1
        session_list: List[str] = []
        gats_to_agats: Gats = self.__create_gats(loop, PROV_FILES_DIRECTORY, session_list)

        agats: AGats = AGats()
        agats.graph_agats = gats_to_agats.graph_gats

        agats.set_common_edges_on_creation(session_list)
        agats.set_invalid_edges_from_file(UTILITIES_FILE_PATH_CONSTANTS.INVALID_EDGE_FILENAME)

        should_paint: bool = True
        self.__export_agats(agats, should_paint)

        self.__ask_for_invalid_edges_to_user()

    def import_agats(self):
        self.__set_session_time()
        folder_name_to_read: str = '2021-03-18_04-02-30'
        agats: AGats = AGats()
        agats.folder_name = folder_name_to_read

        path_structure: str = UTILITIES_FILE_PATH_CONSTANTS.AGATS_FORMAT_FILE_STRUCTURE
        graph: Graph = agats.import_agats_file(path_structure, AGATS_FILENAME)
        # print(agats.common_path)
        self.graph = graph

        loop: int = 1
        gats_file_name: str = '{} {}'.format(GATS_FILENAME, loop)
        loop += 1

        gats_to_export: Gats = Gats()
        gats_to_export.graph_gats = graph

        self.__export_gats(gats_to_export, gats_file_name)

        session_list: List[str] = [gats_file_name]
        gats_to_agats: Gats() = self.__create_gats(loop, NEW_PROV_FILES_DIRECTORY, session_list)

        agats.graph_agats = gats_to_agats.graph_gats
        agats.set_common_edges_from_file_read(session_list)
        # print(agats.common_path)

        should_paint: bool = True
        self.__export_agats(agats, should_paint)

        self.__ask_for_invalid_edges_to_user()

    def __create_gats(self, loop: int, directory: str, session_list: List[str]) -> Gats:
        list_prov_files: List[str] = self.__get_file_path_list(directory)
        gats_to_agats: Gats = Gats()
        for path in list_prov_files:
            file_name: str = '{} {}'.format(GATS_FILENAME, loop)
            loop += 1

            self.__create_graph(self.graph, path, file_name)

            graph_to_export: Gats = Gats()
            self.__create_graph(graph_to_export, path, file_name)
            gats_to_agats.graph_gats = self.graph

            self.graph.empty_lists()
            session_list.append(file_name)

            gats_to_export: Gats = Gats()
            gats_to_export.graph_gats = graph_to_export
            self.__export_gats(gats_to_export, file_name)

        return gats_to_agats

    def __export_agats(self, agats: AGats, should_color_graph: bool):
        AGATS_SERVICE.export_agats(self.read_session_time, agats,
                                   UTILITIES_FILE_PATH_CONSTANTS.GATS_FORMAT_FILE_STRUCTURE,
                                   AGATS_FILENAME, should_color_graph)

    def __export_gats(self, gats: Gats, file_name: str):
        GATS_SERVICE.export_gats(self.read_session_time, gats,
                                 UTILITIES_FILE_PATH_CONSTANTS.GATS_FORMAT_FILE_STRUCTURE,
                                 file_name)

    def __set_session_time(self):
        time: datetime = datetime.now()
        str_time: str = time.strftime(DATE_FORMAT)
        self.read_session_time = str_time

    @staticmethod
    def __read_session(graph: Graph, path: str, file_name: str):
        prov_service = EXTRACT_PROV_DATA_SERVICE
        tree: ElementTree = prov_service.get_tree_from_filename(path)

        vertex_dictionary: Dict[str, ProvVertex] = prov_service.get_tree_vertices_dictionary(tree)
        edge_dictionary: Dict[str, ProvEdge] = prov_service.get_tree_edges_dictionary(tree, vertex_dictionary)

        edge_dictionary_filtered = \
            prov_service.filter_edge_dict_by_type_and_label(edge_dictionary, UTILITIES_CONSTANTS.ACTIVITY)

        graph.add_edges_to_graph(edge_dictionary_filtered, file_name)

    def __create_graph(self, graph: Graph, path: str, file_name: str):
        self.__read_session(graph, path, file_name)

    @staticmethod
    def __get_file_path_list(directory) -> List[str]:
        file_path_list: List[str] = UTILITIES_IOS.get_fullname_from_all_files_in_dir(directory)
        return file_path_list

    @staticmethod
    def __ask_for_invalid_edges_to_user():
        has_invalid_edge: bool = True
        filename = UTILITIES_FILE_PATH_CONSTANTS.INVALID_EDGES_FILE_NAME
        file_path_and_name = os.path.join(UTILITIES_FILE_PATH_CONSTANTS.INVALID_EDGES_FILES_DIRECTORY, filename)
        with open(file_path_and_name, 'a') as file:
            while has_invalid_edge:
                invalid_edge_response = input(HAS_INVALID_EDGES_MESSAGE)

                has_invalid: bool = (invalid_edge_response == 'S') or (invalid_edge_response == 's')
                has_valid: bool = (invalid_edge_response == 'N') or (invalid_edge_response == 'n')

                if has_valid:
                    has_invalid_edge = False

                elif has_invalid:
                    invalid_edge = input(HAS_INVALID_NODE_EDGES_MESSAGE)
                    file.write(invalid_edge)
                    file.write('\n')

                else:
                    print(INVALID_ENTRY_MESSAGE)
