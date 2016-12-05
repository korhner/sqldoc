import yaml


def generate_template(file):
    parser = Parser('<full-path-to-parser-class>', {'config_key': 'config_value'})
    renderer = Renderer('<full-path-to-renderer-class>', {'config_key': 'config_value'})
    job = Job(['<database-name-1>', '<database-name-2>'], parser, renderer)
    yaml.dump(job, file)


def load(file):
    return yaml.safe_load(file.read())


class Parser(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Parser'

    def __init__(self, class_path, config):
        self.class_path = class_path
        self.config = config


class Renderer(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Renderer'

    def __init__(self, class_path, config):
        self.class_path = class_path
        self.config = config


class Job(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Job'

    def __init__(self, databases, parser, renderer):
        self.databases = databases
        self.parser = parser
        self.renderer = renderer
