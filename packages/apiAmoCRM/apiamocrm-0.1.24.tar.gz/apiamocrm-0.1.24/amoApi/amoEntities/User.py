from amoApi.amoEntities.BaseEnity import BaseEnity
import json


class User(BaseEnity):

    def __init__(self, api = None, json = {}):
        self._api = api
        self._json = json
    def get_json(self):
        return self._json
    def get_id(self):
        return self._json.get("id")
    def set_id(self, id:int):
        self._json["id"] = id
    def get_name(self):
        return self._json.get("name")
    def set_name(self, name:str):
        self._json["name"] = name
    def get_email(self):
        return self._json.get("email")
    def set_email(self, email:str):
        self._json["email"] = email
    def get_rights(self):
        return self._json.get("rights")