from flask import Flask
from forward_bot.bot import bot_instance
#from forward_bot.bot import bot_app

#app = Flask(__name__)
#app.register_blueprint(bot_app)



if __name__ == '__main__':
     bot_instance.polling()

    # print(bot_instance.get_me())
    # bot_instance.get_file()

    #bot_instance.test_add()

