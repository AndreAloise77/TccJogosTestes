from typing import List, Dict

from graphviz import Digraph

import Utils.UtilitiesGraph
from Models.Graph.Gats import Gats
from Models.Graph.Graph import Graph
from Models.Graph.GraphEdge import GraphEdge

UTILITIES_GRAPH = Utils.UtilitiesGraph

UNDERLINE_SEPARATOR: str = '_'
FREQUENCY_TEXT_TO_GRAPH: str = 'Freq: {}'

# CONSTANTS TO ADD COLOR TO NODES AND EDGES
COLOR_BLACK = 'black'

# CONSTANTS TO CREATE NODE AND EDGE ON DIGRAPH
GRAPH_EDGE_STYLE_BOLD: str = 'bold'
GRAPH_EDGE_CONSTRAINT_TRUE: str = 'true'
COMMA_WITH_RESPAWNED_INDICATOR: str = ', Resp'


def add_graph_session(gats: Gats, file_name: str):
    gats.sessions_list.append(file_name)


def export_gats(session_time: str, gats: Gats, path: str, file_name: str):
    gats.set_current_time_to_folder(session_time)
    graph: Graph = gats.graph_gats
    digraph: Digraph = __try_to_build_gats_graph(graph, file_name)
    gats.export_file(path, file_name, digraph)


def __try_to_build_gats_graph(graph: Graph, file_name: str) -> Digraph:
    dot = __create_dot_and_notes(graph, file_name)

    gats_edge_dict: Dict[str, GraphEdge] = graph.get_edges()

    for key_value in gats_edge_dict:
        id_node_value: str = key_value
        gats_edge_vertex_regions: List[str] = id_node_value.split(UNDERLINE_SEPARATOR)
        source_region: str = gats_edge_vertex_regions[0]
        target_region: str = gats_edge_vertex_regions[1]
        edge_frequency: int = gats_edge_dict[id_node_value].frequency
        is_respawn = gats_edge_dict[id_node_value].is_respawn

        UTILITIES_GRAPH.create_colored_dot_edge(dot, edge_frequency, source_region,
                                                target_region, COLOR_BLACK, is_respawn)
    return dot


def __create_dot_and_notes(graph: Graph, file_name: str) -> Digraph:
    graph.add_id_to_vertex()
    dot = Digraph(comment=file_name)
    node_dict: Dict[int, str] = graph.vertices_to_node
    for node_id in node_dict:
        named_region: str = node_dict[node_id]
        named_node_region: str = "{}".format(named_region)
        dot.node(named_region, named_node_region)
    return dot
