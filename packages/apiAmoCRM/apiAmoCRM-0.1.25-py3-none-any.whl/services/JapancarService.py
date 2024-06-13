import time
import os.path
import requests
from bs4 import BeautifulSoup
from email.utils import formatdate
import json
from amoChatApi.API import ChatApi
from amoApi.API import API
import settings
from services.AbstractService import AbstractService
from abc import ABC


class JapancarApi(AbstractService, ABC):
    def __init__(self, cookies: dict, url_field:int):
        if not os.path.exists('japancar.txt'):
            open('japancar.txt', 'w+')
        self.cookies = cookies
        self._url_field = url_field

    def send_message(self, mess: str, dialog_id: int):
        params = {
            'dlg': str(id),
        }
        html = requests.get('https://japancar.ru/user/messaging/?dlg=' + str(dialog_id), cookies=self.cookies).text
        soup = BeautifulSoup(html, "html.parser")
        value = soup.find("input")["value"]
        data = {
            'action': 'add',
            'msg': mess,
            'param': value
        }
        response = requests.post('https://japancar.ru/ajx/msg/', cookies=self.cookies, data=data)

    def receive_message(self, api: ChatApi, amo_api: API):
        html = self._get_html_messages()
        soup = BeautifulSoup(html, "html.parser")
        messages = soup.findAll("div", class_="message-preview-block")
        messagesStr = []
        for mess in messages:
            announcement_url = self._get_announcement_url(mess.findAll("a")[0].get("href"))
            message_dialog_id = mess.findAll("a")[0].get("href").replace("?", "").replace("=", "_")
            dialog_url = "https://japancar.ru/user/messaging/" + message_dialog_id
            message_title = mess.find("div", class_="title").text
            message_price = mess.find("div", class_="data").text
            message_text = mess.find("p", class_="pt-2").text
            if not "Вы" in message_text:
                tmp = message_price
                message_price = ""
                nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                for ch in tmp:
                    if ch in nums:
                        message_price += ch
                message_sender_nick = message_text.split(":")[0].replace("\n", "")
                message_text = message_text.replace(message_sender_nick + ":\n", "")
                message_text = message_text.replace("\n", "")
                if len(message_sender_nick) == 0:
                    message_sender_nick = "Клиент с Japancar"
                message_to_send = ("Title:" + message_title +
                                   "\nPrice:" + message_price + "\nNick:" +
                                   message_sender_nick + "\nMessage:" + message_text +
                                   "\nDialog:" + dialog_url)
                messagesStr.append(message_to_send)
                with open("japancar.txt", "r") as file:
                    if not message_to_send in file.read().split("\n\n"):
                        p = api.create_new_text_message()
                        p.set_message_id(
                            message_dialog_id + "_" + str(formatdate(timeval=None, localtime=False, usegmt=True)))
                        p.set_conversation_id(message_dialog_id)
                        p.set_sender_id(message_dialog_id)
                        p.set_sender_name(message_sender_nick)
                        p.message.set_text(message_text)
                        r = p.send()
                        while (amo_api.get_contact_links(
                                chats_id=[json.loads(r.text)["new_message"]["conversation_id"]])[
                                   "_total_items"] == 0): pass
                        l = amo_api.get_contact_links(chats_id=[json.loads(r.text)["new_message"]["conversation_id"]])
                        params = {"with": "leads"}
                        contact = amo_api.get_contact(l["_embedded"]["chats"][0]["contact_id"], params=params)
                        lead = amo_api.get_lead(contact["_embedded"]["leads"][0]["id"])
                        finded = False
                        try:
                            for f in lead.get_json()["custom_fields_values"]:
                                if f["field_id"] == self._url_field:
                                    finded = True
                                    break
                            if not finded:
                                self._patch_after_create(lead, announcement_url, message_price, message_title)
                        except:
                            self._patch_after_create(lead, announcement_url, message_price, message_title)
        with open("japancar.txt", "w+") as f:
            s = ""
            for mess in messagesStr:
                s += mess + "\n\n"
                f.write(s)

    def _get_html_messages(self):
        response = requests.get('https://japancar.ru/user/messaging/', cookies=self.cookies)
        return response.text

    def _get_announcement_url(self, dlg: str):
        response = requests.get('https://japancar.ru/user/messaging/' + dlg, cookies=self.cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        preview = soup.find("div", class_="message-preview-block")
        a_arr = preview.findAll("a")
        for a in a_arr:
            try:
                return a.get("href")
            except:
                pass

    def _patch_after_create(self, lead, announcement_url, messagePrice, messageTitle):
        values = [{"value": announcement_url}]
        lead.set_custom_field(self._url_field, values)
        lead.set_price(int(messagePrice))
        lead.set_name(messageTitle)
        lead.patch()
