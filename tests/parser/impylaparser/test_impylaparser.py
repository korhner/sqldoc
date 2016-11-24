import pytest
import os
from sqldoc.parser.impylaparser.impylaparser import ImpylaParser
from sqldoc.metadata import metadata
from impala.dbapi import connect

skip_impyla = pytest.mark.skipif(
    pytest.config.getoption("--impala-url") is None,
    reason='add --impala-url=<IMPALA-URL>:<IMPALA-PORT> option to execute impylaparser tests.'
)

sql_dir = os.path.dirname(os.path.realpath(__file__))
db_create = os.path.join(sql_dir, 'sql/db_create.sql')
db_destroy = os.path.join(sql_dir, 'sql/db_destroy.sql')


@pytest.fixture
def configuration():
    host, port = pytest.config.getoption("--impala-url").split(':')
    return {'host': host, 'port': port}


def impyla_execute_file(connection, file_path):
    with open(file_path) as f:
        cursor = connection.cursor()
        cursor.execute(f.read())


@pytest.yield_fixture
def prepare_db(configuration):
    connection = connect(host=configuration['host'], port=configuration['port'])
    impyla_execute_file(connection, db_destroy)
    impyla_execute_file(connection, db_create)
    yield
    impyla_execute_file(connection, db_destroy)


def test_empty_db(prepare_db, configuration):
    parser = ImpylaParser('sql_doc_empty', configuration)
    expected_metadata = metadata.Database('sql_doc_empty', None, [])
    assert expected_metadata == parser.build_database_metadata()


def test_full_db(prepare_db, configuration):
    parser = ImpylaParser('sql_doc_two_tables', configuration)
    expected_metadata = metadata.Database('sql_doc_empty', None, [
        metadata.Table('empty_partitioned_no_comments', None, [
            metadata.Column('id', 'INTEGER', True, None)
        ], {'partitions': [metadata.Column('p_id', 'INTEGER', True, None)]}),
        metadata.Table('empty_not_partitioned_no_comments', None, [
            metadata.Column('id', 'INTEGER', True, None)
        ], {}),
        metadata.Table('empty_partitioned_comments', 'A partitioned table.', [
            metadata.Column('id', 'INTEGER', True, 'Id field.')
        ], {'partitions': [metadata.Column('p_id', 'INTEGER', True, 'Id of the partition.')]}),
        metadata.Table('empty_not_partitioned_comments', 'A non partitioned table.', [
            metadata.Column('id', 'INTEGER', True, 'Id field.')
        ], {}),
    ])

    metadata = parser.build_database_metadata()

    # leave only partition information for easier testing
    for table in metadata.tables:
        partitions = table.metadata.get('partitions')
        table.metadata = {} if partitions is None else {'partitions': partitions}

    assert expected_metadata == metadata
