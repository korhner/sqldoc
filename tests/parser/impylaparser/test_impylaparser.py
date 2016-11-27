import pytest
import os
from sqldoc.parser.impylaparser.impylaparser import ImpylaParser
from sqldoc.metadata import metadata
from impala.dbapi import connect

impala_env_var='IMPALA_URL'

skip_impyla = pytest.mark.skipif(
    os.environ.get(impala_env_var) is None,
    reason='define {}=<IMPALA-URL>:<IMPALA-PORT> env variable to execute impylaparser tests.'.format(impala_env_var)
)

sql_dir = os.path.dirname(os.path.realpath(__file__))
db_create = os.path.join(sql_dir, 'sql/db_create.sql')
db_destroy = os.path.join(sql_dir, 'sql/db_destroy.sql')


@pytest.fixture
def configuration():
    host, port = os.environ[impala_env_var].split(':')
    return {'host': host, 'port': int(port)}

@pytest.fixture:
def parser(configuration):
    return ImpylaParser(configuration)

def impyla_execute_file(connection, file_path):
    with open(file_path) as f:
        for query in f.read().split(';'):
            if not query.strip():
                continue
            cursor = connection.cursor()
            cursor.execute(query)


@pytest.yield_fixture
def prepare_db(configuration):
    connection = connect(host=configuration['host'], port=configuration['port'])
    impyla_execute_file(connection, db_destroy)
    impyla_execute_file(connection, db_create)
    yield
    impyla_execute_file(connection, db_destroy)


@skip_impyla
def test_empty_db(prepare_db, parser):
    expected_metadata = metadata.Database('sql_doc_empty', None, [])
    assert str(expected_metadata) == str(parser.build_database_metadata('sql_doc_empty'))


@skip_impyla
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
