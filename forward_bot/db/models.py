import mongoengine as me
from .status import StatusOperation
from ..configs import NoValidationData

me.connect('forward_bot')


class User(me.Document):
    user_id = me.IntField(unique=True, required=True)
    name = me.StringField(max_length=255)
    telephone = me.StringField(min_length=10, max_length=12, regex='^[0-9]*$')
    status_operation = me.StringField(required=True, choices=StatusOperation.TITLES_CONSTANT)
    active_id_client = me.StringField(max_length=9)
    active_id_contact_person = me.StringField(max_length=9)
    authentication = me.BooleanField(default=False)
    admins_bot = me.ListField(me.StringField(min_length=9, max_length=20))
    role = me.ListField(me.StringField(min_length=10, max_length=10))

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_user(cls, chat):
        user = cls.objects(user_id=chat.id)

        if not user:
            try:
                name = chat.last_name + ' ' + chat.first_name
            except Exception:
                # Не знаю як зменшити Exception
                name = ""

            user = cls.objects.create(user_id=chat.id, name=name, status_operation=StatusOperation.NOT_OPERATION)
        else:
            user = user[0]
        return user

    def user_to_status(self, status, active_id_client='', active_id_contact_person=''):
        self.status_operation = status
        self.active_id_client = active_id_client
        self.active_id_contact_person = active_id_contact_person
        self.save()

    def set_info_from_user(self, message_1c):
        if not message_1c:
            raise NoValidationData

        self.authentication = message_1c.get("Authentication", False)
        self.admins_bot = message_1c.get("Admins", [])
        self.role = list(message_1c.get("Role", {}).keys())
        # self.save() - Зайве. Нам ця інформація потрібна тільки для сеансу. Між сеансами зберігати не потрібно

    @property
    def roles(self):
        return set(self.role)



class Partners(me.Document):
    id_client = me.StringField(unique=True, required=True, max_length=9)
    name = me.StringField(max_length=255)

    def __str__(self):
        return str(self.id_client)

    @classmethod
    def get_partner(cls, id_client):
        client = cls.objects(id_client=id_client)
        name_client = ''
        if client:
            name_client = client[0].name
        return name_client

    @classmethod
    def write_partner(cls, id_client, name):
        client = cls.objects(id_client=id_client)
        if client:
            client[0].name = name
            client[0].save()
        else:
            cls.objects.create(id_client=id_client, name=name)
