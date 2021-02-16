from graphviz import Digraph

from Models.Gats import Gats

from Services.GatsService import try_to_build_gats_graph
from Utils.UtilitiesTestFilePathConstants import UtilitiesTestFilePathConstants


class GatsGraph:
    def __init__(self):
        self.gats_graph: Digraph = Digraph()
        self.session_folder_name: str = ''

    def create_gats_graph(self, gats: Gats, file_name: str, loop: int, should_paint: bool):
        gats.add_graph_session(file_name)
        graph_gats = gats.graph_gats
        self.gats_graph = try_to_build_gats_graph(graph_gats, gats.sessions_list, loop, should_paint)
        self.__generate_gats_dot_file(file_name)
        return self.gats_graph

    def set_current_time_to_folder(self, session_time: str):
        self.session_folder_name = session_time

    def __generate_gats_dot_file(self, file_name: str):
        self.gats_graph.render(UtilitiesTestFilePathConstants.GATS_FORMAT_FILE_STRUCTURE
                               .format(UtilitiesTestFilePathConstants.TEST_OUTPUT_PATH,
                                       UtilitiesTestFilePathConstants.TEST_OUTPUT_GATS_PATH,
                                       self.session_folder_name,
                                       file_name,
                                       UtilitiesTestFilePathConstants.GRAPHVIZ_EXTENSION_FILE),
                               view=False)
