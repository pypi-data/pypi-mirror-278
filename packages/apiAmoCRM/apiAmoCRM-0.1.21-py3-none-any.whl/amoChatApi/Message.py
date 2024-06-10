import abc
class Message:
    @abc.abstractmethod
    def get_json(self): pass
    @abc.abstractmethod
    def get_type(self): pass
