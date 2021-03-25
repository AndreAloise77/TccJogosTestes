from typing import List

from graphviz import Digraph

import Utils.UtilitiesIO
from Models.Graph.Graph import Graph
from Models.Graph.GraphVertex import GraphVertex
from Utils.UtilitiesAGatsFileConstants import UtilitiesAGatsFileConstants
from Utils.UtilitiesFilePathConstants import UtilitiesFilePathConstants

UTILITIES_IO = Utils.UtilitiesIO
UNDERSCORE: str = '_'


class AGats(Graph):
    def __init__(self):
        self.graph_agats: Graph = super().__init__()
        self.common_path: List[str] = []
        self.invalid_edges: List[str] = []
        self.folder_name: str = ''

    def set_current_time_to_folder(self, session_time: str):
        self.folder_name = session_time

    def set_common_edges_on_creation(self, session_list: List[str]):
        edge_dict = self.graph_agats.edges
        files_quantity: int = len(session_list)
        edge_list_candidates: List[str] = self.get_common_edges_candidates(session_list)

        common_edges: List[str] = []
        for key in edge_list_candidates:
            edge_sessions = edge_dict[key].sessions
            edge_sessions = list(dict.fromkeys(edge_sessions))
            if len(edge_sessions) >= files_quantity:
                common_edges.append(key)
        # End For
        self.common_path = list(dict.fromkeys(common_edges))

    def get_common_edges_candidates(self, session_list: List[str]) -> List[str]:
        edge_list_candidates: List[str] = []
        files_quantity: int = len(session_list)
        loop: int = 1
        while loop <= files_quantity:
            for key_value in self.graph_agats.edges:
                graph_edge = self.graph_agats.edges[key_value]
                frequency: int = self.graph_agats.edges[key_value].frequency
                if frequency >= files_quantity:
                    session_to_compare: str = session_list[loop - 1]
                    session_name = session_to_compare
                    if session_name in graph_edge.sessions:
                        edge_list_candidates.append(key_value)
            loop += 1
        # End while
        return edge_list_candidates

    def set_common_edges_from_file_read(self, session_list: List[str]):
        edge_list_candidates: List[str] = self.get_common_edges_candidates(session_list)
        self.common_path = self.__get_updated_common_path_list(edge_list_candidates, self.common_path)

    @staticmethod
    def __get_updated_common_path_list(candidate_list: List[str], current_common_path: List[str]) -> List[str]:
        files_quantity: int = len(candidate_list)
        common_edges_quantity: int = len(current_common_path)

        common_edges: List[str] = []
        if files_quantity <= common_edges_quantity:
            for candidate in candidate_list:
                if candidate in current_common_path:
                    common_edges.append(candidate)
        else:
            for candidate in current_common_path:
                if candidate in candidate_list:
                    common_edges.append(candidate)

        return common_edges

    def set_invalid_edges_from_file(self, invalid_file_name: str):
        self.invalid_edges = UTILITIES_IO.read_invalid_edges_file(invalid_file_name)

    def export_file(self, path: str, file_name: str, agats: Digraph):
        agats.render(path.format(UtilitiesFilePathConstants.OUTPUT_PATH,
                                 UtilitiesFilePathConstants.OUTPUT_AGATS_PATH,
                                 self.folder_name, file_name,
                                 UtilitiesFilePathConstants.GRAPHVIZ_EXTENSION_FILE),
                     view=True)

    def import_agats_file(self, path: str, file_name: str):
        graph: Graph = Graph()
        line_list: List[str] = UTILITIES_IO.import_agats_file_to_list(path, self.folder_name, file_name)
        edge_lines: List[str] = []
        node_lines: List[str] = []

        self.__update_edge_and_node_lines(edge_lines, node_lines, line_list)
        self.__create_graph_node_from_node_file_list(node_lines, graph)
        self.__create_graph_edge_from_edge_file_list(edge_lines, node_lines, file_name, graph)

        return graph

    @staticmethod
    def __update_edge_and_node_lines(edge_lines: List[str], node_lines: List[str], lines: List[str]):
        for line in lines:
            valid_line = line.strip()
            if UtilitiesAGatsFileConstants.DOUBLE_SLASH in valid_line:
                continue
            elif UtilitiesAGatsFileConstants.DIGRAPH_WITH_OPEN_BRACES in valid_line:
                continue
            elif UtilitiesAGatsFileConstants.CLOSE_BRACES in valid_line:
                continue
            else:
                if (UtilitiesAGatsFileConstants.ARROW_SEPARATOR not in valid_line) \
                        and (UtilitiesAGatsFileConstants.CONSTRAINT_WITH_EQUAL not in valid_line):
                    node_lines.append(valid_line)
                else:
                    edge_lines.append(valid_line)

    @staticmethod
    def __prepare_vertex_region_from_file(info_list: List[str]):
        vertex_region: str = info_list[0].replace(UtilitiesAGatsFileConstants.QUOTATION_MARK, '')
        vertex_region = vertex_region.replace(UtilitiesAGatsFileConstants.DOUBLE_BACKSLASH, '')
        vertex_region = UtilitiesAGatsFileConstants.WHITE_SPACE.join(vertex_region.split())
        return vertex_region

    def __create_graph_node_from_node_file_list(self, node_lines: List[str], graph: Graph):
        for node in node_lines:
            split_node = node.split(UtilitiesAGatsFileConstants.OPEN_BRACKETS)
            node_name = self.__prepare_vertex_region_from_file(split_node)

            graph_vertex: GraphVertex = GraphVertex(node_name)

            graph.vertices[node_name] = graph_vertex
            graph.newVertexElements.append(node_name)

    def __create_graph_edge_from_edge_file_list(self, edge_lines: List[str],
                                                node_lines: List[str], file_name: str, graph: Graph):
        for edge in edge_lines:
            split_edge = edge.split(UtilitiesAGatsFileConstants.ARROW_SEPARATOR)
            source_vertex_region: str = self.__prepare_vertex_region_from_file(split_edge)

            target_vertex_region_with_edge_info = split_edge[1]
            info_list = target_vertex_region_with_edge_info.split(UtilitiesAGatsFileConstants.OPEN_BRACKETS)
            target_vertex_region = self.__prepare_vertex_region_from_file(info_list)

            edge_info = info_list[1]
            is_respawn: bool
            if UtilitiesAGatsFileConstants.RESPAWNED_INDICATOR in edge_info:
                is_respawn = True
            else:
                is_respawn = False

            edge_freq: int
            freq_information_list = edge_info.split(UtilitiesAGatsFileConstants.QUOTATION_WITH_COLOR_EDGE)
            freq_information = freq_information_list[0]
            freq_value: str
            if UtilitiesAGatsFileConstants.COMMA_WITH_RESPAWNED_INDICATOR in freq_information:
                freq_label_info_list = freq_information\
                    .split(UtilitiesAGatsFileConstants.COMMA_WITH_RESPAWNED_INDICATOR)
                freq_with_label = freq_label_info_list[0]
                freq_value = freq_with_label.split(UtilitiesAGatsFileConstants.COLON)[1]
                edge_freq = int(freq_value)
            else:
                freq_info_list = freq_information.split(UtilitiesAGatsFileConstants.COLON)
                freq_value = freq_info_list[1].replace(UtilitiesAGatsFileConstants.QUOTATION_MARK, '')
                edge_freq = int(freq_value)

            # Search for common edges:
            if UtilitiesAGatsFileConstants.COMMON_EDGE_INDICATOR in edge_info:
                common_edge_path: str = source_vertex_region + UNDERSCORE + target_vertex_region
                self.common_path.append(common_edge_path)

            # Search for invalid edges:
            if UtilitiesAGatsFileConstants.INVALID_EDGE_INDICATOR in edge_info:
                # Search Node on node_lines for source and target regions ids
                self.__update_invalid_edges_from_file(source_vertex_region, target_vertex_region, node_lines)

            graph.add_edge_from_file(source_vertex_region, target_vertex_region, file_name, is_respawn, edge_freq)

    def __update_invalid_edges_from_file(self, source_region: str, target_region: str, node_lines: List[str]):
        source_id: str = ''
        target_id: str = ''
        for node in node_lines:
            split_node: List[str] = node.split(UtilitiesAGatsFileConstants.OPEN_BRACKETS)
            node_region_info: str = split_node[0]
            node_info: str = split_node[1]

            if source_region in node_region_info:
                source_id = self.__get_id_node_from_string(node_info)

            if target_region in node_region_info:
                target_id = self.__get_id_node_from_string(node_info)

        if source_id and target_id:
            # Create invalid edge, write it on invalid file and update invalid_edges
            invalid_edge_ids: str = '{} {} {}'.format(source_id, UtilitiesAGatsFileConstants.ARROW_SEPARATOR, target_id)
            UTILITIES_IO.write_on_invalid_file(invalid_edge_ids)
            self.invalid_edges.append(invalid_edge_ids)

    @staticmethod
    def __get_id_node_from_string(node_info: str) -> str:
        info_list: List[str] = node_info.split(UtilitiesAGatsFileConstants.HYPHEN_SEPARATOR)
        label_and_id_info: str = info_list[0]
        id_list: List[str] = label_and_id_info.split(UtilitiesAGatsFileConstants.ID_NODE_INDICATOR)
        id_value: str = id_list[1].strip()
        return id_value
