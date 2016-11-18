class Database:
    def __init__(self, name, description, tables):
        self.name = name
        self.description = description
        self.tables = tables


class Table:
    def __init__(self, name, description, columns):
        self.name = name
        self.description = description
        self.columns = columns


class Column:
    def __init_(self, name, type, nullable, description):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.description = description
