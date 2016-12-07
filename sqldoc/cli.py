# -*- coding: utf-8 -*-

import click
from sqldoc.config import config
import importlib
from pkg_resources import iter_entry_points
from sqldoc.parser.parser import Parser
from sqldoc.renderer.renderer import Renderer
from sqldoc.renderer.jinjarenderer.jinjarenderer import JinjaRenderer


def build_parser_map():
    return {}

def build_renderer_map():
    return {'jinjarenderer': JinjaRenderer}

def add_if_not_exists(map, name, plugin):
    if name in map:
        raise Exception('Conflict with plugin: {name} '.format(name=name))
    map[name] = plugin

def load_plugins(parser_map, renderer_map):
    for entry_point in iter_entry_points(group='sqldoc_component', name=None):
        plugin_name = entry_point.name
        plugin_class = entry_point.load()
        if issubclass(plugin_class, Parser):
            add_if_not_exists(parser_map, plugin_name, plugin_class)
        elif issubclass(plugin_class, Renderer):
            add_if_not_exists(renderer_map, plugin_name, plugin_class)
        else:
            raise Exception("Plugin {name} is neither a parser or render!".format(name=plugin_name))


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file', type=click.File())
@click.argument('output_file', type=click.File('w'))
def render(config_file, output_file):
    """Console script for sqldoc"""
    # load job
    parser_map = build_parser_map()
    renderer_map = build_renderer_map()
    load_plugins(parser_map, renderer_map)

    job = config.load(config_file)
    parser_class = parser_map[job.parser.name]
    parser = parser_class(job.parser.config)
    renderer_class = renderer_map(job.renderer.name)
    renderer = renderer_class(job.renderer.config)

    databases = [parser.build_database_metadata(database) for database in job.databases]
    renderer.render(databases, output_file)


@main.command()
@click.argument('output_file', type=click.File('w'))
def generate_config(output_file):
    config.generate_template(output_file)
