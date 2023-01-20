import telebot
from config import token, keys
from utils import ExchangeException, Exchange
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n- Показать список доступных валют через команду /values \
    \n- Вывести конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Введите команду или 3 параметра')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {amount} {quote} в {base} - {total_base} '
        bot.send_message(message.chat.id, text)


bot.polling()


# import telebot
# from config import keys, TOKEN
# from utils import ConvertionExeption, CryptoConverter
#
# bot = telebot.TeleBot(TOKEN)
#
# @bot.message_handler(commands=['start', 'help'])
# def help(message: telebot.types.Message):
#     text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
# <в какую валюту перевести> \
# <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
#     bot.reply_to(message, text)
#
# @bot.message_handler(commands=['values'])
# def values(message: telebot.types.Message):
#     text = 'Доступные валюты:'
#     for key in keys.keys():
#         text = '\n'.join((text, key, ))
#     bot.reply_to(message, text)
#
# @bot.message_handler(content_types=['text', ])
# def convert(message: telebot.types.Message):
#     try:
#         values = message.text.split(' ')
#
#         if len(values) != 3:
#             raise ConvertionExeption('Слишком много параметров.')
#
#         quote, base, amount = values
#         total_base = CryptoConverter.convert(quote, base, amount)
#     except ConvertionExeption as e:
#         bot.reply_to(message, f'Ошибка пользователя.\n{e}')
#     except Exception as e:
#         bot.reply_to(message, f'Не удалось обработать команду\n{e}')
#     else:
#         text = f'Цена {amount} {quote} в {base} - {total_base}'
#         bot.send_message(message.chat.id, text)
#
# bot.polling()