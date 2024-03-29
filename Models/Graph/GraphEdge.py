from typing import List

# CONSTANTS
from Models.Graph.GraphVertex import GraphVertex

UNDERSCORE: str = '_'


class GraphEdge:
    def __init__(self, source_vertex_region: GraphVertex, target_vertex_region: GraphVertex,
                 session_name: str, is_respawn: bool, is_invalid: bool = False):

        self.source_vertex_region: GraphVertex = source_vertex_region
        self.target_vertex_region: GraphVertex = target_vertex_region
        self.id_node: str = self.source_vertex_region.region + UNDERSCORE + self.target_vertex_region.region
        self.frequency: int = 1
        self.sessions: List[str] = []
        self.sessions.append(session_name)
        self.is_respawn: bool = is_respawn
        self.is_invalid: bool = is_invalid
