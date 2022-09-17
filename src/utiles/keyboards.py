from telebot import types
from types import SimpleNamespace
import emoji



keys = SimpleNamespace(
   random_connect = ":busts_in_silhouette: Random Connect",
   setting = ":wrench: Setting",
)


def create_keyboard(keys, row_width=2, resize_keyboard=True):
    """
    creating kebored

    example :
    keys = ["a", "b", "c"]
    """

    markup = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
    keys = map(emoji.emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup.add(*buttons)
    return markup


keyboards = SimpleNamespace(
    main = create_keyboard([keys.random_connect, keys.setting])
)
