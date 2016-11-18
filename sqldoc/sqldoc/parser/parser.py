from abc import ABCMeta, abstractmethod

class Parser(metaclass=ABCMeta):

    def __init__(self, database_name, configuration):
        self.database_name = database_name
        self.configuration = configuration
        self.validate_configuration()
        pass

    @abstractmethod
    def validate_configuration(self):
        pass

    @abstractmethod
    def build_database_metadata(self):
        pass
