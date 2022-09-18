import telebot
from src.utiles.io import write_json
from telebot import types
from src.utiles.keyboards import create_keyboard, keyboards
import emoji
from src.bot import bot
from src.filters import IsAdmin




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


		@self.bot.message_handler(is_admin=True)
		def admin_of_group(message):
			self.bot.send_message(message.chat.id, 'You are admin of this group!')


		@self.bot.message_handler(func=lambda m: True)
		def echo_all(message):
			#write_json(message.json , "message.json")
			#print(emoji.demojize(message.text))
			self.bot.send_message(message.chat.id, str(message.text), reply_markup=keyboards.main)



if __name__ == "__main__":
	bot1 = Bot(tele_bot=bot)
	bot1.run()
