from typing import List

from graphviz import Digraph

from Models.Graph.Graph import Graph
from Utils.UtilitiesFilePathConstants import UtilitiesFilePathConstants


class Gats(Graph):
    def __init__(self):
        self.graph_gats: Graph = super().__init__()
        self.sessions_list: List[str] = []
        self.folder_name: str = ''

    def set_current_time_to_folder(self, session_time: str):
        self.folder_name = session_time

    def export_file(self, path: str, file_name: str, gats: Digraph()):
        gats.render(path.format(UtilitiesFilePathConstants.OUTPUT_PATH,
                                UtilitiesFilePathConstants.OUTPUT_GATS_PATH,
                                self.folder_name, file_name,
                                UtilitiesFilePathConstants.GRAPHVIZ_EXTENSION_FILE), view=False)
