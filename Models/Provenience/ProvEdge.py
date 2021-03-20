from Models.Provenience.ProvVertex import ProvVertex


class ProvEdge:
    def __init__(self, edge_id_name: str, type_element: str, label_element: str, value,
                 source_vertex_id: ProvVertex, target_vertex_id: ProvVertex):
        self.edge_id_name = edge_id_name
        self.type_element = type_element
        self.label_element = label_element
        self.value = value
        self.source_vertex_id = source_vertex_id
        self.target_vertex_id = target_vertex_id
