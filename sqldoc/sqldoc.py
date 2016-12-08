# -*- coding: utf-8 -*-

from pkg_resources import iter_entry_points
from sqldoc.parser.parser import Parser
from sqldoc.renderer.renderer import Renderer
from sqldoc.renderer.jinjarenderer.jinjarenderer import JinjaRenderer


class PluginConflictException(Exception):
    pass


class InvalidPluginException(Exception):
    pass


def build_parser_map():
    return {}


def build_renderer_map():
    return {'jinjarenderer': JinjaRenderer}


def add_if_not_exists(map, name, plugin):
    if name in map:
        raise PluginConflictException('Conflict with plugin: {name} '.format(name=name))
    map[name] = plugin


def register_plugins(parser_map, renderer_map, plugins):
    for plugin in plugins:
        plugin_name = plugin.name
        plugin_class = plugin.load()
        if issubclass(plugin_class, Parser):
            add_if_not_exists(parser_map, plugin_name, plugin_class)
        elif issubclass(plugin_class, Renderer):
            add_if_not_exists(renderer_map, plugin_name, plugin_class)
        else:
            raise InvalidPluginException("Plugin {name} {type} is neither a parser or render!"
                                         .format(name=plugin_name, type=plugin_class))


def load_plugins():
    return iter_entry_points(group='sqldoc_component', name=None)
