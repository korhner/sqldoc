from abc import ABCMeta, abstractmethod


class Renderer(metaclass=ABCMeta):
    def __init__(self, ):
        pass

    @abstractmethod
    def render(self, database, output_dir):
        pass
