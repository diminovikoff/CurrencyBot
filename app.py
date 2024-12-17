import telebot
from config import keys, HTTP_TOKEN
from extensions import APIException, CurrencyConverter

# Cоздание бота
bot = telebot.TeleBot(HTTP_TOKEN)

# Инструкция для пользователя

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = (
        "Чтобы начать работу введите команду в формате:\n"
        "<имя валюты> <в какую валюту перевести> <количество>\n\n"
        "Например: рубль евро 25\n\n"
        "Посмотреть список всех доступных валют: /values"
    )
    bot.reply_to(message, text)


# Ввод команды /values

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    available_currency = "Доступные валюты: \n"
    for key in keys.values():
        available_currency = "\n".join((available_currency, key, ))
    bot.reply_to(message, available_currency)

# Конвертация

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("Cлишком много парамтеров.")

        quote, base, amount = values

        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"{amount} {base} в {quote} = {total_base:.2f} {quote}"
        bot.send_message(message.chat.id, text)

# Запуск бота
bot.polling(none_stop=True)
