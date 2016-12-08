# -*- coding: utf-8 -*-

import click
from sqldoc.config import config
import importlib
from sqldoc import sqldoc


@click.group()
def main():
    pass


def build_plugin_maps():
    parser_map = sqldoc.build_parser_map()
    renderer_map = sqldoc.build_renderer_map()
    sqldoc.register_plugins(parser_map, renderer_map, sqldoc.load_plugins())
    return parser_map, renderer_map


def print_plugins(title, plugins):
    click.echo(title)
    for plugin in plugins:
        click.echo('\t- {plugin}'.format(plugin=plugin))


@main.command()
@click.argument('config_file', type=click.File())
@click.argument('output_file', type=click.File('w'))
def render(config_file, output_file):
    """Console script for sqldoc"""
    parser_map, renderer_map = build_plugin_maps()

    # load job
    job = config.load(config_file)
    parser_class = parser_map[job.parser.name]
    parser = parser_class(job.parser.config)
    renderer_class = renderer_map[job.renderer.name]
    renderer = renderer_class(job.renderer.config)

    databases = [parser.build_database_metadata(database) for database in job.databases]
    renderer.render(databases, output_file)


@main.command()
@click.argument('output_file', type=click.File('w'))
def generate_config(output_file):
    config.generate_template(output_file)


@main.command()
def plugins():
    parser_map, renderer_map = build_plugin_maps()
    print_plugins("Parser plugins:", parser_map)
    print_plugins("Renderer plugins:", renderer_map)
