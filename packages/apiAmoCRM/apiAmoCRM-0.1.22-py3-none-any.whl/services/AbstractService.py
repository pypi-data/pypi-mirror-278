from abc import ABC, abstractmethod
class AbstractService(ABC):
    @abstractmethod
    def send_message(self, dialog_id:int, text:str):
        pass
    @abstractmethod
    def receive_message(self, chat_amo_api, amo_api):
        pass