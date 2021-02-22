# Import System Objects
from typing import Dict, List

# Import Graphviz
from graphviz import Digraph

# Import Models
from Models.Gats import Gats
from Models.Graph import Graph
from Models.GraphEdge import GraphEdge
from Models.GraphVertex import GraphVertex

# Constants
from Utils.UtilitiesTestFilePathConstants import UtilitiesTestFilePathConstants

UNDERLINE_SEPARATOR: str = '_'
FREQUENCY_TEXT_TO_GRAPH: str = 'Freq: {}'

# CONSTANTS TO ADD COLOR TO NODES AND EDGES
COLOR_GREEN = 'green'
COLOR_BLUE = 'blue'
COLOR_BLACK = 'black'
COLOR_RED = 'red'

# CONSTANTS TO CREATE NODE AND EDGE ON DIGRAPH
GRAPH_NODE_STYLE_FILLED: str = 'filled'
GRAPH_EDGE_STYLE_DASHED: str = 'dashed'
GRAPH_EDGE_STYLE_BOLD: str = 'bold'
GRAPH_EDGE_CONSTRAINT_TRUE: str = 'true'

# CONSTANTS TO READ AGATS FILE
DOUBLE_SLASH: str = '//'
DIGRAPH_WITH_OPEN_BRACES: str = 'digraph {'
CLOSE_BRACES: str = '}'
ARROW_SEPARATOR: str = '->'
CONSTRAINT_WITH_EQUAL: str = 'constraint='

# CONSTANTS TO MANIPULATE AGATS FILE INFO
QUOTATION_MARK: str = '"'
DOUBLE_BACKSLASH: str = "\\"
WHITE_SPACE: str = ' '
RESPAWNED_INDICATOR: str = 'Resp'
OPEN_BRACKETS: str = '['
QUOTATION_WITH_COLOR_EDGE: str = '" color='
COMMA_WITH_RESPAWNED_INDICATOR: str = ', Resp'
COLON: str = ':'


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
            __create_colorless_dot_edge(dot, edge_frequency, source_region, target_region)
        else:
            invalid_edges_list: List[str] = \
                __read_invalid_edges_file(UtilitiesTestFilePathConstants.INVALID_EDGE_FILENAME)

            invalid_source_region_list = __get_source_region_form_invalid_edges_list(invalid_edges_list)
            invalid_target_region_list = __get_target_region_form_invalid_edges_list(invalid_edges_list)

            if (source_region in invalid_source_region_list) and (target_region in invalid_target_region_list):
                __create_invalid_dot_edge(dot, edge_frequency, source_region, target_region)

            elif key_value in common_edges:
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
            dot.node(name_region, name_region, style=GRAPH_NODE_STYLE_FILLED, fillcolor=COLOR_GREEN)
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


def __create_invalid_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str):
    frequency_text: str = FREQUENCY_TEXT_TO_GRAPH.format(frequency)
    dot.edge(source_node, target_node, frequency_text, color=COLOR_RED, constraint=GRAPH_EDGE_CONSTRAINT_TRUE,
             style=GRAPH_EDGE_STYLE_DASHED)


def __create_colorless_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str):
    frequency_text: str = FREQUENCY_TEXT_TO_GRAPH.format(frequency)
    dot.edge(source_node, target_node, frequency_text, color=COLOR_BLACK, constraint=GRAPH_EDGE_CONSTRAINT_TRUE)


def __create_colored_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str,
                              edge_color: str, is_respawn: bool):
    frequency_text: str = FREQUENCY_TEXT_TO_GRAPH.format(frequency)
    if is_respawn:
        frequency_text = frequency_text + COMMA_WITH_RESPAWNED_INDICATOR
        dot.edge(source_node, target_node, frequency_text,
                 color=edge_color, constraint=GRAPH_EDGE_CONSTRAINT_TRUE, style=GRAPH_EDGE_STYLE_BOLD)
    else:
        dot.edge(source_node, target_node, frequency_text,
                 color=edge_color, constraint=GRAPH_EDGE_CONSTRAINT_TRUE)


def __get_source_region_form_invalid_edges_list(invalid_edges_list: List[str]):
    source_region_list: List[str] = []
    for invalid_edge in invalid_edges_list:
        regions = invalid_edge.split(ARROW_SEPARATOR)
        source_region = regions[0].strip()
        source_region_list.append(source_region)

    source_region_list = list(set(source_region_list))
    return source_region_list


def __get_target_region_form_invalid_edges_list(invalid_edges_list: List[str]):
    target_region_list: List[str] = []
    for invalid_edge in invalid_edges_list:
        regions = invalid_edge.split(ARROW_SEPARATOR)
        target_region = regions[1].strip()
        target_region_list.append(target_region)

    target_region_list = list(set(target_region_list))
    return target_region_list


