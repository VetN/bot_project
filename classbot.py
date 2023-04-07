import requests
import json
from config import *


class ConvertionException(Exception):
    pass


class Exchange:
    @staticmethod
    def convert(quote: str,  base: str, amount: str):
        quote = quote.lower()
        base = base.lower()
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
