from graphviz import Digraph


class GraphVizInterface:
    def export_file(self, path: str, file_name: str, digraph: Digraph):
        pass

    def import_agats_file(self, path: str, file_name: str):
        pass
