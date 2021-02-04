# Import System Struct Objects

# Import Models
from Models.Gats import Gats
from Models.Graph import Graph

# Import Utility Functions
from Services.ExtractProvDataService import get_tree_from_file_path
from Services.ExtractProvDataService import get_tree_vertices_dictionary
from Services.ExtractProvDataService import get_tree_edges_dictionary
from Services.ExtractProvDataService import filter_edge_dict_by_type_and_label
from Services.ExtractProvDataService import add_edges_to_graph
from Services.GatsService import try_to_build_gats_graphs_for_single
from Services.GatsService import try_to_build_gats_graphs_for_multiple

# Constants
PATH_01: str = 'C:/Users/silvi/Desktop/Angry Robot 3/Builds/Build 08_Data/Teste/02'
PATH_02: str = 'C:/Users/silvi/Desktop/Angry Robot 3/Builds/Build 08_Data/Teste/01'
PATH_03: str = 'C:/Users/silvi/Desktop/Angry Robot 3/Builds/Build 08_Data/Teste/03'
BUG_NAMED_PATH_01: str = 'C:/Users/silvi/Desktop/Angry Robot 3/ProvFiles/01'
BUG_NAMED_PATH_02: str = 'C:/Users/silvi/Desktop/Angry Robot 3/ProvFiles/02'
BUG_NAMED_PATH_03: str = 'C:/Users/silvi/Desktop/Angry Robot 3/ProvFiles/03'
ACTIVITY: str = 'Activity'


class LeituraManipulacaoDadosT:
    def __init__(self):
        self.gats: Gats = Gats()

    @staticmethod
    def read_session(path: str, graph: Graph, file_name: str):
        tree = get_tree_from_file_path(path)
        vertex_dictionary = get_tree_vertices_dictionary(tree)
        edge_dictionary = get_tree_edges_dictionary(tree, vertex_dictionary)
        edge_dictionary_filtered = filter_edge_dict_by_type_and_label(edge_dictionary, ACTIVITY)
        add_edges_to_graph(edge_dictionary_filtered, graph, file_name)

    def print_graph(self):
        self.gats.graph_gats.print_graph()

    def read_session_and_create_gats(self, path: str, file_name: str, loop: int = None):
        self.read_session(path, self.gats.graph_gats, file_name)
        self.gats.add_graph_session(file_name)

        if not loop:
            try_to_build_gats_graphs_for_single(self.gats.graph_gats, file_name)
            self.gats = Gats()
        else:
            try_to_build_gats_graphs_for_multiple(self.gats.graph_gats, self.gats.sessions_list, loop)

        self.gats.graph_gats.empty_lists()

    def read_single_session(self, path: str, file_name: str):
        self.read_session_and_create_gats(path, file_name)

    def read_multiple_sessions_with_no_bug(self):
        self.read_session_and_create_gats(PATH_01, 'Gats Test 01', 1)
        self.read_session_and_create_gats(PATH_02, 'Gats Test 02', 2)
        self.read_session_and_create_gats(PATH_03, 'Gats Test 03', 3)

    def read_multiple_sessions_with_bug(self):
        self.read_session_and_create_gats(BUG_NAMED_PATH_01, 'Gats BUG Test 01', 1)
        self.read_session_and_create_gats(BUG_NAMED_PATH_02, 'Gats BUG Test 02', 2)
        self.read_session_and_create_gats(BUG_NAMED_PATH_03, 'Gats BUG Test 03', 3)

    def read_multiple_sessions(self):
        """Build with normal run"""
        self.read_multiple_sessions_with_no_bug()

        """Clean gats for renamed regions and multiples runs"""
        """self.gats = Gats()"""

        """Build with bug run"""
        """self.read_multiple_sessions_with_bug()"""

    def main(self):
        """Multiple sessions reader"""
        self.read_multiple_sessions()

        """Single session reader"""
        """self.read_single_session(BUG_NAMED_PATH_01, 'Gats BUG Test 01')
        self.read_single_session(BUG_NAMED_PATH_02, 'Gats BUG Test 02')
        self.read_single_session(BUG_NAMED_PATH_03, 'Gats BUG Test 03')"""


'''End of Class'''
