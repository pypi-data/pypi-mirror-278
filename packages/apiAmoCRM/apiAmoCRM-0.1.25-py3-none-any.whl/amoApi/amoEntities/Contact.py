import json
from typing import List
from amoApi.amoEntities.BaseEnity import BaseEnity


class Contact(BaseEnity):
    def __init__(self, api = None, json_contact:json = {}):
        self._json = json_contact
        self._api = api

    def from_json(self, json_contact:json):
        self._json = json_contact
        return self

    def set_id(self, id:str):
        self._json["id"] = id

    def get_id(self):
        return self._json.get("id")

    def set_name(self, name:str):
        self._json["name"] = name

    def get_name(self):
        return self._json.get("name")

    def set_first_name(self, first_name:str):
        self._json["first_name"] = first_name

    def get_first_name(self):
        return self._json.get("first_name")

    def set_last_name(self, last_name:str):
        self._json["last_name"] = last_name

    def get_last_name(self):
        return self._json.get("last_name")

    def set_responsible_user_id(self, responsible_user_id:str):
        self._json["responsible_user_id"] = responsible_user_id

    def get_responsible_user_id(self):
        return self._json.get("responsible_user_id")

    def set_group_id(self, group_id:str):
        self._json["group_id"] = group_id

    def get_group_id(self):
        return self._json.get("group_id")

    def set_created_by(self, created_by:str):
        self._json["created_by"] = created_by

    def get_created_by(self):
        return self._json.get("created_by")

    def set_updated_by(self, updated_by:str):
        self._json["updated_by"] = updated_by

    def get_updated_by(self):
        return self._json.get("updated_by")

    def set_created_at(self, created_at:str):
        self._json["created_at"] = created_at

    def get_created_at(self):
        return self._json.get("created_at")

    def set_updated_at(self, updated_at:str):
        self._json["updated_at"] = updated_at

    def get_updated_at(self):
        return self._json.get("updated_at")

    def set_is_deleted(self, is_deleted:str):
        self._json["is_deleted"] = is_deleted

    def get_is_deleted(self):
        return self._json.get("is_deleted")

    def set_closest_task_at(self, closest_task_at:str):
        self._json["closest_task_at"] = closest_task_at

    def get_closest_task_at(self):
        return self._json.get("closest_task_at")

    def set_account_id(self, account_id:str):
        self._json["account_id"] = account_id

    def get_account_id(self):
        return self._json.get("account_id")

    def set_custom_field(self, id:int, values):
        if not self._json.get("custom_fields_values"):
            self._json["custom_fields_values"] = []
        field = {
            "field_id": id,
            "values": values
        }
        for i in range(0, len(self._json["custom_fields_values"])):
            if self._json["custom_fields_values"][i]["field_id"] == id:
                self._json["custom_fields_values"][i]["values"] = values
                return
        self._json["custom_fields_values"].append(field)
    def get_custom_fiedls(self):
        return self._json.get("custom_fields_values")
    def get_leads(self) -> List["Lead"]:
        if not self._json["_embedded"].get("leads") is None:
            ids = [json_lead["id"] for json_lead in self._json["_embedded"].get("leads")]
            params = {"filter[id][]":ids}
            leads = self._api.get_leads(params=params)
            return leads
        else:
            return []

    def get_tags(self):
        from amoApi.amoEntities.Tag import Tag
        return [Tag(self.api, json_tag) for json_tag in self._json["_embedded"]["tags"]]

    def get_json(self):
        return self._json
    def patch(self):
        return self._api.patch_contact(self)