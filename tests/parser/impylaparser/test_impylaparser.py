import os

import pytest
from impala.dbapi import connect

from sqldoc.metadata import metadata
from sqldoc.parser.impylaparser.impylaparser import ImpylaParser, Driver

impala_env_var = 'IMPALA_URL'

sql_dir = os.path.dirname(os.path.realpath(__file__))
db_create = os.path.join(sql_dir, 'sql/db_create.sql')
db_destroy = os.path.join(sql_dir, 'sql/db_destroy.sql')


class FakeDriver(Driver):
    def __init__(self, host, port):
        pass

    def get_tables(self, database):
        if database == 'sql_doc_empty':
            return []
        elif database == 'sql_doc_tables':
            return ['empty_not_partitioned_comments', 'empty_not_partitioned_no_comments',
                    'empty_partitioned_comments', 'empty_partitioned_no_comments']
        else:
            raise Exception("Unknown database: {}".format(database))

    def get_desc(self, database, table):
        full_table = '{database}.{table}'.format(database=database, table=table)
        if full_table == 'sql_doc_tables.empty_not_partitioned_comments':
            return [('# col_name            ', 'data_type           ', 'comment             '),
                    ('', None, None),
                    ('id', 'INT', 'Id field.'),
                    ('', None, None),
                    ('# Detailed Table Information', None, None),
                    ('Database:           ', 'sql_doc_tables      ', None),
                    ('Owner:              ', 'ivank               ', None),
                    ('CreateTime:         ', 'Tue Nov 29 16:15:18 CET 2016', None),
                    ('LastAccessTime:     ', 'UNKNOWN             ', None),
                    ('Protect Mode:       ', 'None                ', None),
                    ('Retention:          ', '0                   ', None),
                    ('Location:           ', 'hdfs://nameservice/tmp/sql_doc_tables/empty_not_partitioned_comments',
                     None),
                    ('Table Type:         ', 'MANAGED_TABLE       ', None),
                    ('Table Parameters:', None, None),
                    ('', 'comment             ', 'A non partitioned table.'),
                    ('', 'transient_lastDdlTime', '1480432518          '),
                    ('', None, None),
                    ('# Storage Information', None, None),
                    ('SerDe Library:      ', 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe', None),
                    ('InputFormat:        ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat', None),
                    ('OutputFormat:       ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat', None),
                    ('Compressed:         ', 'No                  ', None),
                    ('Num Buckets:        ', '0                   ', None),
                    ('Bucket Columns:     ', '[]                  ', None),
                    ('Sort Columns:       ', '[]                  ', None)]
        elif full_table == 'sql_doc_tables.empty_not_partitioned_no_comments':
            return [('# col_name            ', 'data_type           ', 'comment             '),
                    ('', None, None),
                    ('id', 'INT', None),
                    ('', None, None),
                    ('# Detailed Table Information', None, None),
                    ('Database:           ', 'sql_doc_tables      ', None),
                    ('Owner:              ', 'ivank               ', None),
                    ('CreateTime:         ', 'Tue Nov 29 16:15:18 CET 2016', None),
                    ('LastAccessTime:     ', 'UNKNOWN             ', None),
                    ('Protect Mode:       ', 'None                ', None),
                    ('Retention:          ', '0                   ', None),
                    ('Location:           ', 'hdfs://nameservice/tmp/sql_doc_tables/empty_not_partitioned_no_comments',
                     None),
                    ('Table Type:         ', 'MANAGED_TABLE       ', None),
                    ('Table Parameters:', None, None),
                    ('', 'transient_lastDdlTime', '1480432518          '),
                    ('', None, None),
                    ('# Storage Information', None, None),
                    ('SerDe Library:      ', 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe', None),
                    ('InputFormat:        ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat', None),
                    ('OutputFormat:       ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat', None),
                    ('Compressed:         ', 'No                  ', None),
                    ('Num Buckets:        ', '0                   ', None),
                    ('Bucket Columns:     ', '[]                  ', None),
                    ('Sort Columns:       ', '[]                  ', None)]
        elif full_table == 'sql_doc_tables.empty_partitioned_comments':
            return [('# col_name            ', 'data_type           ', 'comment             '),
                    ('', None, None),
                    ('id', 'INT', 'Id field.'),
                    ('', None, None),
                    ('# Partition Information', None, None),
                    ('# col_name            ', 'data_type           ', 'comment             '),
                    ('', None, None),
                    ('p_id', 'INT', 'Id of the partition.'),
                    ('', None, None),
                    ('# Detailed Table Information', None, None),
                    ('Database:           ', 'sql_doc_tables      ', None),
                    ('Owner:              ', 'ivank               ', None),
                    ('CreateTime:         ', 'Tue Nov 29 16:15:18 CET 2016', None),
                    ('LastAccessTime:     ', 'UNKNOWN             ', None),
                    ('Protect Mode:       ', 'None                ', None),
                    ('Retention:          ', '0                   ', None),
                    ('Location:           ', 'hdfs://nameservice/tmp/sql_doc_tables/empty_partitioned_comments', None),
                    ('Table Type:         ', 'MANAGED_TABLE       ', None),
                    ('Table Parameters:', None, None),
                    ('', 'comment             ', 'A partitioned table.'),
                    ('', 'transient_lastDdlTime', '1480432518          '),
                    ('', None, None),
                    ('# Storage Information', None, None),
                    ('SerDe Library:      ', 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe', None),
                    ('InputFormat:        ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat', None),
                    ('OutputFormat:       ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat', None),
                    ('Compressed:         ', 'No                  ', None),
                    ('Num Buckets:        ', '0                   ', None),
                    ('Bucket Columns:     ', '[]                  ', None),
                    ('Sort Columns:       ', '[]                  ', None)]
        elif full_table == 'sql_doc_tables.empty_partitioned_no_comments':
            return [('# col_name            ', 'data_type           ', 'comment             '),
                    ('', None, None),
                    ('id', 'INT', None),
                    ('', None, None),
                    ('# Partition Information', None, None),
                    ('# col_name            ', 'data_type           ', 'comment             '),
                    ('', None, None),
                    ('p_id', 'INT', None),
                    ('', None, None),
                    ('# Detailed Table Information', None, None),
                    ('Database:           ', 'sql_doc_tables      ', None),
                    ('Owner:              ', 'ivank               ', None),
                    ('CreateTime:         ', 'Tue Nov 29 16:15:18 CET 2016', None),
                    ('LastAccessTime:     ', 'UNKNOWN             ', None),
                    ('Protect Mode:       ', 'None                ', None),
                    ('Retention:          ', '0                   ', None),
                    ('Location:           ', 'hdfs://nameservice/tmp/sql_doc_tables/empty_partitioned_no_comments',
                     None),
                    ('Table Type:         ', 'MANAGED_TABLE       ', None),
                    ('Table Parameters:', None, None),
                    ('', 'transient_lastDdlTime', '1480432518          '),
                    ('', None, None),
                    ('# Storage Information', None, None),
                    ('SerDe Library:      ', 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe', None),
                    ('InputFormat:        ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat', None),
                    ('OutputFormat:       ', 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat', None),
                    ('Compressed:         ', 'No                  ', None),
                    ('Num Buckets:        ', '0                   ', None),
                    ('Bucket Columns:     ', '[]                  ', None),
                    ('Sort Columns:       ', '[]                  ', None)]
        else:
            raise Exception("Unknown table: {}".format(full_table))


class FakeImpylaParser(ImpylaParser):
    def __init__(self, configuration):
        super().__init__(configuration)

    def driver(self):
        return FakeDriver(self.configuration['host'], self.configuration['port'])


@pytest.fixture
def mock_database():
    return os.environ.get(impala_env_var) is None


@pytest.fixture
def configuration(mock_database):
    if mock_database:
        host, port = 'localhost', 21050
    else:
        host, port = os.environ[impala_env_var].split(':')
    return {'host': host, 'port': int(port)}


@pytest.fixture
def parser(configuration, mock_database):
    if mock_database:
        return FakeImpylaParser(configuration)
    else:
        return ImpylaParser(configuration)


def impyla_execute_file(connection, file_path):
    with open(file_path) as f:
        for query in f.read().split(';'):
            if not query.strip():
                continue
            cursor = connection.cursor()
            cursor.execute(query)


@pytest.yield_fixture
def prepare_db(configuration, mock_database):
    if not mock_database:
        connection = connect(host=configuration['host'], port=configuration['port'])
        impyla_execute_file(connection, db_destroy)
        impyla_execute_file(connection, db_create)
        yield
        impyla_execute_file(connection, db_destroy)
    else:
        yield


def test_empty_db(prepare_db, parser):
    expected_metadata = metadata.Database('sql_doc_empty', None, [])
    assert str(expected_metadata) == str(parser.build_database_metadata('sql_doc_empty'))


def test_full_db(prepare_db, parser):
    expected_metadata = metadata.Database('sql_doc_tables', None, [
        metadata.Table('empty_not_partitioned_comments', 'A non partitioned table.', [
            metadata.Column('id', 'INT', True, 'Id field.')
        ], {}),
        metadata.Table('empty_not_partitioned_no_comments', None, [
            metadata.Column('id', 'INT', True, None)
        ], {}),
        metadata.Table('empty_partitioned_comments', 'A partitioned table.', [
            metadata.Column('id', 'INT', True, 'Id field.')
        ], {'partitions': [metadata.Column('p_id', 'INT', True, 'Id of the partition.')]}),
        metadata.Table('empty_partitioned_no_comments', None, [
            metadata.Column('id', 'INT', True, None)
        ], {'partitions': [metadata.Column('p_id', 'INT', True, None)]})
    ])

    parsed_metadata = parser.build_database_metadata('sql_doc_tables')

    # leave only partition information for easier testing
    for table in parsed_metadata.tables:
        partitions = table.metadata.get('partitions')
        table.metadata = {} if partitions is None else {'partitions': partitions}

    assert str(expected_metadata) == str(parsed_metadata)
