from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from ..db import User, ScanDocument, Text

class SaveDocumentBot(TeleBot):
    # Відправляє повідомлення
    def send_message_from_type(self, user: User, type_message: Text.TITLES_CONSTANT):
        text = Text.get_body(type_message)
        result = self.send_message(user.user_id, text)
        return result

    # Створює документ в базі, на основі отрманого повідомлення
    def add_document(self, user: User, message):
        document = ScanDocument.add_document(user, message.document)
        self.get_url_file(document)
        return document

    # отримуємо урл файла і зберігаємо його в базі
    def get_url_file(self, document: ScanDocument):
        try:
            message = self.get_file(document.file_id)
        except ApiTelegramException:
            return

        document.file_path = message.file_path
        self.get_data_file(document, False)
        document.save()
        return True

    # Отримуємо дані файлу із нету і зберігаємо в базі
    def get_data_file(self, document, save=True):
        if not document.file_path:
            return

        file = self.download_file(document.file_path)

        document.data_file.put(file, content_type='image/jpeg')
        if save:
            document.save()



#------------------------------------------
    def test_add(self):
        doc = ScanDocument.objects(id='5fa40e4a60db69abd73fd0a0').get()
        if doc:
            self.get_data_file(doc)

            print('OK')


if __name__ == '__main__':
   pass




