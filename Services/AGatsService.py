from typing import Dict, List

from graphviz import Digraph

import Utils.UtilitiesGraph
from Models.Graph.AGats import AGats
from Models.Graph.Graph import Graph
from Models.Graph.GraphEdge import GraphEdge

UTILITIES_GRAPH = Utils.UtilitiesGraph

UNDERLINE_SEPARATOR: str = '_'
ARROW_SEPARATOR: str = '->'

# CONSTANTS TO ADD COLOR TO NODES AND EDGES
COLOR_BLUE = 'blue'
COLOR_BLACK = 'black'


def __create_dot_and_notes(graph: Graph, file_name: str):
    graph.add_id_to_vertex()
    dot = Digraph(comment=file_name)
    node_dict: Dict[int, str] = graph.vertices_to_node
    for node_id in node_dict:
        named_node: str = '{}'.format(node_id)
        named_region: str = node_dict[node_id]
        named_node_region: str = "Id: {} - {}".format(named_node, named_region)
        dot.node(named_region, named_node_region)
    return dot


def __try_to_build_agats_graph(agats: AGats, file_name: str, should_paint: bool) -> Digraph:
    graph: Graph = agats.graph_agats
    dot = __create_dot_and_notes(graph, file_name)

    common_edges: List[str] = agats.common_path
    invalid_edges: List[str] = agats.invalid_edges

    agats_edge_dict: Dict[str, GraphEdge] = graph.get_edges()

    for key_value in agats_edge_dict:
        id_node_value: str = key_value
        agats_edge_vertex_regions: List[str] = id_node_value.split(UNDERLINE_SEPARATOR)
        source_region: str = agats_edge_vertex_regions[0]
        target_region: str = agats_edge_vertex_regions[1]
        edge_frequency: int = agats_edge_dict[id_node_value].frequency
        is_respawn = agats_edge_dict[id_node_value].is_respawn

        if not should_paint:
            UTILITIES_GRAPH.create_colorless_dot_edge(dot, edge_frequency, source_region, target_region)

        else:
            invalid_source_id_list = __get_region_from_invalid_edges_list(invalid_edges, 0)
            invalid_target_id_list = __get_region_from_invalid_edges_list(invalid_edges, 1)

            node_vertices = graph.vertices_to_node

            invalid_source_region_list_by_id = \
                __get_invalid_regions_by_invalid_id_list(invalid_source_id_list, node_vertices)

            invalid_target_region_list_by_id = \
                __get_invalid_regions_by_invalid_id_list(invalid_target_id_list, node_vertices)

            if (source_region in invalid_source_region_list_by_id) and (target_region in
                                                                        invalid_target_region_list_by_id):
                UTILITIES_GRAPH.create_invalid_dot_edge(dot, edge_frequency, source_region, target_region)

            elif key_value in common_edges:
                UTILITIES_GRAPH.create_colored_dot_edge(dot, edge_frequency, source_region, target_region,
                                                        COLOR_BLUE, is_respawn)

            else:
                UTILITIES_GRAPH.create_colored_dot_edge(dot, edge_frequency, source_region, target_region,
                                                        COLOR_BLACK, is_respawn)
    return dot


# vertex_indicator = 0 for SOURCE
# vertex_indicator = 1 for TARGET
def __get_region_from_invalid_edges_list(invalid_edges_list: List[str], vertex_indicator: int):
    if vertex_indicator > 1 or vertex_indicator < 0:
        raise ValueError("Param [vertex_indicator] must be 0 or 1")

    regions_list: List[str] = []
    for invalid_edge in invalid_edges_list:
        regions = invalid_edge.split(ARROW_SEPARATOR)
        region = regions[vertex_indicator].strip()
        regions_list.append(region)

    regions_list = list(set(regions_list))
    return regions_list


def __get_invalid_regions_by_invalid_id_list(invalid_id_list: List[str], node_vertices: Dict[int, str]):
    source_region_list: List[str] = []
    for invalid_id in invalid_id_list:
        id_int: int = int(invalid_id)
        if id_int in node_vertices:
            region = node_vertices[id_int]
            source_region_list.append(region)

    return source_region_list


def export_agats(session_time: str, agats: AGats, path: str, file_name: str, should_paint: bool):
    agats.set_current_time_to_folder(session_time)
    digraph: Digraph = __try_to_build_agats_graph(agats, file_name, should_paint)
    agats.export_file(path, file_name, digraph)
