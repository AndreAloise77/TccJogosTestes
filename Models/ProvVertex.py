from typing import List

from Models.ProvVertexAttribute import ProvVertexAttribute


class ProvVertex:
    def __init__(self, str_id, type_element, label_element, date_element,
                 attributes: List[ProvVertexAttribute], is_obj_player: bool):
        self.str_id = str_id
        self.type_element = type_element
        self.label_element = label_element
        self.date_element = date_element
        self.attributes = attributes
        self.is_obj_player = is_obj_player
