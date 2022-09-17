import telebot
import os
from src.utiles.io import write_json
from telebot import types
from src.utiles.keyboards import create_keyboard, keyboards
import emoji


class Bot:
	def __init__(self):
		self.bot = telebot.TeleBot("5677978685:AAHW7RuuniCaJQgStKHucealE11zc6Prh-g" , parse_mode=None )
		self.echo_all = self.bot.message_handler(func=lambda m: True)(self.echo_all)

	def run(self):
		self.bot.infinity_polling()

	def echo_all(self, message):
		#write_json(message.json , "message.json")
		print(emoji.demojize(message.text))
		self.bot.send_message(message.chat.id, str(message.text), reply_markup=keyboards.main)



if __name__ == "__main__":
	bot1 = Bot()
	bot1.run()
