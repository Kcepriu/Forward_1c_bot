import requests
import codecs
import json

from ..db import User
from ..configs import NoConnectionWith1c


class Http1c:
    def __init__(self, *arg):
        (self.USER_1C,
         self.PASSWD_1C,
         self.NAME_BOT,
         self.NAME_SERVER,
         self.ADDITIONAL_ADDRESS) = arg

    @staticmethod
    def decoder_to_json(data):
        try:
            decoded_data = codecs.decode(data, 'utf-8-sig')
        except ValueError:
            raise NoConnectionWith1c

        return json.loads(decoded_data)

    def get_url(self, user: User, name_operation):
        # http://172.30.222.101/Test7/hs/bot1c/1c_forward/555666888
        url = f'http://{self.NAME_SERVER}/{self.ADDITIONAL_ADDRESS}/{self.NAME_BOT}/{user.user_id}/{name_operation}'
        return url

    def get_request(self, url, payload):
        try:
            r = requests.get(url, auth=(self.USER_1C, self.PASSWD_1C), params=payload)
        except ConnectionError:
            raise NoConnectionWith1c

        if r.status_code != 200:
            raise NoConnectionWith1c

        return self.decoder_to_json(r.text.encode())

    def post_request(self, url, payload, data):
        try:
            r = requests.post(url, auth=(self.USER_1C, self.PASSWD_1C), params=payload, json=data)
        except ConnectionError:
            raise NoConnectionWith1c

        if r.status_code != 200:
            raise NoConnectionWith1c

        return self.decoder_to_json(r.text.encode())

    def get_authentication_1c(self, user: User):
        # /{NameBot}/{User}/authentication?username=testSergiy
        url = self.get_url(user, "authentication")
        payload = {"username": user.name}
        return self.get_request(url, payload)

    # Запит на пошук контрагента в 1с
    def get_find_partner(self, user: User, name_partner):
        # /{NameBot}/{User}/partner?name=веранда
        url = self.get_url(user, "partner")
        payload = {"username": user.name, "name": name_partner}

        return self.get_request(url, payload)

    def get_information_partner(self, user: User, id_partner):
        # /{NameBot}/{User}/partner?id=000053338&username=testSergiy
        url = self.get_url(user, "partner")
        payload = {"username": user.name, "id": id_partner}

        return self.get_request(url, payload)

    def post_event(self, user: User, text_event):
        # /{NameBot}/{User}/event
        url = self.get_url(user, "event")
        payload = {"id": user.active_id_client,
                   "id_person": user.active_id_contact_person}
        data = {'text': text_event}

        return self.post_request(url, payload, data)

    def get_events(self, user: User, id_partners, company):
        # /{NameBot}/{User}/partner?id=000053338&username=testSergiy
        url = self.get_url(user, "event")
        payload = {"company": company, "id": id_partners}

        return self.get_request(url, payload)

    def get_contact_person(self, user: User, id_partners):
        # /{NameBot}/{User}/partner?id=000053338&username=testSergiy
        url = self.get_url(user, "contact_person")
        payload = {"username": user.name, "id": id_partners}

        return self.get_request(url, payload)
