class Database:
    def __init__(self, name, description, tables):
        self.name = name
        self.description = description
        self.tables = tables

    def __str__(self):
        tables = [str(table) for table in self.tables]
        return "{name} - {description}. Tables: {tables}"\
            .format(name=self.name, description=self.description, tables='\n'.join(tables))

    def __repr__(self):
        return self.__str__()


class Table:
    def __init__(self, name, description, columns, metadata):
        self.name = name
        self.description = description
        self.columns = columns
        self.metadata = metadata

    def __str__(self):
        columns = [str(column) for column in self.columns]
        return "{name} - {description}. Columns: {columns}. Metadata: {metadata}"\
            .format(name=self.name, description=self.description, columns='\n'.join(columns),
                    metadata=self.metadata)

    def __repr__(self):
        return self.__str__()


class Column:
    def __init__(self, name, data_type, nullable, description):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.description = description

    def __str__(self):
        return "{name} - {data_type} - {nullable} - {description}"\
            .format(name=self.name, data_type=self.data_type, nullable=self.nullable, description=self.description)

    def __repr__(self):
        return self.__str__()
