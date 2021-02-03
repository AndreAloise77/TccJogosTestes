class ProvVertexAttribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_name(self, name: str):
        self.name = name

    def set_value(self, value: str):
        self.value = value

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value
