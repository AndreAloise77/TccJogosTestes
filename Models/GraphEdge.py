from typing import List

from Models.GraphVertex import GraphVertex


class GraphEdge:
    def __init__(self, source_vertex_region: GraphVertex, target_vertex_region: GraphVertex,
                 session_name: str, is_respawn: bool):

        self.source_vertex_region = source_vertex_region
        self.target_vertex_region = target_vertex_region
        self.id_node = self.source_vertex_region.region + '_' + self.target_vertex_region.region
        self.frequency = 1
        self.sessions: List[str] = []
        self.sessions.append(session_name)
        self.is_respawn = is_respawn

    def print_edge(self):
        return 'NodeId: {}, Frequency: {}'.format(self.id_node, self.frequency)
