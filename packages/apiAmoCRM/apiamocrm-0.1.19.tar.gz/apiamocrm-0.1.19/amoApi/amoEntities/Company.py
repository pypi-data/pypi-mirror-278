from amoApi.amoEntities.BaseEnity import BaseEnity


class Company(BaseEnity):
    def __init__(self, api = None, json = {}):
        self._api = api
        self._json = json
    def get_json(self):
        return self._json
    def from_json(self, json):
        self._json = json
    json = property(get_json, from_json)
    def get_id(self):
        return self._json.get("id")
    def set_id(self, id:int):
        self._json["id"] = id
    id = property(get_id, set_id)
    def get_name(self):
        return self._json.get("name")
    def set_name(self, name):
        self._json["name"] = name
    name = property(get_name, set_name)
    def get_responsible_user_id(self):
        return self._json.get("responsible_user_id")
    def set_responsible_user_id(self, id:int):
        self._json["responsible_user_id"] = id
    responsible_user_id = property(get_responsible_user_id, set_responsible_user_id)
    def get_group_id(self):
        return self._json.get("group_id")
    def set_group_id(self, id:int):
        self._json["group_id"] = id
    group_id = property(get_group_id, set_group_id)
    def get_created_by(self):
        return self._json.get("created_by")
    def set_created_by(self, id):
        self._json["created_by"] = id
    created_by = property(get_created_by, set_created_by)
    def get_updated_by(self):
        return self._json.get("updated_by")
    def set_updated_by(self, id:int):
        self._json["updated_by"] = id
    updated_by = property(get_updated_by, set_updated_by)
    def get_created_at(self):
        return self._json.get("created_at")
    def set_created_at(self, timestamp:int):
        self._json["created_at"] = timestamp
    created_at = property(get_created_at, set_created_at)
    def get_updated_at(self):
        return self._json.get("updated_at")
    def set_updated_at(self, timestamp:int):
        self._json["updated_at"] = timestamp
    updated_at = property(get_updated_at, set_updated_at)
    def get_closest_task_at(self):
        return self._json.get("closest_task_at")
    def set_closest_task_at(self, timestamp:int):
        self._json["closest_task_at"] = timestamp
    closest_tast_at = property(get_closest_task_at, set_closest_task_at)
    def get_is_deleted(self):
        if self._json.get("is_deleted"):
            return self._json.get("is_deleted")
        else:
            return False
    def set_is_deleted(self, state:bool):
        self.json["is_deleted"] = state
    is_deleted = property(get_is_deleted, set_is_deleted)
    def get_account_id(self):
        return self._json.get("account_id")
    def set_account_id(self, id:int):
        self._json["account_id"] = id
    account_id = property(get_account_id, set_account_id)
    def get_tags(self):
        from amoApi.amoEntities.Tag import Tag
        if self._json["_embedded"].get("tags") is None:
            return []
        return [Tag(self._api, json_tag) for json_tag in self._json["_embedded"]["tags"]]

    def get_contacts(self):
        from amoApi.amoEntities.Contact import Contact
        if self._json["_embedded"].get("contacts") is None:
            return []
        return [Contact(self._api, json_contact) for json_contact in self._json["_embedded"]["contacts"]]

    def get_leads(self):
        from amoApi.amoEntities.Lead import Lead
        if self._json["_embedded"].get("leads") is None:
            return []
        return [Lead(self._api, json_lead) for json_lead in self._json["_embedded"]["leads"]]