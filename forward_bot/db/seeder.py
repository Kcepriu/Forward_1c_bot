from models import Text

list_text = [
        {
            'title': 'start_message',
            'body': 'Вітаємо. Ви підключилися до бота зберігання скана документів'
        },
        {
            'title': 'others_message',
            'body': 'Бот опрацьовує лише надіслані файли'
        },
        {
            'title': 'photo_message',
            'body': 'Файли надіслані як фото не опрацьовуються. '
                    'У них мала роздільна здатність. Бот не може розпізнати QR код. '
                    'Надішліть зображення як файл.'
        },
        {
            'title': 'document_message',
            'body': 'Опрацьовуємо документ '
        },
        {
            'title': 'document_message_not_type_message',
            'body': 'Надісланий документ не являється файлом зображень.'
        }
    ]

Text.drop_collection()

for item in list_text:
    print(item['title'])
    Text.objects.create(**item)