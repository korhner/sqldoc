from abc import ABCMeta, abstractmethod


class Renderer(metaclass=ABCMeta):
    def __init__(self, configuration):
        self.configuration = configuration
        self.validate_configuration()

    @abstractmethod
    def validate_configuration(self):
        pass

    @abstractmethod
    def render(self, databases, output_file):
        pass
