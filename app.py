import telebot
from config import keys, HTTP_TOKEN
from extensions import APIException, CurrencyConverter
import emoji


# Cоздание бота
bot = telebot.TeleBot(HTTP_TOKEN)

# Инструкция для пользователя

@bot.message_handler(commands=['start'])
def starting(message: telebot.types.Message):
    user = message.from_user
    username = user.username or "друг"
    text = (
        f"Привет, {username}!\n"
        f"Добро пожаловать в {emoji.emojize('💱')}CurrencyBot!\n\n"
        f"Я умею конвертировать валюту. \nЗдесь полный список валют: /values \n\n"
        "Нажми здесь, для краткой инструкции: /help \n"

    )
    bot.reply_to(message, text)

# Помощь для пользователя
@bot.message_handler(commands=['help'])
def help_user(message: telebot.types.Message):
    text = (
        "Чтобы начать работу введи команду в формате:\n"
        "<твоя валюта> <в какую валюту перевести> <сумма>\n\n"
        "Например: рубль евро 25\n\n"
    )
    bot.reply_to(message, text)

# Ввод команды /values

@bot.message_handler(commands=['values'])
def give_values(message: telebot.types.Message):
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
            raise APIException(f"Я не смог понять твой запрос.\n\nДоступные команды: /help\nДоступные валюты: /values\n\nПопробуй по шаблону \n{emoji.emojize('🔽🔽🔽')}\n\nрубль евро 25")

        quote, base, amount = values

        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Упс, кажется что-то пошло не так... {emoji.emojize('😔')} \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"{emoji.emojize('✅')} Успешно выполнено: \n\n{emoji.emojize('➕')}Покупка: {amount} {base} \n{emoji.emojize('➖')}Продажа: {total_base:.2f} {quote}"
        bot.send_message(message.chat.id, text)

# Запуск бота
bot.polling(none_stop=True)
