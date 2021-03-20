from typing import List

# CONSTANTS
from Models.Graph.Graph import GraphVertex

UNDERSCORE: str = '_'


class GraphEdge:
    def __init__(self, source_vertex_region: GraphVertex, target_vertex_region: GraphVertex,
                 session_name: str, is_respawn: bool, is_invalid: bool = False):

        self.source_vertex_region = source_vertex_region
        self.target_vertex_region = target_vertex_region
        self.id_node = self.source_vertex_region.region + UNDERSCORE + self.target_vertex_region.region
        self.frequency = 1
        self.sessions: List[str] = []
        self.sessions.append(session_name)
        self.is_respawn = is_respawn
        self.is_invalid = is_invalid
