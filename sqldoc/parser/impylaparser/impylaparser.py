from impala.dbapi import connect
import os
from sqldoc.parser.parser import Parser
from sqldoc.metadata import metadata

relevant_table_information = {'Location:', 'Owner:', 'CreateTime:'}


def _get_tables(connection, database):
    cursor = connection.cursor()
    cursor.execute('show tables in {}'.format(database))
    return [table[0] for table in cursor]


def _get_desc(connection, database, table):
    cursor = connection.cursor()
    cursor.execute("describe formatted {database}.{table}".format(database=database, table=table))
    return cursor.fetchall()


def _parse_desc(desc):
    value_map = {}
    try:
        current_index = 2  # skip first two rows
        columns = []
        while desc[current_index] != ('', None, None):
            column_name, data_type, column_description = desc[current_index]
            columns.append(metadata.Column(column_name, data_type, True, column_description))
            current_index += 1
        value_map['columns'] = columns
        while current_index < len(desc):
            while not desc[current_index][0].startswith('#'):
                current_index += 1
            if desc[current_index][0].startswith('# Partition Information'):
                current_index += 3
                partition_columns = []
                while desc[current_index][0] != '':
                    column_name, data_type, column_description = desc[current_index]
                    partition_columns.append(metadata.Column(column_name, data_type, True, column_description))
                    current_index += 1
                value_map['partitions'] = partition_columns
            elif desc[current_index][0].startswith('# Detailed Table Information'):
                current_index += 1
                while desc[current_index][0] != '':
                    if desc[current_index][0] not in relevant_table_information:
                        continue
                    key, value, _ = desc[current_index]
                    value_map[key.strip()] = value.strip() if value is not None else None
                    current_index += 1
            else:
                current_index += 1
    except IndexError:
        pass
    return value_map


class ImpylaParser(Parser):
    def __init__(self, database_name, configuration):
        super().__init__(database_name, configuration)

    def connection(self):
        return connect(host=self.configuration['host'], port=self.configuration['port'])

    def validate_configuration(self):
        pass

    def build_database_metadata(self):
        connection = self.connection()
        tables = []
        for table_name in _get_tables(connection, self.database_name):
            desc = _parse_desc(_get_desc(connection, self.database_name, table_name))
            columns = desc.pop['columns']
            tables.append(metadata.Table(table_name, None, columns, desc))
        return metadata.Database(self.database_name, None, tables)
