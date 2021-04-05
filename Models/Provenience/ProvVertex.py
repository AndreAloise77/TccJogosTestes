from typing import List

from Models.Provenience.ProvVertexAttribute import ProvVertexAttribute


class ProvVertex:
    def __init__(self, vertex_id: str, type_element: str, label_element: str, date_element: str,
                 attributes: List[ProvVertexAttribute], is_obj_player: bool):
        self.vertex_id: str = vertex_id
        self.type_element: str = type_element
        self.label_element: str = label_element
        self.date_element: str = date_element
        self.attributes: List[ProvVertexAttribute] = attributes
        self.is_obj_player: bool = is_obj_player
