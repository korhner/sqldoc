import jinja2
import os
from sqldoc.renderer.renderer import Renderer

default_template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')


class JinjaRenderer(Renderer):
    def __init__(self, template_name, template_path=default_template_dir):
        super().__init__()
        self.template = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path)).get_template(template_name
                                                                                                       + '.j2')

    def render(self, database, output_dir):
        result = self.template.render(database=database)
        with open(os.path.join(output_dir, database.name + '.html'), "w") as f:
            f.write(result)
