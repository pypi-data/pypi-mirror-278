import json
import requests
from email.utils import formatdate
import os
from amoChatApi.API import ChatApi
from amoApi.API import API
from abc import ABC
from services.AbstractService import AbstractService


class BibinetApi(AbstractService, ABC):
    def __init__(self, token: str, url_field:int):
        if not os.path.exists('bibinet.txt'):
            open('bibinet.txt', 'w+').close()
        self._token = token
        self._url_field = url_field

    def send_message(self, text: str, dialog_id: int) -> None:
        headers = {'authorization': self._token}
        json_data = {'message': text, 'files': []}
        response = requests.post(
            f'https://bibinet.ru/service/dialogs/add/message/{dialog_id}/',
            headers=headers,
            json=json_data
        )
        response.raise_for_status()

    def _get_messages(self) -> dict:
        headers = {'authorization': self._token}
        json_data = {'page': 1}
        response = requests.post('https://bibinet.ru/service/dialogs/', headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()

    def receive_message(self, chat_api: ChatApi, amo_api: API) -> None:
        try:
            response = self._get_messages()
        except requests.RequestException as e:
            print(f"Failed to get messages: {e}")
            return

        messages = []
        for mess in response.get("response", []):
            try:
                if mess.get("last_message", {}).get("user_type") == "recipient":
                    continue
            except KeyError:
                pass

            sender = mess["user_sender"]["first_name"]
            message = mess["message"].replace("\n", "")
            if "last_message" in mess:
                if mess["last_message"]["user_type"] == "recipient":
                    continue
                if mess["last_message"]["message_type"] == "text":
                    message = mess["last_message"]["message"]

            date_create = mess["date_create"]
            data_json = mess.get("data_json", {}).get("part", {}).get("data", {})
            mark = data_json.get("mark", {}).get("name", "")
            model = data_json.get("model", {}).get("name", "")
            part_type = data_json.get("part_type", {}).get("name", "")
            part_url = "https://bibinet.ru/part/" + mess.get("data_json", {}).get("part", {}).get("invnn", "")
            dialog_id = f"dlg_{mess['id']}"
            str_message = (
                f"Sender: {sender}\nMessage: {message}\nDate: {date_create}\n"
                f"Mark: {mark}\nModel: {model}\nPartType: {part_type}\nId: {dialog_id}"
            )
            messageTitle = f"{mark} {model} {part_type}"
            messages.append(str_message)

            with open("bibinet.txt", "r") as file:
                if str_message not in file.read().split("\n\n"):
                    p = chat_api.create_new_text_message()
                    p.set_message_id(dialog_id + "_" + formatdate(timeval=None, localtime=False, usegmt=True))
                    p.set_conversation_id(dialog_id)
                    p.set_sender_id(dialog_id)
                    p.set_sender_name(sender)
                    p.message.set_text(message)
                    r = p.send()
                    while True:
                        contact_links = amo_api.get_contact_links(
                            chats_id=[json.loads(r.text)["new_message"]["conversation_id"]]
                        )
                        if contact_links["_total_items"] > 0:
                            break
                    contact_link = contact_links["_embedded"]["chats"][0]
                    contact = amo_api.get_contact(contact_link["contact_id"], params={"with": "leads"})
                    lead = amo_api.get_lead(contact["_embedded"]["leads"][0]["id"])
                    try:
                        finded = any(f["field_id"] == self._url_field for f in lead.get_json().get("custom_fields_values", []))
                    except:
                        finded = False
                    if not finded:
                        self._patch_after_create(lead, part_url, 0, messageTitle)

        with open("bibinet.txt", "w") as f:
            f.write("\n\n".join(messages))

    def _patch_after_create(self, lead, announcement_url: str, messagePrice: int, messageTitle: str) -> None:
        values = [{"value": announcement_url}]
        lead.set_custom_field(self._url_field, values)
        lead.set_price(messagePrice)
        lead.set_name(messageTitle)
        lead.patch()
