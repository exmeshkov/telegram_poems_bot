# - *- coding: utf- 8 - *-
import config
import telebot
from poems import get_random_poem_from_database
from telebot import types


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Случайное стихотворение')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!'.format(
        message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_poem(message):

    if message.chat.type == 'private':
        if message.text == 'Случайное стихотворение':
            bot.send_message(message.chat.id, get_random_poem_from_database())


bot.polling(none_stop=True)
