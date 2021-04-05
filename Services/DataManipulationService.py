import os
from datetime import datetime
from typing import Dict, List
# Import Tree
from xml.etree.ElementTree import ElementTree

# Import Services
import Services.AGatsService
import Services.ExtractProvDataService
import Services.GatsService
# Import Utils
import Utils.UtilitiesProvConstants
import Utils.UtilitiesFilePathConstants
import Utils.UtilitiesIO
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
UTILITIES_IO = Utils.UtilitiesIO
UTILITIES_FILE_PATH_CONSTANTS = Utils.UtilitiesFilePathConstants.UtilitiesFilePathConstants

AGATS_FILENAME: str = 'Agats'
GATS_FILENAME: str = 'Gats'


class DataManipulationService:
    def __init__(self):
        self.graph: Graph = Graph()
        self.read_session_time: str = ''

    # Change call for the desired functionality
    def main(self):
        self.__create_agats()
        self.__import_agats()

    def __create_agats(self):
        self.__set_session_time()
        loop: int = 1
        session_list: List[str] = []
        gats_to_agats: Gats = \
            self.__create_gats(loop, UTILITIES_FILE_PATH_CONSTANTS.READ_PROV_FILES_DIRECTORY, session_list)

        agats: AGats = AGats()
        agats.graph_agats = gats_to_agats.graph_gats

        agats.set_common_edges_on_creation(session_list)
        agats.set_invalid_edges_from_file(UTILITIES_FILE_PATH_CONSTANTS.INVALID_EDGE_FILENAME)

        should_paint: bool = True
        self.__export_agats(agats, should_paint)

        self.__ask_for_invalid_edges_to_user()

    def __import_agats(self):
        self.__set_session_time()
        folder_name_to_read: str = \
            UTILITIES_IO.get_dir_base_name(UTILITIES_FILE_PATH_CONSTANTS.READ_OUT_PUT_AGATS_DIRECTORY)
        agats: AGats = AGats()
        agats.folder_name = folder_name_to_read

        path_structure: str = UTILITIES_FILE_PATH_CONSTANTS.FORMAT_FILE_STRUCTURE
        graph: Graph = agats.import_agats_file(path_structure, AGATS_FILENAME)
        self.graph = graph

        loop: int = 1
        gats_file_name: str = '{} {}'.format(GATS_FILENAME, loop)
        loop += 1

        gats_to_export: Gats = Gats()
        gats_to_export.graph_gats = graph

        self.__export_gats(gats_to_export, gats_file_name)

        session_list: List[str] = [gats_file_name]
        gats_to_agats: Gats() = \
            self.__create_gats(loop, UTILITIES_FILE_PATH_CONSTANTS.READ_NEW_PROV_FILES_DIRECTORY, session_list)
        agats.graph_agats = gats_to_agats.graph_gats
        agats.set_common_edges_from_file_read(session_list)

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
                                   UTILITIES_FILE_PATH_CONSTANTS.FORMAT_FILE_STRUCTURE,
                                   AGATS_FILENAME, should_color_graph)

    def __export_gats(self, gats: Gats, file_name: str):
        GATS_SERVICE.export_gats(self.read_session_time, gats,
                                 UTILITIES_FILE_PATH_CONSTANTS.FORMAT_FILE_STRUCTURE,
                                 file_name)

    def __set_session_time(self):
        time: datetime = datetime.now()
        date_format: str = '%Y-%m-%d_%H-%M-%S'
        str_time: str = time.strftime(date_format)
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
    def __get_file_path_list(directory: str) -> List[str]:
        file_path_list: List[str] = UTILITIES_IO.get_fullname_from_all_files_in_dir(directory)
        return file_path_list

    @staticmethod
    def __ask_for_invalid_edges_to_user():
        has_invalid_edge: bool = True
        filename = UTILITIES_FILE_PATH_CONSTANTS.READ_INVALID_EDGES_FILE_NAME
        file_path_and_name = os.path.join(UTILITIES_FILE_PATH_CONSTANTS.READ_INVALID_EDGES_FILES_DIRECTORY, filename)

        has_invalid_edge_message: str = "O modelo possui alguma aresta (edge) inválida não informada? (S/s ou N/n): "
        has_invalid_node_edges_message: str = \
            "Entre com os IDs das regiões (nodes) que possuem uma aresta (edge) inválida (Ex:01 -> 02):"
        invalid_entry_message: str = "Por favor, entre com uma resposta válida (S/s ou N/n)"
        with open(file_path_and_name, 'a') as file:
            while has_invalid_edge:
                invalid_edge_response = input(has_invalid_edge_message)

                has_invalid: bool = (invalid_edge_response == 'S') or (invalid_edge_response == 's')
                has_valid: bool = (invalid_edge_response == 'N') or (invalid_edge_response == 'n')

                if has_valid:
                    has_invalid_edge = False

                elif has_invalid:
                    invalid_edge = input(has_invalid_node_edges_message)
                    file.write(invalid_edge)
                    file.write('\n')

                else:
                    print(invalid_entry_message)

    # Method that show how many coded lines were made on the following projects
    @staticmethod
    def __show_lines_on_all_projects():
        model_lines = EXTRACT_PROV_DATA_SERVICE.item_line_count(UTILITIES_FILE_PATH_CONSTANTS.MODELS_DIRECTORY)
        interface_lines = EXTRACT_PROV_DATA_SERVICE.item_line_count(UTILITIES_FILE_PATH_CONSTANTS.INTERFACE_DIRECTORY)
        services_lines = EXTRACT_PROV_DATA_SERVICE.item_line_count(UTILITIES_FILE_PATH_CONSTANTS.SERVICES_DIRECTORY)
        utils_lines = EXTRACT_PROV_DATA_SERVICE.item_line_count(UTILITIES_FILE_PATH_CONSTANTS.UTILS_DIRECTORY)

        resp = model_lines + interface_lines + services_lines + utils_lines
        print('\nModels Total Lines: {}\nInterface Total Lines: {}\nServices Total Lines: {}\nUtils Total Lines: {}'
              .format(model_lines, interface_lines, services_lines, utils_lines))
        print('\nApplication Total Lines: {}'.format(resp))
