import jinja2
import os
from sqldoc.renderer.renderer import Renderer

default_template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')


class JinjaRenderer(Renderer):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.template = jinja2.Environment(loader=jinja2.FileSystemLoader(self.configuration['template_path']))\
            .get_template(self.configuration['template_name'])

    def validate_configuration(self):
        default_values = {
            'template_path': default_template_dir
        }
        default_values.update(self.configuration)
        self.configuration = default_values

    def render(self, databases, output_file):
        result = self.template.render(databases=databases)
        output_file.write(result)
