from amoApi.amoEntities.BaseEnity import BaseEnity
import json


class CustomField(BaseEnity):
    def __init__(self, api = None, json_field:json = {}):
        self._json = json_field
        self._api = api

    def from_json(self, json_field:json):
        self._json = json_field
        return self

    def get_json(self):
        return self._json

    def get_id(self) -> int:
        return self._json.get("id")

    def set_id(self, id:int):
        self._json["id"] = id

    def get_type(self) -> str:
        return self._json.get("type")

    def set_type(self, type:str):
        self._json["type"] = type

    def get_name(self) -> str:
        return self._json.get("name")

    def set_name(self, name:str):
        self._json["name"] = name

    def get_code(self) -> str:
        return self._json.get("code")

    def set_code(self, code:str):
        self._json["code"] = code

    def get_sort(self):
        return self._json.get("sort")

    def set_sort(self, sort:int):
        self._json["sort"] = sort

    def get_group_id(self) -> int:
        return self._json.get("group_id")

    def set_group_id(self, group_id:int):
        self._json["group_id"] = group_id

    def is_api_only(self):
        return self._json.get("is_api_only")