import time
from amoChatApi.TextMessage import TextMessage
from amoChatApi.PhotoMessage import PhotoMessage
class Payload:
    def __init__(self, api, type = "text"):
        self._json_payload = {"payload":{}}
        self.set_timestamp(int(time.time()))
        self.api = api
        self.set_silent(False)
        self.set_event_type("new_message")
        if type == "text":
            self.message:TextMessage = TextMessage()
        if type == "photo":
            self.message:PhotoMessage = PhotoMessage()
    def set_event_type(self, type:str):
        self._json_payload["event_type"] = type
    def set_timestamp(self, timestamp:int):
        self._json_payload["payload"]["timestamp"] = timestamp
        self.set_msec_timestamp(timestamp*1000)
    def set_msec_timestamp(self, msec_timestamp:int):
        self._json_payload["payload"]["msec_timestamp"] = msec_timestamp
    def set_sender_id(self, id:str):
        try:
            self._json_payload["payload"]["sender"]["id"] = id
        except:
            self._json_payload["payload"]["sender"] = {}
            self._json_payload["payload"]["sender"]["id"] = id
    def set_sender_name(self, name:str):
        try:
            self._json_payload["payload"]["sender"]["name"] = name
        except:
            self._json_payload["payload"]["sender"] = {}
            self._json_payload["payload"]["sender"]["name"] = name
    def set_conversation_id(self, id:str):
        self._json_payload["payload"]["conversation_id"] = id
    def set_silent(self, state:bool):
        self._json_payload["payload"]["silent"] = state
    def set_source_id(self, id:str):
        self._json_payload["payload"]["source"] = {"external_id": id}
    def set_message_id(self, id:str):
        self._json_payload["payload"]["msgid"] = id
    def send(self):
        self._json_payload["payload"]["message"] = self.message.get_json()
        r = self.api.send_or_edit_message(self._json_payload)
        return r
