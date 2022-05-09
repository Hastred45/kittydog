import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

load_dotenv()
secret_token = os.getenv('TOKEN')
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'


def get_cat():
    response = requests.get(URL_CAT)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_dog():
    response = requests.get(URL_DOG)
    response = response.json()
    random_dog = response[0].get('url')
    return random_dog


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_cat())


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_dog())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    buttons = ReplyKeyboardMarkup(
        [['Пёсели', 'Котейки']], resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=buttons
    )
    context.bot.send_photo(chat.id, new_cat(update, context))


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('Пёсели'), new_dog)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('Котейки'), new_cat)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
