class Database:
    def __init__(self, name, description, tables):
        self.name = name
        self.description = description
        self.tables = tables


class Table:
    def __init__(self, name, description, columns, metadata):
        self.name = name
        self.description = description
        self.columns = columns
        self.metadata = metadata


class Column:
    def __init__(self, name, data_type, nullable, description):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.description = description
