import requests
import telebot
import json

TOKEN = "6179594384:AAGCD_4gEv4wgm9TXPdFc-InFQA13e9q_Kg"
bot = telebot.TeleBot(TOKEN)

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'фунт': 'GBR',
    'биткоин': 'BTC',
    'рубль': 'RUB',
    'юань': 'CNH'
}

class ConvertionException(Exception):
    print("Неправильный ввод данных")
    #pass

class Exchange:

    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Нельзя вводить одинаковые валюты {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать запрос {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base

@bot.message_handler(commands=['start', 'help'])
def start_exchange(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username},введите команду:\n<с какой валюты>\n<в какую валюту>\n<сумму>\n Список валют /values")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    if len(values) > 3:
        raise ConvertionException
            #("Неправильный ввод данных")

    quote, base, amount = values
    total_base = Exchange.convert(quote, base, amount)


    text = f'Цена {amount} {quote} к {base} -{total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()



