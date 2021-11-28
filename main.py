from flask import Flask
from forward_bot.bot import bot_instance
from forward_bot.bot import bot_app
from forward_bot.configs import WEBHOOK_URL


#app = Flask(__name__)
#app.register_blueprint(bot_app)

if __name__ == '__main__':
     bot_instance.remove_webhook()
     bot_instance.polling()

     # bot_instance.remove_webhook()
     # time.sleep(2)
     # a = bot_instance.set_webhook(
     #    url=WEBHOOK_URL,
     #    certificate=open('webhook_cert.pem', 'r')
     # )
     #
     # app.run(host="172.40.99.100")


