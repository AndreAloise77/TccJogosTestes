from typing import Dict, List

from graphviz import Digraph

from Models.Graph import Graph
from Models.GraphEdge import GraphEdge

# Constants
COLOR_GREEN = 'green'
COLOR_BLUE = 'blue'
COLOR_BLACK = 'black'
COLOR_RED = 'red'


def try_to_build_gats_graph(graph: Graph, file_name_list: List[str], loop: int, should_paint: bool):
    dot = __create_dot_and_nodes_for_gats_graph(graph, file_name_list, should_paint)
    common_edges: List[str] = __get_common_edges(graph, file_name_list, loop)
    gats_edge_dict: Dict[str, GraphEdge] = graph.get_edges()
    for key_value in gats_edge_dict:
        id_node_value: str = key_value
        gats_edge_vertex_regions: List[str] = id_node_value.split('_')
        source_region: str = gats_edge_vertex_regions[0]
        target_region: str = gats_edge_vertex_regions[1]
        edge_frequency: int = gats_edge_dict[id_node_value].frequency
        is_respawn = gats_edge_dict[id_node_value].is_respawn
        if not should_paint:
            __create_colored_dot_edge(dot, edge_frequency, source_region, target_region, COLOR_BLACK)
        else:
            if key_value in common_edges:
                """Caminho em comum para todas as sessions"""
                __create_colored_dot_edge(dot, edge_frequency, source_region, target_region, COLOR_BLUE, is_respawn)
            elif key_value in graph.newEdgeElements:
                """Caminho novo para a ultima session"""
                __create_colored_dot_edge(dot, edge_frequency, source_region, target_region, COLOR_GREEN, is_respawn)
            else:
                """Somente um caminho que não é novo, comum ou respawn"""
                __create_colored_dot_edge(dot, edge_frequency, source_region, target_region, COLOR_BLACK, is_respawn)
    return dot


def __create_dot_and_nodes_for_gats_graph(graph: Graph, file_name_list: List[str], should_paint: bool):
    file_name: str = str(file_name_list)
    dot = Digraph(comment=file_name)
    node_name_list: List[str] = __get_node_name_form_graph(graph)
    for name_region in node_name_list:
        if should_paint and (name_region in graph.newVertexElements):
            dot.node(name_region, name_region, style='filled', fillcolor=COLOR_GREEN)
        else:
            dot.node(name_region, name_region)
    return dot


def __get_node_name_form_graph(graph: Graph):
    vertex_dict = graph.vertices
    v_list: List[str] = []
    for region in vertex_dict:
        v_list.append(region)
    return v_list


def __get_common_edges(graph: Graph, file_name_list: List[str], loop: int):
    edge_dict = graph.edges
    edge_list: List[str] = []
    for key_value in edge_dict:
        graph_edge = edge_dict[key_value]
        frequency: int = edge_dict[key_value].frequency
        if frequency >= loop:
            file_name = file_name_list[loop - 1]
            if file_name in graph_edge.sessions:
                edge_list.append(key_value)
    """End for"""
    return edge_list


def __create_colored_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str,
                              edge_color: str, is_respawn: bool = False):
    frequency_text: str = "Freq: {}".format(frequency)
    if is_respawn:
        e_color = edge_color + ':' + COLOR_RED
        frequency_text = frequency_text + '\n, Respawn'
        dot.edge(source_node, target_node, frequency_text, color=e_color, constraint='true', style='dashed')
    else:
        dot.edge(source_node, target_node, frequency_text, color=edge_color, constraint='true')
