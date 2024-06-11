import hashlib
import hmac
import json
from email.utils import formatdate
from amoChatApi.Payload import Payload
import requests


class ChatApi:
    def __init__(self, secret: str, id,  account_id, title, source_id, hook_api_version = "v2"):
        self.source_id = source_id
        self._secret = secret
        self._account_id = account_id
        self._title = title
        self._hook_api_version = hook_api_version
        self._id = id
        self._path = "/v2/origin/custom/"
        self._url = "https://amojo.amocrm.ru"
        self._content_type = "application/json"
        r = self._connect()
        if r.status_code == 200:
            self.scope_id = json.loads(r.text)["scope_id"]
        else:
            raise ValueError("Cant connect to amoChatApi")
    def __del__(self):
        self._disconnect()
    def _connect(self):
        connect_path = self._path + self._id + "/connect"
        connect_url = self._url + connect_path
        body = {
            "account_id": self._account_id,
            "title": self._title,
            "hook_api_version": "v2"
        }
        request_body = json.dumps(body)
        checksum = hashlib.md5(request_body.encode("utf-8")).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        str_to_sign = "\n".join(["POST", checksum, self._content_type, date, connect_path])
        signature = hmac.new(self._secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha1).hexdigest()
        headers = {
            "Date": date,
            "Content-Type": self._content_type,
            'Content-MD5': checksum,
            'X-Signature': signature,
        }
        response = requests.post(connect_url, data=request_body, headers=headers)
        return response

    def _disconnect(self):
        disconnect_path = self._path + self._id + "/disconnect"
        disconnect_url = self._url + disconnect_path
        body = {
            "account_id": self._account_id
        }
        request_body = json.dumps(body)
        checksum = hashlib.md5(request_body.encode("utf-8")).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        str_to_sign = "\n".join(["DELETE", checksum, self._content_type, date, disconnect_path])
        signature = hmac.new(self._secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha1).hexdigest()
        headers = {
            "Date": date,
            "Content-Type": self._content_type,
            'Content-MD5': checksum,
            'X-Signature': signature,
        }
        response = requests.delete(disconnect_url, data=request_body, headers=headers)
        return response

    def create_chat(self, conversation_id, user):
        create_chat_path = self._path + self._scope_id + "/chats"
        create_chat_url = self._url + create_chat_path
        body = {
            "conversation_id": conversation_id,
            "user": user,
            "account_id": self._account_id,
            "source": {
                "external_id": self.source_id
            }
        }
        request_body = json.dumps(body)
        checksum = hashlib.md5(request_body.encode("utf-8")).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        str_to_sign = "\n".join(["POST", checksum, self._content_type, date, create_chat_path])
        signature = hmac.new(self._secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha1).hexdigest()
        headers = {
            "Date": date,
            "Content-Type": self._content_type,
            'Content-MD5': checksum,
            'X-Signature': signature,
        }
        response = requests.post(create_chat_url, data=request_body, headers=headers)
        return response

    def send_or_edit_message(self, payload):
        user = {
            "id": payload["payload"]["sender"]["id"],
            "name":payload["payload"]["sender"]["name"]
        }
        r = self.create_chat(payload["payload"]["conversation_id"], user)
        send_or_edit_message_path = self._path + self._scope_id
        send_or_edit_message_url = self._url + send_or_edit_message_path
        request_body = json.dumps(payload)
        checksum = hashlib.md5(request_body.encode("utf-8")).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        str_to_sign = "\n".join(["POST", checksum, self._content_type, date, send_or_edit_message_path])
        signature = hmac.new(self._secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha1).hexdigest()
        headers = {
            "Date": date,
            "Content-Type": self._content_type,
            'Content-MD5': checksum,
            'X-Signature': signature,
        }
        response = requests.post(send_or_edit_message_url, data=request_body, headers=headers)
        response.raise_for_status()
        return response

    def change_message_status(self, msgid:str, delivery_status:int, error_code:int, error:str):
        path = self._path + self._scope_id + "/" + msgid + "/delivery_status"
        url = self._url + path
        body = {
            "msgid":msgid,
            "delivery_status":delivery_status,
            "error_code":error_code,
            "error":error
        }
        request_body = json.dumps(body)
        checksum = hashlib.md5(request_body.encode("utf-8")).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        str_to_sign = "\n".join(["POST", checksum, self._content_type, date, path])
        signature = hmac.new(self._secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha1).hexdigest()
        headers = {
            "Date": date,
            "Content-Type": self._content_type,
            'Content-MD5': checksum,
            'X-Signature': signature,
        }
        response = requests.post(url, data=request_body, headers=headers)
        response.raise_for_status()
        return response

    def create_new_text_message(self):
        return Payload(self)
    def create_new_photo_message(self):
        return Payload(self, "photo")

