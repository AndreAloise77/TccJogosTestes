# Import System Struct Objects
from typing import Dict, List
from os import listdir
from os.path import isfile, isdir, join
# Import Utilities
from xml.etree.ElementTree import ElementTree

import Utils.UtilitiesIO
import Utils.UtilitiesProvConstants
from Models.Provenience.ProvEdge import ProvEdge
from Models.Provenience.ProvVertex import ProvVertex
# Import Models
from Models.Provenience.ProvVertexAttribute import ProvVertexAttribute

# LOCAL CONSTANTS
UTILITIES_IO = Utils.UtilitiesIO
UTILITIES_CONSTANTS = Utils.UtilitiesProvConstants.UtilitiesProvConstants


def get_tree_from_filename(file_name: str) -> ElementTree:
    file_tree: ElementTree = UTILITIES_IO.build_tree_by_filename(file_name)
    return file_tree


def get_tree_vertices_dictionary(tree_from_file) -> Dict[str, ProvVertex]:
    dictionary_vertex: Dict[str, ProvVertex] = {}
    new_vertex_attribute: ProvVertexAttribute
    new_vertex: ProvVertex
    prov_vertices = tree_from_file.findall(UTILITIES_CONSTANTS.VERTICES)

    for vertices in prov_vertices:
        vertices_vertex = vertices.findall(UTILITIES_CONSTANTS.VERTEX)
        for vertex in vertices_vertex:
            id_vertex = vertex.find(UTILITIES_CONSTANTS.ID).text
            type_vertex = vertex.find(UTILITIES_CONSTANTS.TYPE).text
            label_vertex = vertex.find(UTILITIES_CONSTANTS.LABEL).text
            date_vertex = vertex.find(UTILITIES_CONSTANTS.VERTEX_DATE).text

            vertex_attributes_list: List[ProvVertexAttribute] = []
            attributes_vertex = vertex.findall(UTILITIES_CONSTANTS.ATTRIBUTES)

            for a_v in attributes_vertex:
                attribute_from_attributes = a_v.findall(UTILITIES_CONSTANTS.ATTRIBUTE)
                object_player: bool = False

                for att in attribute_from_attributes:
                    name = att.find(UTILITIES_CONSTANTS.ATTRIBUTE_NAME).text
                    att_value = att.find(UTILITIES_CONSTANTS.VALUE).text

                    if name == UTILITIES_CONSTANTS.ATTRIBUTE_NAME_OBJECT_NAME and \
                            att_value == UTILITIES_CONSTANTS.ATTRIBUTE_VALUE_PLAYER:
                        object_player = True
                    new_vertex_attribute = ProvVertexAttribute(name, att_value)
                    vertex_attributes_list.append(new_vertex_attribute)
                # end loop for single vertex attribute read

                new_vertex = \
                    ProvVertex(id_vertex, type_vertex, label_vertex, date_vertex, vertex_attributes_list, object_player)
                # clean attribute list
                vertex_attributes_list = []
                dictionary_vertex[id_vertex] = new_vertex
            # end 'for' attributes
        # end 'for' single vertex
    # end 'for' vertices
    return dictionary_vertex


def get_tree_edges_dictionary(tree_from_file, dict_vertex: Dict[str, ProvVertex]) -> Dict[str, ProvEdge]:
    dictionary_edges: Dict[str, ProvEdge] = {}
    new_edge: ProvEdge
    prov_edges = tree_from_file.findall(UTILITIES_CONSTANTS.EDGES)

    for edges_edg in prov_edges:
        edges_edge = edges_edg.findall(UTILITIES_CONSTANTS.EDGE)

        for e in edges_edge:
            edge_id = e.find(UTILITIES_CONSTANTS.ID).text
            edge_type = e.find(UTILITIES_CONSTANTS.TYPE).text
            edge_label = e.find(UTILITIES_CONSTANTS.LABEL).text
            edge_value = e.find(UTILITIES_CONSTANTS.VALUE).text

            edge_source_id = e.find(UTILITIES_CONSTANTS.EDGE_SOURCE_ID).text
            source_vertex = dict_vertex.get(edge_source_id)

            edge_target_id = e.find(UTILITIES_CONSTANTS.EDGE_TARGET_ID).text
            target_vertex = dict_vertex.get(edge_target_id)

            new_edge = ProvEdge(edge_id, edge_type, edge_label, edge_value, source_vertex, target_vertex)
            dictionary_edges[edge_id] = new_edge
        # end 'for' single Edge
    # end 'for' Edges
    return dictionary_edges


def filter_edge_dict_by_type_and_label(dictionary: Dict[str, ProvEdge],
                                       type_element: str, label_element: str = '') -> Dict[str, ProvEdge]:
    filtered_edges_dict: Dict[str, ProvEdge] = {}
    for key in dictionary:
        edge = dictionary[key]

        # bypass the edge read, if label is not Neutral
        is_edge_neutral = edge.label_element == UTILITIES_CONSTANTS.EDGE_LABEL_NEUTRAL
        if not is_edge_neutral:
            continue

        source_vertex: ProvVertex = edge.source_vertex_id
        target_vertex: ProvVertex = edge.target_vertex_id

        # bypass the edge read, if the vertex is not from a player
        is_from_player: bool = __check_vertex_came_from_player(source_vertex, target_vertex)
        if not is_from_player:
            continue

        # validate if 'type_element' from any vertex matches the param 'type_element'
        has_matched_types: bool = \
            __validate_param_match(source_vertex.type_element, target_vertex.type_element, type_element)
        if not has_matched_types:
            continue

        # filter by label
        if label_element:
            # bypass the edge read, if the label not matches the param 'label_element'
            has_matched_labels: bool = \
                __validate_param_match(source_vertex.label_element, target_vertex.label_element, label_element)
            if not has_matched_labels:
                continue

        # add edge 'filtered' to dictionary
        edge_id = edge.edge_id_name
        filtered_edges_dict[edge_id] = edge
    return filtered_edges_dict


def __check_vertex_came_from_player(source_vertex: ProvVertex, target_vertex: ProvVertex) -> bool:
    is_from_player: bool = True
    is_source_player: bool = source_vertex.is_obj_player
    is_target_player: bool = target_vertex.is_obj_player

    if (not is_source_player) or (not is_target_player):
        is_from_player = False

    return is_from_player


def __validate_param_match(source_param: str, target_param: str, param: str) -> bool:
    has_matched_params: bool = True
    has_source_matched: bool = source_param == param
    has_target_matched: bool = target_param == param

    if (not has_source_matched) or (not has_target_matched):
        has_matched_params = False

    return has_matched_params


def item_line_count(path):
    if isdir(path):
        return dir_line_count(path)
    elif isfile(path):
        return len(open(path, 'rb').readlines())
    else:
        return 0


def dir_line_count(dire):
    return sum(map(lambda item: item_line_count(join(dire, item)), listdir(dire)))
