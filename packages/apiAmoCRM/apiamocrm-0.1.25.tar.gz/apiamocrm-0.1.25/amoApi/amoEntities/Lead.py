import json
from typing import List
from amoApi.amoEntities.BaseEnity import BaseEnity


class Lead(BaseEnity):
    def __init__(self, api=None, json_lead:json = {}):
        self._json_lead = json_lead
        self.api = api

    def add_text_note(self, text: str):
        self.api.add_lead_text_note(lead=self, text=text)

    def from_json(self, json: json):
        self._json_lead = json

    def set_id(self, id: int):
        self._json_lead["id"] = id

    def set_name(self, name: str):
        self._json_lead["name"] = name

    def set_price(self, price: int):
        self._json_lead["price"] = price

    def set_status_id(self, status_id: int):
        self._json_lead["status_id"] = status_id

    def set_pipeline_id(self, pipeline_id: int):
        self._json_lead["pipeline_id"] = pipeline_id

    def set_created_by(self, created_by: int):
        self._json_lead["created_by"] = created_by

    def set_updated_by(self, updated_by: int):
        self._json_lead["updated_by"] = updated_by

    def set_closed_at(self, closed_at: int):
        self._json_lead["closed_at"] = closed_at

    def set_created_at(self, created_at: int):
        self._json_lead["created_at"] = created_at

    def set_updated_at(self, updated_at: int):
        self._json_lead["updated_at"] = updated_at

    def set_loss_reason_id(self, loss_reason_id: int):
        self._json_lead["loss_reason_id"] = loss_reason_id

    def set_responsible_user_id(self, responsible_user_id: int):
        self._json_lead["responsible_user_id"] = responsible_user_id
    def set_custom_field(self, id:int, values):
        if not self._json_lead.get("custom_fields_values"):
            self._json_lead["custom_fields_values"] = []
        field = {
            "field_id": id,
            "values": values
        }
        for i in range(0, len(self._json_lead["custom_fields_values"])):
            if self._json_lead["custom_fields_values"][i]["field_id"] == id:
                self._json_lead["custom_fields_values"][i]["values"] = values
                return
        self._json_lead["custom_fields_values"].append(field)
    def get_tags(self):
        from amoApi.amoEntities.Tag import Tag
        return [Tag(self.api, json_tag) for json_tag in self._json_lead["_embedded"]["tags"]]
    
    # Getters
    def get_id(self) -> int:
        return self._json_lead.get("id")

    def get_name(self) -> str:
        return self._json_lead.get("name")

    def get_price(self) -> int:
        return self._json_lead.get("price")

    def get_status_id(self) -> int:
        return self._json_lead.get("status_id")

    def get_pipeline_id(self) -> int:
        return self._json_lead.get("pipeline_id")

    def get_created_by(self) -> int:
        return self._json_lead.get("created_by")

    def get_updated_by(self) -> int:
        return self._json_lead.get("updated_by")

    def get_closed_at(self) -> int:
        return self._json_lead.get("closed_at")

    def get_created_at(self) -> int:
        return self._json_lead.get("created_at")

    def get_updated_at(self) -> int:
        return self._json_lead.get("updated_at")

    def get_loss_reason_id(self) -> int:
        return self._json_lead.get("loss_reason_id")

    def get_responsible_user_id(self) -> int:
        return self._json_lead.get("responsible_user_id")

    def get_json(self) -> json:
        return self._json_lead

    def get_contacts(self):
        params = {
            "with": "contacts"
        }
        me = self.api.get_lead(self.get_id(), params=params)
        contacts_ids = []
        for contact_json in me.get_json()["_embedded"]["contacts"]:
            contacts_ids.append(contact_json["id"])
        params = {
            "filter[id][]": contacts_ids
        }
        return self.api.get_contacts(params=params)
    def patch(self):
        self.api.patch_lead(self)
