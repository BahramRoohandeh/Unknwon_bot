import emoji
import telebot
from telebot import types

from src.bot import bot
from src.filters import IsAdmin
from src.utiles.io import write_json
from src.utiles.keyboards import create_keyboard, keyboards, keys, states
from src.db import db


class Bot:
    def __init__(self, tele_bot):

        #defining bot
        self.bot = tele_bot


        #adding filter
        self.bot.add_custom_filter(IsAdmin())

        #register handling
        self.handlers()


        #running but
        self.bot.infinity_polling()



    def handlers(self):

        @bot.message_handler(commands=['start'])
        def start(message):
            self.send_message(message.chat.id, f"hello {message.chat.username}")


            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
            )
            self.update_state(message.chat.id, states.main)


        @self.bot.message_handler(regexp = emoji.emojize(keys.random_connect))
        def rnadom_connect(message):
            self.send_message(message.chat.id, 'connecting to a random stranger....',reply_markup =keyboards.exit )
            self.update_state(message.chat.id, states.random_connect)
            other_user = db.users.find_one(
                {'state' : states.random_connect,
                'chat.id':{'$ne': message.chat.id}
                },
                )

            if not other_user:
                return


            #state update for both two users and messaging them
            self.update_state(message.chat.id, states.connected)
            self.send_message(message.chat.id, f"You are connected to {other_user['chat']['first_name']}")

            self.update_state(other_user["chat"]["id"], states.connected)
            self.send_message(other_user["chat"]["id"], f"You are connected to {message.chat.username}")

            #storing connection informations
            db.users.update_one(
                {'chat.id':message.chat.id},
                {'$set': {'connected_to' : other_user['chat']['id']}}
            )

            db.users.update_one(
                {'chat.id':other_user['chat']['id']},
                {'$set': {'connected_to' : message.chat.id}}
            )


        @self.bot.message_handler(regexp = emoji.emojize(keys.exit))
        def exit(message):
            self.send_message(message.chat.id, 'Connection terminated',reply_markup =keyboards.main )
            self.update_state(message.chat.id, states.main)


            #finding connected to ..
            connected_to = db.users.find_one(
                {'chat.id':message.chat.id}
            )['connected_to']

            print(connected_to)

            if not connected_to:
                return

            other_chat_id = connected_to
            #updating stateand messaging to connected to
            #if not connected_to:
               # return

            self.update_state(other_chat_id, states.main)
            self.send_message(other_chat_id, "Connection terminated by stranger",reply_markup =keyboards.main)


            #removing connected to
            db.users.update_one(
                {'chat.id':message.chat.id},
                {'$set': {'connected_to' : None}}
            )

            db.users.update_one(
                {'chat.id':connected_to},
                {'$set': {'connected_to' : None}}
            )




        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 'You are admin of this group!')


        @self.bot.message_handler(func=lambda m: True)
        def echo_all(message):

            user = db.users.find_one(
                {'chat.id' : message.chat.id}
            )

            if ((not user) or (user['state'] != states.connected) or (user['connected_to'] is None)):

                print(True)
                return


            self.send_message(user['connected_to'], message.text)



    def update_state(self, chat_id, state):
        db.users.update_one(
            {'chat.id' : chat_id},
            {'$set' : {'state': state}}
        )





    def send_message(self, chat_id, text, reply_markup=None, emojize=True):

        if emojize == True:
            text = emoji.emojize(text)


        self.bot.send_message(chat_id, text, reply_markup = reply_markup)


if __name__ == "__main__":
    bot1 = Bot(tele_bot=bot)
  

