import jinja2
import os
from sqldoc.renderer.renderer import Renderer


class JinjaRenderer(Renderer):
    def __init__(self, database, output_dir, template_dir, template_name):
        super.__init__(database, output_dir)
        self.template_dir = template_dir
        self.template_name = template_name

    def render(self):
        result = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir)
        ).get_template(self.template_name).render(self.database)
        with open(os.path.join(self.output_dir, self.database.name, '.html'), "w") as f:
            f.write(result)
