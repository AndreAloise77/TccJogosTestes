from Models.ProvVertex import ProvVertex


class ProvEdge:
    def __init__(self, id_name, type_element, label_element, value,
                 source_vertex_id: ProvVertex, target_vertex_id: ProvVertex):
        self.id_name = id_name
        self.type_element = type_element
        self.label_element = label_element
        self.value = value
        self.source_vertex_id = source_vertex_id
        self.target_vertex_id = target_vertex_id

    def id_name(self):
        return self.id_name

    def type_element(self):
        return self.type_element

    def label_element(self):
        return self.label_element

    def value(self):
        return self.value

    # Vertex witch starts the action
    def source_vertex_id(self):
        return self.source_vertex_id

    # Vertex witch receives the action
    def target_vertex_id(self):
        return self.target_vertex_id
