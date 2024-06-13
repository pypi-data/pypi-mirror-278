from amoChatApi.AbstractMessage import Message
class TextMessage(Message):
    def __init__(self, text:str = None):
        self._text = text
    def get_json(self):
        json = {
            "type": "text",
            "text": self._text
        }
        return json
    def set_text(self, text:str):
        self._text = text
    def get_type(self):
        return "text"
