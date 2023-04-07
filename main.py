import telebot
from classbot import *
from config import *
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_hello(message: telebot.types.Message):
    bot.reply_to(message, f"Привет,{message.chat.username}!\n"
                          f"Я могу помочь тебе перевести валюту\n"
                          f"обмен валюты /change\n"
                          f"список валют возможных для перевода /look\n"
                          f"помощь /help")


@bot.message_handler(commands=['help'])
def start_help(message: telebot.types.Message):
    bot.reply_to(message, f"для корректной работы необходимо вводить название валют через пробел\n"
                          f"пример: доллар евро 100\n"
                          f"обмен валюты /change\n"
                          f"список валют возможных для перевода /look")


@bot.message_handler(commands=['change'])
def start_exchange(message: telebot.types.Message):
    bot.reply_to(message, f"\nВведите данные через пробел:\n"
                          f"<перевод с какой валюты>\n<в какую валюту>\n<сумму>\n"
                          f" Список валют возможных для перевода /help")


@bot.message_handler(commands=['look'])
def list_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        parametr = message.text.split()
        if len(parametr) > 3:
            raise ConvertionException("Неправильный ввод данных")
        quote, base, amount = parametr
        total_base = Exchange.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    else:

        text = f'{amount} {keys.get(quote)} стоит {round((total_base * float(amount)), 3)} {keys.get(base)}'
        bot.send_message(message.chat.id, text)


bot.polling()

