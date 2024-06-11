import requests
from amoApi.amoEntities.Lead import Lead
import json
from typing import List
from amoApi.amoEntities.Contact import Contact


class API:
    def __init__(self, token:str, url:str):
        self._auth(token, url)

    def _delete(self, method: str, headers=None, body=None) -> json:
        if body is None:
            body = {}
        if headers is None:
            headers = {}
        if not self._token:
            raise ValueError("Not authorized!")
        headers["Authorization"] = "Bearer " + self._token
        r = requests.delete("https://" + self._suburl + ".amocrm.ru/api/v4/" + method,
                          headers=headers, json=body)
        if r.status_code != 200:
            raise ValueError(r.status_code, r.text)
        return json.loads(r.text)
    def _get(self, method, headers=None, parameters=None) -> json:
        if headers is None:
            headers = {}
        if parameters is None:
            parameters = {}
        if not self._token:
            raise ValueError("Not authorized!")
        headers["Authorization"] = "Bearer " + self._token
        r = requests.get("https://" + self._suburl + ".amocrm.ru/api/v4/" + method,
                         headers=headers, params=parameters)
        if r.status_code != 200:
            if r.status_code == 204:
                raise ValueError("Not found!")
            raise ValueError(r.status_code, r.text)
        return json.loads(r.text)

    def _post(self, method: str, headers=None, body=None) -> json:
        if body is None:
            body = {}
        if headers is None:
            headers = {}
        if not self._token:
            raise ValueError("Not authorized!")
        headers["Authorization"] = "Bearer " + self._token
        r = requests.post("https://" + self._suburl + ".amocrm.ru/api/v4/" + method,
                          headers=headers, json=body)
        if r.status_code != 200:
            raise ValueError(r.status_code, r.text)
        return json.loads(r.text)

    def _patch(self, method, headers=None, body=None) -> json:
        if headers is None:
            headers = {}
        if body is None:
            body = {}
        if not self._token:
            raise ValueError("Not authorized!")
        headers["Authorization"] = "Bearer " + self._token
        r = requests.patch("https://" + self._suburl + ".amocrm.ru/api/v4/" + method,
                           headers=headers, json=body)
        if r.status_code != 200:
            raise ValueError(r.status_code, r.text)
        return json.loads(r.text)

    def _auth(self, token, url):
        headers = {"Authorization": "Bearer " + token}
        r = requests.get("https://" + url + ".amocrm.ru/api/v4/leads", headers=headers)
        if r.status_code == 200:
            self._token = token
            self._suburl = url
            self._url = "https://" + url + ".amocrm.ru/api/v4/"
        else:
            raise ValueError("Bad auth!")

    def get_lead(self, id: int, params = {}) -> Lead:
        try:
            r = self._get("leads/" + str(id), parameters=params)
            lead = Lead(self)
            lead.from_json(r)
            return lead
        except Exception as e:
            return None

    def get_leads(self, params: dict = {}) -> List[Lead]:
        leads = []
        response_leads = self._get("leads", parameters=params)
        if len(response_leads) == 0:
            return leads
        for lead in response_leads["_embedded"]["leads"]:
            l = Lead(self)
            l.from_json(lead)
            leads.append(l)
        return leads

    def complex_create_lead(self, body=None, contacts=None, fields=None) -> Lead:
        if body is None:
            body = [{}]
        if contacts is None:
            contacts = [{}]
        if fields is None:
            fields = [{}]
        body[0]["custom_fields_values"] = fields
        body[0]["_embedded"] = {}
        body[0]["_embedded"]["contacts"] = contacts
        headers = {"Authorization": "Bearer " + self._token}
        r = requests.post(self._url + "leads/complex", json=body, headers=headers)
        lead = Lead()
        lead.id = json.loads(r.text)[0]["id"]
        return lead
    def get_contact(self, id:int, params:dict = {}):
        params["with"] = "leads"
        contact = Contact(self, self._get("contacts/" + str(id), parameters=params))
        return contact
    def get_contacts(self, params:dict = {}):
        return [Contact(self, json_contact) for json_contact in self._get("contacts", parameters=params)["_embedded"]["contacts"]]
    def get_contact_links(self, contacts_id: List[int] = None, chats_id: List[str] = None):
        params = {}
        if not contacts_id is None:
            params["contact_id"] = contacts_id
        if not chats_id is None:
            params["chat_id"] = chats_id
        return self._get("contacts/chats", parameters=params)
    def get_lead_links(self, lead_id):
        return self._get("/api/v4/leads/" + str(lead_id) + "/links")
    def create_lead(self, params: dict = [{}]) -> Lead:
        r = self._post("leads", body=params)
        lead = Lead(self)
        lead.from_json(r["_embedded"]["leads"][0])
        return lead
    def patch_lead(self, lead:Lead):
        body = lead.get_json()
        try:
            for i in range(0, len(body["_embedded"]["tags"])):
                try:
                    body["_embedded"]["tags"][i].pop("color")
                except:
                    pass
        except:
            pass
        try:
            for i in range(0, len(body["_embedded"]["contacts"])):
                try:
                    body["_embedded"]["contacts"][i].pop("_links")
                except:
                    pass
        except:
            pass
        return self._patch("leads/"+str(lead.get_id()), body=lead.get_json())

    def patch_contact(self, contact:Contact):
        body = contact.get_json()
        try:
            for i in range(0, len(body["_embedded"]["tags"])):
                try:
                    body["_embedded"]["tags"][i].pop("color")
                except:
                    pass
        except:
            pass
        try:
            for i in range(0, len(body["_embedded"]["contacts"])):
                try:
                    body["_embedded"]["contacts"][i].pop("_links")
                except:
                    pass
        except:
            pass
        return self._patch("contacts/" + str(contact.get_id()), body=contact.get_json())
    def add_lead_text_note(self, lead: Lead, text: str):
        body = [{}]
        body[0]["entity_id"] = lead.get_id()
        body[0]["note_type"] = "common"
        body[0]["params"] = {"text": text}
        r = self._post(method="leads/notes", body=body)

    def create_source(self, name:str, id:str):
        body = [{"name":name, "external_id": id}]
        return self._post("sources", body=body)
    def delete_source(self, id:int):
        body = [{"id":id}]
        return self._delete("sources", body=body)
    def get_sources(self):
        return self._get("sources")
    def get_users(self):
        from amoApi.amoEntities.User import User
        return [User(self, json) for json in self._get("users")["_embedded"]["users"]]

    def get_companies(self, params = {}):
        from amoApi.amoEntities.Company import Company
        return [Company(self, json) for json in self._get("companies", parameters=params)["_embedded"]["companies"]]

    def get_company(self, id:int):
        from amoApi.amoEntities.Company import Company
        return Company(self, self._get("companies/"+str(id)))