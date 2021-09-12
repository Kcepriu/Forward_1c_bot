import requests
import codecs
import json

from ..db import User

class HTTP_1C():
    def __init__(self, *arg):
        (self.USER_1C,
         self.PASSWD_1C,
         self.NAME_BOT,
         self.NAME_SERVER,
         self.ADDITIONAL_ADRESS) = arg


    def URL(self, user: User, name_operation):
        # http://172.30.222.101/Test7/hs/bot1c/1c_forward/555666888

        url = f'http://{self.NAME_SERVER}/{self.ADDITIONAL_ADRESS}/{self.NAME_BOT}/{user.user_id}/{name_operation}'
        return url

    def get_autentification_1c(self, user: User):
        # /{NameBot}/{User}/autentification?username=testSergiy
        url = self.URL(user, "autentification")
        payload = {"username": User.name}
        print(22222)
        r = requests.get(url, auth=(self.USER_1C, self.PASSWD_1C), params=payload)

        print(r.text)
        decoded_data = codecs.decode(r.text.encode(), 'utf-8-sig')

        return json.loads(decoded_data)

    def get_find_contrahents(self, user: User, name_contrahent):
        #/{NameBot}/{User}/contrahens?name=веранда

        url = self.URL(user, "contrahens")
        payload = {"username": user.name, "name": name_contrahent}
        r = requests.get(url, auth=(self.USER_1C, self.PASSWD_1C), params=payload)

        decoded_data = codecs.decode(r.text.encode(), 'utf-8-sig')
        return json.loads(decoded_data)


    def get_information_contrahent(self, user: User, id_contrahents):
        # /{NameBot}/{User}/contrahens?id=000053338&username=testSergiy

        url = self.URL(user, "contrahens")
        payload = {"username": user.name, "id": id_contrahents}

        r = requests.get(url, auth=(self.USER_1C, self.PASSWD_1C), params=payload)

        decoded_data = codecs.decode(r.text.encode(), 'utf-8-sig')
        return json.loads(decoded_data)

