from typing import Dict, List

from graphviz import Digraph

from Models.Graph import Graph
from Models.GraphEdge import GraphEdge

# Constants
COLOR_GREEN = 'green'
COLOR_BLUE = 'blue'
COLOR_BLACK = 'black'


def __create_dot_and_nodes(graph: Graph, file_name: str):
    dot = Digraph(comment=file_name)
    node_name_list: List[str] = __get_node_name_form_graph(graph)
    for name_region in node_name_list:
        if name_region in graph.newVertexElements:
            dot.node(name_region, name_region, style='filled', fillcolor=COLOR_GREEN)
        else:
            dot.node(name_region, name_region)
    return dot


def __create_dot_and_nodes_for_multiple_sessions(graph: Graph, file_name: List[str]):
    file: str = str(file_name)
    return __create_dot_and_nodes(graph, file)


def __create_dot_and_nodes_for_single_session(graph: Graph, file_name: str):
    return __create_dot_and_nodes(graph, file_name)


def __create_colored_dot_edge(dot: Digraph, frequency: int, node_a: str, node_b: str, edge_color: str):
    frequency_text: str = "Frequência: {}".format(frequency)
    dot.edge(node_a, node_b, frequency_text,  color=edge_color, constraint='true')


def try_to_build_gats_graphs_for_multiple(graph: Graph, file_name: List[str], loops: int):
    dot = __create_dot_and_nodes_for_multiple_sessions(graph, file_name)
    common_edges: List[str] = __get_common_edges_from_all_sessions(graph, file_name, loops)
    edge_dict: Dict[str, GraphEdge] = graph.get_edges()
    for key in edge_dict:
        edge_regions: List[str] = key.split('_')
        frequency: int = edge_dict[key].frequency
        if key in common_edges:
            __create_colored_dot_edge(dot, frequency, edge_regions[0], edge_regions[1], COLOR_BLUE)
        elif key in graph.newEdgeElements:
            __create_colored_dot_edge(dot, frequency, edge_regions[0], edge_regions[1], COLOR_GREEN)
        else:
            __create_colored_dot_edge(dot, frequency, edge_regions[0], edge_regions[1], COLOR_BLACK)
    dot.render('test-output/{}.gv'.format(file_name), view=True)


def try_to_build_gats_graphs_for_single(graph: Graph, file_name: str):
    dot = __create_dot_and_nodes_for_single_session(graph, file_name)
    edge_dict: Dict[str, GraphEdge] = graph.get_edges()
    for key_value in edge_dict:
        id_node_value: str = key_value
        edge_regions: List[str] = id_node_value.split('_')
        frequency: int = edge_dict[key_value].frequency
        __create_colored_dot_edge(dot, frequency, edge_regions[0], edge_regions[1], COLOR_BLACK)
    dot.render('test-output/{}.gv'.format(file_name), view=True)


def __get_node_name_form_graph(graph: Graph):
    vertex_dict = graph.vertices
    v_list: List[str] = []
    for region in vertex_dict:
        v_list.append(region)
    return v_list


def __get_common_edges_from_all_sessions(graph: Graph, file_name_list: List[str], loop: int = None):
    edge_dict = graph.edges
    edge_list: List[str] = []
    for key_value in edge_dict:
        graph_edge = edge_dict[key_value]
        frequency: int = edge_dict[key_value].frequency
        if frequency >= loop:
            file_name = file_name_list[loop-1]
            if file_name in graph_edge.sessions:
                edge_list.append(key_value)
    """End for"""
    return edge_list
