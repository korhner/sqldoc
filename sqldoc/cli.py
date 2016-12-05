# -*- coding: utf-8 -*-

import click
from sqldoc.config import config
import importlib


def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file', type=click.File())
@click.argument('output_file', type=click.File('w'))
def render(config_file, output_file):
    """Console script for sqldoc"""
    # load job
    job = config.load(config_file)
    parser_class = load_class(job.parser.class_path)
    parser = parser_class(job.parser.config)
    renderer_class = load_class(job.renderer.class_path)
    renderer = renderer_class(job.renderer.config)

    databases = [parser.build_database_metadata(database) for database in job.databases]
    renderer.render(databases, output_file)


@main.command()
@click.argument('output_file', type=click.File('w'))
def generate_config(output_file):
    config.generate_template(output_file)
