from abc import ABCMeta, abstractmethod

class Parser(metaclass=ABCMeta):

    def __init__(self, configuration):
        self.configuration = configuration
        self.validate_configuration()
        pass

    @abstractmethod
    def validate_configuration(self):
        pass

    @abstractmethod
    def build_database_metadata(self, database_name):
        pass
