from abc import ABC
from email.utils import formatdate
from amoApi.API import API
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Dict
import os
from services.AbstractService import AbstractService
from amoChatApi.API import ChatApi


class DromApi(AbstractService, ABC):
    class Brief:
        def __init__(self, json_brief: Dict):
            try:
                self.json = json_brief
                self.id = json_brief["dialogId"]
                self.sender_nick = json_brief["interlocutor"]
                self.last_message_date = json_brief["lastMessageDate"]
                self.last_message = DromApi._get_text_message_by_brief(json_brief)
            except KeyError as e:
                raise ValueError(f"KeyError: {e} in {json_brief}")

    def __init__(self, cookies: Dict, url_field:int):
        if not os.path.exists("drom.txt"):
            open("drom.txt", "w+").close()
        self.cookies = cookies
        self._url_field = url_field

    def _get_briefs(self) -> List[Brief]:
        params = {
            'ajax': '1',
            'fromIndex': '0',
            'count': '50',
            'list': 'personal',
        }
        response = requests.get('https://my.drom.ru/personal/messaging/inbox-list', params=params, cookies=self.cookies)
        response.raise_for_status()
        briefs = []
        for json_brief in response.json().get("briefs"):
            try:
                briefs.append(DromApi.Brief(json_brief))
            except:
                print("Error to create brief", json_brief)
                pass
        return briefs

    @staticmethod
    def _get_text_message_by_brief(brief: Dict) -> str:
        soup = BeautifulSoup(brief["html"], "html.parser")
        latest_msg_div = soup.find("div", class_="dialog-brief__latest_msg")
        try:
            return latest_msg_div.text if latest_msg_div else ""
        except:
            return "Пользователь пытается отправить вам сообщения с Drom, ответьте ему или перезвоните"

    def send_message(self, dialog_id: int, text: str):
        params = {
            'dialogId': str(dialog_id),
            'flat-layout': 'false',
            'ajax': '1',
        }
        data = {'message': text}
        response = requests.post('https://baza.drom.ru/personal/messaging/view', params=params, cookies=self.cookies, data=data)
        response.raise_for_status()

    def receive_message(self, api: ChatApi, amo_api: API):
        briefs = self._get_briefs()
        messages = []
        for brief in briefs:
            if BeautifulSoup(brief.json["html"], "html.parser").find("i", class_="bzr-dialog__message-check"):
                continue
            info = self._get_brief_info(str(brief.id))
            dialog_id = "dlg_" + str(brief.id)
            str_message = f"Sender: {brief.sender_nick}\nMessage: {brief.last_message}\nDate: {brief.last_message_date}\nId: {dialog_id}"
            messages.append(str_message)

            with open("drom.txt", "r") as file:
                if str_message not in file.read().split("\n\n"):
                    p = api.create_new_text_message()
                    p.set_message_id(dialog_id + "_" + formatdate(timeval=None, localtime=False, usegmt=True))
                    p.set_conversation_id(dialog_id)
                    p.set_sender_id(dialog_id)
                    p.set_sender_name(brief.sender_nick)
                    p.message.set_text(brief.last_message)
                    r = p.send()
                    while amo_api.get_contact_links(chats_id=[json.loads(r.text)["new_message"]["conversation_id"]])["_total_items"] == 0:
                        pass
                    l = amo_api.get_contact_links(chats_id=[json.loads(r.text)["new_message"]["conversation_id"]])
                    params = {"with": "leads"}
                    contact = amo_api.get_contact(l["_embedded"]["chats"][0]["contact_id"], params=params)
                    lead = amo_api.get_lead(contact["_embedded"]["leads"][0]["id"])
                    try:
                        if not any(f["field_id"] == self._url_field for f in lead.get_json().get("custom_fields_values", [])):
                            self._patch_after_create(lead, info["url"], info["price"], info["title"])
                    except:
                        self._patch_after_create(lead, info["url"], info["price"], info["title"])
        with open("drom.txt", "w") as f:
            f.write("\n\n".join(messages))

    def _patch_after_create(self, lead, announcement_url, messagePrice, messageTitle):
        values = [{"value": announcement_url}]
        lead.set_custom_field(self._url_field, values)
        lead.set_price(int(messagePrice))
        lead.set_name(messageTitle)
        lead.patch()

    def _get_brief_info(self, brief_id: str) -> Dict:
        params = {
            'dialogId': brief_id,
            'json': 'true',
            'flat-layout': 'false',
            'ajax': '1',
        }

        response = requests.get('https://baza.drom.ru/personal/messaging/view', params=params, cookies=self.cookies)
        response.raise_for_status()
        json_r = response.json()
        header_html = json_r["header"]
        soup = BeautifulSoup(header_html, "html.parser")
        header = soup.find("h3", class_="bzr-dialog-header__sub-title")
        try:
            price_text = header.find("strong").text
        except:
            price_text = "0"
        message_price = "".join([ch for ch in price_text if ch.isdigit()])
        price = int(message_price)
        url = header.find("a").get("href")
        title = header.find("a").text
        return {"url": url, "title": title, "price": price}
