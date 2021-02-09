from graphviz import Digraph

from Models.Gats import Gats

from Services.GatsService import try_to_build_gats_graph


class GatsGraph:
    def __init__(self):
        self.gats_graph: Digraph = Digraph()

    def create_gats_graph(self, gats: Gats, file_name: str, loop: int, should_paint: bool):
        gats.add_graph_session(file_name)
        graph_gats = gats.graph_gats
        self.gats_graph = try_to_build_gats_graph(graph_gats, gats.sessions_list, loop, should_paint)
        return self.gats_graph
