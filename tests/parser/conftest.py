import pytest


def pytest_addoption(parser):
    parser.addoption("--impala_url", action="store", default=None, help="<IMPALA-HOST>:<IMPALA-PORT>")
