#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import json
import requests
import os
import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, CallbackQueryHandler, InlineQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from functools import wraps
from time import sleep
import time
import datetime
from telegram.utils.helpers import escape_markdown
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
def checkall(update, context):
   #headers = {
   # "Cache-Control" : "no-cache",
   # "Pragma" : "no-cache"
   #}
   st = requests.session()
   st2 = st.get('http://our_url/ping.php').json()
   json_data = json.dumps(st2, indent=2)
   st.cookies.clear()
   update.message.reply_text('wait aku check')
   time.sleep(5)
   update.message.reply_text(json_data.replace("}","").replace("{","").replace("p ","p\n").replace('"',''))
def tracert_callback(update, context):
   update.message.reply_text('wait agak lama ya bentar ..')
   hostname = "".join(context.args)
   response = os.system("sshpass -p 'password' ssh user@mikrotikip -o StrictHostKeyChecking=no tool traceroute " + hostname + " count=1 > r1.txt && tail -20 r1.txt > tr1.txt")
   z1 = open("tr1.txt", "r")
   z2 = z1.read()
   z1.close()
   update.message.reply_text(z2)
def nslookup_callback(update, context):
   hostname = "".join(context.args)
   response = os.system("nslookup " + hostname + "> ns1.txt")
   r3 = open("ns1.txt", "r")
   r1 = r3.read()
   r3.close()
   update.message.reply_text('wait aku check')
   time.sleep(5)
   update.message.reply_text(r1)
def ping_callback(update, context):
  #if len(args) == 0:
  hostname = "".join(context.args)
  response = os.system("ping -c 5 " + hostname +  "> t1.txt")
  r2 = open("t1.txt", "r")
  t1 = r2.read()
  r2.close()
  """Send a message when the command /help is issued."""
  update.message.reply_text('wait aku check')
  time.sleep(5)
  #update.message.reply_text(json_data.replace("}","").replace("{","").replace("p ","p\n").replace('"',''))
  update.message.reply_text(t1)

#def test(update, context):
#    update.message.reply_text(chat_id=chat_id,text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.',parse_mode=telegram.ParseMode.HTML)
def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("your key akses", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ping", ping_callback))
    dp.add_handler(CommandHandler("nslookup", nslookup_callback))
    dp.add_handler(CommandHandler("tracert", tracert_callback))
    dp.add_handler(CommandHandler("checkall", checkall))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
