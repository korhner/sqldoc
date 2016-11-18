from abc import ABCMeta, abstractmethod


class Renderer(metaclass=ABCMeta):
    def __init__(self, database, output_dir):
        self.database = database
        self.output_dir = output_dir

    @abstractmethod
    def render(self):
        pass
