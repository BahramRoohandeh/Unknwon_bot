
import telebot
import os


bot = telebot.TeleBot(os.environ["bot_token"] , parse_mode=None )