import os
import pytest
from sqldoc.renderer.jinjarenderer import jinjarenderer
from sqldoc.metadata import metadata


@pytest.fixture
def db_metadata():
    employee_columns = [
        metadata.Column('name', 'String', False, 'Name of the employee.'),
        metadata.Column('age', 'Integer', True, None)
    ]
    employee_table = metadata.Table('employee', 'List of employees.', employee_columns, {})

    order_columns = [
        metadata.Column('orderer_name', 'String', False, 'Name of the orderer.'),
        metadata.Column('order_id', 'String', False, 'Id of the order.')
    ]
    order_table = metadata.Table('order', None, order_columns, {})
    return metadata.Database('test_db', 'A test database.', [employee_table, order_table])


@pytest.fixture
def expected_output():
    return '''test_db
A test database.

employee
List of employees.

name
String
False
Name of the employee.

age
Integer
True
None


order
None

orderer_name
String
False
Name of the orderer.

order_id
String
False
Id of the order.

'''


def test_output(tmpdir, db_metadata, expected_output):
    output_path = os.path.join(str(tmpdir), 'output.html')
    renderer = jinjarenderer.JinjaRenderer({'template_name': 'simpletext.j2'})
    with open(output_path, 'w') as output_file:
        renderer.render([db_metadata], output_file)
    with open(output_path, 'r') as output_file:
        assert output_file.read() == expected_output
