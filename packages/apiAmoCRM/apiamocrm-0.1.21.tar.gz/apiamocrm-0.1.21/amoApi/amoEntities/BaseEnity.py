from abc import ABC, abstractmethod


class BaseEnity(ABC):
    @abstractmethod
    def get_id(self):
        pass
    @abstractmethod
    def get_json(self):
        pass