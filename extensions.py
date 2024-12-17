import requests
import json
from config import keys

#Дополнительные структуры данных (класс или функция)

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f"Невозможно перевести одинаковую валюту {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        try:
            # Запросы к стороннему API
            r = requests.get(
                f'https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_AYDYkbg8oJYRkL84j3qlYEaBq2un67quOU7bLmIB&base_currency={base_ticker}&currencies={quote_ticker}')

            # Обработка ошибки достуа
            if r.status_code != 200:
                raise APIException(f"Ошибка API: {r.status_code}. Попробуйте позже.")

            # Библиотека JSON и сбор от API

            API_DATA = json.loads(r.content)

            # Проверка на наличие необходиммых данных
            if 'data' not in API_DATA or quote_ticker not in API_DATA['data']:
                raise APIException("Не удалось получить данные о курсе валюты.")

            currency = API_DATA["data"][quote_ticker]

            return currency * amount

        except requests.exceptions.RequestException as e:
            raise APIException(f"Сетевая ошибка: {e}")