from amoChatApi.AbstractMessage import Message
class PhotoMessage(Message):
    def __init__(self, photo_url:str = None, photo_name:str = None, file_size:int = None, text:str = ""):
        self._text = text
        self._photo_url = photo_url
        self._photo_name = photo_name
        self._file_size = file_size
    def get_json(self):
        json = {
            "type": "picture",
            "media": self._photo_url,
            "file_name": self._photo_name
        }
        if not self._text is None:
            json["text"] = self._text
        if not self._file_size is None:
            json["file_size"] = self._file_size
        return json
    def set_text(self, text:str):
        self._text = text
    def set_url(self, url:str):
        self._photo_url = url
    def set_name(self, name:str):
        self._photo_name = name
    def set_file_size(self, size:int):
        self._file_size = size
    def get_type(self):
        return "picture"