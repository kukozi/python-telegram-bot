#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext
from src.openweather_api import openweather_vars as ow_vars, location, apikey as ow_key
from src.apikey import key as tkey

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def get_weather(uri, key, city, lat, lon):
    result = requests.get(uri, params={'lon': lat, 'lat': lon, 'appid': key, 'units': 'metric'})
    return result.json()

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

# a way to send echo message:
# update.message.reply_text(update.message.text)

def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def weather_command(update: Update, _: CallbackContext) -> 'Ответ с информацией о погоде':
    user = update.effective_user
    """Send data from api file to weather function"""
    try:
        answer = get_weather(ow_vars.uri, ow_key, ow_vars.default_city, location.lat, location.lon)
        print(answer)
        ans_weather = answer['weather'][0]['description']
        ans_temp = answer['main']['temp']
        ans_temp_min = answer['main']['temp_min']
        ans_temp_max = answer['main']['temp_max']
        #ans_weather = answer['list'][0]['weather'][0]['description']
        #ans_temp_day = answer['list'][0]['temp']['day']
        #ans_temp_night = answer['list'][0]['temp']['night']
        update.message.reply_text('''{}, вот что у нас сегодня в Питере...
        
        Погода: {}
        Температура средняя: {}
        Температура (max): {}
        Температура (min): {}
        
Хорошего дня!
        '''.format(user.name,ans_weather, ans_temp, ans_temp_min, ans_temp_max))
    except Exception as e:
        print("Exception (weather):", e)
        pass

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(tkey)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("weather", weather_command))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
