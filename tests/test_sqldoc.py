#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sqldoc import sqldoc
from sqldoc.parser.parser import Parser
from sqldoc.renderer.renderer import Renderer


@pytest.fixture
def mock_load_plugins(mocker):
    mocker.patch('sqldoc.sqldoc.load_plugins')
    sqldoc.load_plugins.return_value = [
        Plugin('parser_plugin', ParserPlugin),
        Plugin('renderer_plugin', RendererPlugin)
    ]


@pytest.fixture
def mock_wrong_plugin_type(mocker):
    mocker.patch('sqldoc.sqldoc.load_plugins')
    sqldoc.load_plugins.return_value = [
        Plugin('parser_plugin', InvalidPlugin)
    ]


class Plugin:
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls

    def load(self):
        return self.get_component

    def get_component(self):
        return self.cls


class InvalidPlugin:
    def __init__(self, configuration):
        pass


class ParserPlugin(Parser):
    def __init__(self, configuration):
        super().__init__(configuration)

    def validate_configuration(self):
        return True

    def build_database_metadata(self, database_name):
        return None


class RendererPlugin(Renderer):
    def __init__(self, configuration):
        super().__init__(configuration)

    def validate_configuration(self):
        return True

    def render(self, databases, output_file):
        pass


def test_plugin_added_to_map(mock_load_plugins):
    parser_map = sqldoc.build_parser_map()
    renderer_map = sqldoc.build_renderer_map()

    default_parsers = len(parser_map)
    default_renderers = len(renderer_map)

    plugins = sqldoc.load_plugins()
    sqldoc.register_plugins(parser_map, renderer_map, plugins)

    assert len(parser_map) == default_parsers + 1
    assert 'parser_plugin' in parser_map
    assert len(renderer_map) == default_renderers + 1
    assert 'renderer_plugin' in renderer_map


def test_plugin_conflict(mock_load_plugins):
    parser_map = sqldoc.build_parser_map()
    renderer_map = sqldoc.build_renderer_map()
    plugins = sqldoc.load_plugins()
    sqldoc.register_plugins(parser_map, renderer_map, plugins)

    # registering same plugins twice should cause conflict
    with pytest.raises(sqldoc.PluginConflictException):
        sqldoc.register_plugins(parser_map, renderer_map, plugins)


def test_unknown_plugin_type(mock_wrong_plugin_type):
    parser_map = sqldoc.build_parser_map()
    renderer_map = sqldoc.build_renderer_map()
    plugins = sqldoc.load_plugins()

    with pytest.raises(sqldoc.InvalidPluginException):
        sqldoc.register_plugins(parser_map, renderer_map, plugins)
