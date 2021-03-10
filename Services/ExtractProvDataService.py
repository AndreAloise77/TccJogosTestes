# Import System Struct Objects
from typing import Dict, List

# Import Models
from Models.Graph import Graph
from Models.ProvVertexAttribute import ProvVertexAttribute
from Models.ProvVertex import ProvVertex
from Models.ProvEdge import ProvEdge
from Utils.UtilitiesProvConstants import UtilitiesProvConstants

# Import Utility Functions
import Utils.UtilitiesIO

# Constants:
REGION = 'Region'
EDGE_LABEL_NEUTRAL = 'Neutral'
# EDGE_LABEL_RESPAWNED = 'Respawned'
ATTRIBUTE_NAME_OBJECT_NAME = 'ObjectName'
ATTRIBUTE_VALUE_PLAYER = 'Player'
RESPAWN = 'Respawn'

UTILITIES_IO = Utils.UtilitiesIO


def get_tree_from_file_path(file_path: str):
    file_tree = UTILITIES_IO.get_single_file_in_dir(file_path)
    return file_tree


def get_tree_from_filename(file_name: str):
    file_tree = UTILITIES_IO.build_tree_by_filename(file_name)
    return file_tree


def get_tree_vertices_dictionary(tree_from_file):
    dictionary_vertex: Dict[str, ProvVertex] = {}
    new_attribute: ProvVertexAttribute
    new_vertex: ProvVertex
    prov_vertices = tree_from_file.findall(UtilitiesProvConstants.VERTICES)

    for vertices in prov_vertices:
        vertices_vertex = vertices.findall(UtilitiesProvConstants.VERTEX)
        for vertex in vertices_vertex:
            id_vertex = vertex.find(UtilitiesProvConstants.ID).text
            type_vertex = vertex.find(UtilitiesProvConstants.TYPE).text
            label_vertex = vertex.find(UtilitiesProvConstants.LABEL).text
            date_vertex = vertex.find(UtilitiesProvConstants.VERTEX_DATE).text

            vertex_attributes_list: List[ProvVertexAttribute] = []
            attributes_vertex = vertex.findall(UtilitiesProvConstants.ATTRIBUTES)

            for a_v in attributes_vertex:
                attribute_from_attributes = a_v.findall(UtilitiesProvConstants.ATTRIBUTE)
                object_player: bool = False

                for att in attribute_from_attributes:
                    name = att.find(UtilitiesProvConstants.ATTRIBUTE_NAME).text
                    att_value = att.find(UtilitiesProvConstants.VALUE).text

                    if name == ATTRIBUTE_NAME_OBJECT_NAME and att_value == ATTRIBUTE_VALUE_PLAYER:
                        object_player = True
                    new_attribute = ProvVertexAttribute(name, att_value)
                    vertex_attributes_list.append(new_attribute)
                '''End For single attribute'''
                new_vertex = \
                    ProvVertex(id_vertex, type_vertex, label_vertex, date_vertex, vertex_attributes_list, object_player)
                '''Limpa a lista de atributos para uma nova lista'''
                vertex_attributes_list = []
                dictionary_vertex[id_vertex] = new_vertex
            '''End For attributes'''
        '''End For single vertex'''
    '''End For vertices'''
    return dictionary_vertex


def get_tree_edges_dictionary(tree_from_file, dict_vertex: Dict[str, ProvVertex]):
    dictionary_edges: Dict[str, ProvEdge] = {}
    new_edge: ProvEdge
    prov_edges = tree_from_file.findall(UtilitiesProvConstants.EDGES)

    for edges_edg in prov_edges:
        edges_edge = edges_edg.findall(UtilitiesProvConstants.EDGE)

        for e in edges_edge:
            edge_id = e.find(UtilitiesProvConstants.ID).text
            edge_type = e.find(UtilitiesProvConstants.TYPE).text
            edge_label = e.find(UtilitiesProvConstants.LABEL).text
            edge_value = e.find(UtilitiesProvConstants.VALUE).text

            edge_source_id = e.find(UtilitiesProvConstants.EDGE_SOURCE_ID).text
            source_vertex = dict_vertex.get(edge_source_id)

            edge_target_id = e.find(UtilitiesProvConstants.EDGE_TARGET_ID).text
            target_vertex = dict_vertex.get(edge_target_id)

            new_edge = ProvEdge(edge_id, edge_type, edge_label, edge_value, source_vertex, target_vertex)
            dictionary_edges[edge_id] = new_edge
        '''End For Edge'''
    '''End For Edges'''
    return dictionary_edges


def filter_edge_dict_by_type_and_label(dictionary: Dict[str, ProvEdge], type_element: str, label_element: str = ''):
    edge_dict: Dict[str, ProvEdge] = {}
    for index, key in enumerate(dictionary):
        edge = dictionary[key]
        is_edge_neutral = edge.label_element == EDGE_LABEL_NEUTRAL
        # is_edge_respawned = edge.label_element == EDGE_LABEL_RESPAWNED
        # is_valid: bool = is_edge_respawned or is_edge_neutral
        # is_valid: bool = is_edge_respawned or is_edge_neutral
        # if not is_valid:
        if not is_edge_neutral:
            continue
        source_v = edge.source_vertex_id
        target_v = edge.target_vertex_id
        is_source_player = source_v.is_obj_player
        is_target_player = target_v.is_obj_player
        '''Caso algum vertex não seja do tipo player, pula de edge'''
        if (not is_source_player) or (not is_target_player):
            continue
        is_source_type = source_v.type_element == type_element
        is_target_type = target_v.type_element == type_element
        '''Caso algum vextex não seja do tipo passado, pula de edge'''
        if (not is_source_type) or (not is_target_type):
            continue
        '''Se o usuário desejar filtrar por label'''
        if label_element:
            is_source_label = source_v.label_element == label_element
            is_target_label = target_v.label_element == label_element
            '''Caso algum vertex não seja do label passado, pula de edge'''
            if (not is_source_label) or (not is_target_label):
                continue
        edge_id = edge.id_name
        '''Caso atenda as condições anteriores, adicionamos no dicionario'''
        edge_dict[edge_id] = edge
    return edge_dict


def __get_region_from_vertex(vertex: ProvVertex):
    region: str = ''
    for att in vertex.attributes:
        att_name = att.get_name()
        if att_name == REGION:
            region = att.get_value()
    return region


def __try_add_edge_to_graph(edge: ProvEdge, graph: Graph, file_name: str):
    source_vertex = edge.source_vertex_id
    source_region = __get_region_from_vertex(source_vertex)
    label_s = source_vertex.label_element

    target_vertex = edge.target_vertex_id
    target_region = __get_region_from_vertex(target_vertex)
    label_t = target_vertex.label_element

    has_valid_source_region: bool = source_region is not None
    has_valid_target_region: bool = target_region is not None
    has_valid_regions: bool = has_valid_source_region and has_valid_target_region

    if has_valid_regions and (source_region != target_region):
        if label_s != label_t and (label_t == RESPAWN or label_s == RESPAWN):
            # print("Label: {}, Source: {}, Target: {}".format(edge.label_element, target_region, source_region))
            # if edge.label_element != EDGE_LABEL_RESPAWNED:
            graph.add_edge(target_region, source_region, file_name, True)

        else:
            graph.add_edge(target_region, source_region, file_name, False)


def add_edges_to_graph(dict_edge: Dict[str, ProvEdge], graph: Graph, file_name: str):
    for index_enum, key_dict in enumerate(dict_edge):
        edge = dict_edge[key_dict]
        __try_add_edge_to_graph(edge, graph, file_name)

