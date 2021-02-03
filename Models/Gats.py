from typing import List

from Models.Graph import Graph


class Gats:
    def __init__(self):
        self.graph_gats: Graph = Graph()
        self.sessions_list: List[str] = []

    def add_graph_session(self, file_name: str):
        self.sessions_list.append(file_name)