def __read_invalid_edges_file(file_name: str):
    file = open(UtilitiesTestFilePathConstants.INVALID_EDGES_FILES_STRUCTURE
                .format(UtilitiesTestFilePathConstants.INVALID_EDGES_FILES_DIRECTORY,
                        file_name,
                        UtilitiesTestFilePathConstants.TEXT_EXTENSION_FILE))

    file_lines_list: List[str] = file.readlines()
    return file_lines_list


def __read_agats_from_file(file_name: str):
    file = open(UtilitiesTestFilePathConstants.AGATS_FORMAT_FILE_STRUCTURE
                .format(UtilitiesTestFilePathConstants.TEST_OUTPUT_PATH,
                        UtilitiesTestFilePathConstants.TEST_OUTPUT_AGATS_PATH,
                        file_name,
                        UtilitiesTestFilePathConstants.GRAPHVIZ_EXTENSION_FILE))

    file_lines_list: List[str] = file.readlines()
    return file_lines_list


def __update_edge_and_node_lines(edge_lines: List[str], node_lines: List[str], lines: List[str]):
    for line in lines:
        valid_line = line.strip()
        if DOUBLE_SLASH in valid_line:
            continue
        elif DIGRAPH_WITH_OPEN_BRACES in valid_line:
            continue
        elif CLOSE_BRACES in valid_line:
            continue
        else:
            if ARROW_SEPARATOR not in valid_line and CONSTRAINT_WITH_EQUAL not in valid_line:
                node_lines.append(valid_line)
            else:
                edge_lines.append(valid_line)


def __create_graph_edge_from_edge_file_list(edge_lines: List[str], file_name: str, graph: Graph):
    for edge in edge_lines:
        split_edge = edge.split(ARROW_SEPARATOR)
        source_vertex_region = split_edge[0].replace(QUOTATION_MARK, '')
        source_vertex_region = source_vertex_region.replace(DOUBLE_BACKSLASH, '')
        source_vertex_region = WHITE_SPACE.join(source_vertex_region.split())
        target_vertex_region_with_edge_info = split_edge[1]
        info_list = target_vertex_region_with_edge_info.split(OPEN_BRACKETS)
        target_vertex_region = info_list[0].replace(QUOTATION_MARK, '')
        target_vertex_region = target_vertex_region.replace(DOUBLE_BACKSLASH, '')
        target_vertex_region = WHITE_SPACE.join(target_vertex_region.split())
        edge_info = info_list[1]
        is_respawn: bool
        if RESPAWNED_INDICATOR in edge_info:
            is_respawn = True
        else:
            is_respawn = False

        edge_freq: int
        freq_information_list = edge_info.split(QUOTATION_WITH_COLOR_EDGE)
        freq_information = freq_information_list[0]
        freq_value: str
        if COMMA_WITH_RESPAWNED_INDICATOR in freq_information:
            freq_label_info_list = freq_information.split(COMMA_WITH_RESPAWNED_INDICATOR)
            freq_with_label = freq_label_info_list[0]
            freq_value = freq_with_label.split(COLON)[1]
            edge_freq = int(freq_value)
        else:
            freq_info_list = freq_information.split(COLON)
            freq_value = freq_info_list[1].replace(QUOTATION_MARK, '')
            edge_freq = int(freq_value)

        source_graph_vertex: GraphVertex = GraphVertex(source_vertex_region)
        target_graph_vertex: GraphVertex = GraphVertex(target_vertex_region)

        graph_edge: GraphEdge = GraphEdge(source_graph_vertex, target_graph_vertex, file_name, is_respawn)
        graph_edge.frequency = edge_freq

        key_value: str = source_vertex_region + UNDERLINE_SEPARATOR + target_vertex_region

        graph.edges[key_value] = graph_edge
        graph.newEdgeElements.append(key_value)


def __create_graph_node_from_node_file_list(node_lines: List[str], graph: Graph):
    for node in node_lines:
        split_node = node.split(OPEN_BRACKETS)
        node_name = split_node[0].replace(QUOTATION_MARK, '')
        node_name = node_name.replace(DOUBLE_BACKSLASH, '')
        node_name = WHITE_SPACE.join(node_name.split())

        graph_vertex: GraphVertex = GraphVertex(node_name)

        graph.vertices[node_name] = graph_vertex
        graph.newVertexElements.append(node_name)


def create_gats_form_agats_file(file_name: str, gats: Gats):
    file_lines_list: List[str] = __read_agats_from_file(file_name)

    edge_lines: List[str] = []
    node_lines: List[str] = []

    __update_edge_and_node_lines(edge_lines, node_lines, file_lines_list)

    __create_graph_node_from_node_file_list(node_lines, gats.graph_gats)
    __create_graph_edge_from_edge_file_list(edge_lines, file_name, gats.graph_gats)
    gats.sessions_list.append(file_name)

    return gats
