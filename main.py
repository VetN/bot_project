import telebot
#  from config import *
from classbot import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_exchange(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username},введите команду:\n"
                          f"<с какой валюты>\n<в какую валюту>\n<сумму>\n Список валют /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    if len(values) > 3:
        raise ConvertionException("Неправильный ввод данных")
    quote, base, amount = values
    total_base = Exchange.convert(quote, base, amount)
    text = f'Цена {amount} {quote} к {base} -{total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()
