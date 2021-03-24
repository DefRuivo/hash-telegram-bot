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

from models import Session, HashCode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

session = Session()

anterior = {'memo': None}


# Function to add to DB a new Hash data
def add_to_db(code, chat_id):
    new_data = HashCode(ch_id=chat_id, hashed=str(code))
    session.add(new_data)
    session.commit()
    session.flush()


def update_db(code):
    q = session.query(HashCode)
    q = q.filter(HashCode.hashed == str(anterior['memo']))
    record = q.one()
    record.hashed = str(code)
    session.commit()
    session.flush()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Olá, envie: '/n SEU_TOKEN' para receber o token")


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Envie: '/n SEU_TOKEN' para receber o token")


def new_code(update: Update, _: CallbackContext) -> None:
    try:
        query = session.query(HashCode).filter_by(ch_id=int(update.message.chat_id)).first()

        if query is None:
            msg_hash = hash(_.args[0])
            add_to_db(msg_hash, int(update.message.chat_id))
            update.message.reply_text("AQUI SEU TOKEN!")
            update.message.reply_text(f"{msg_hash}")

        elif query is not None:
            buttons = [
                [
                    InlineKeyboardButton(text='Sim', callback_data='SIM'),
                    InlineKeyboardButton(text='Não', callback_data='NAO'),
                ],
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            update.message.reply_text(f"Você já tem um token: {query} , deseja fazer outro?", reply_markup=keyboard)
        anterior['memo'] = query
    except IndexError:
        update.message.reply_text("insira o codigo após o '/n'")


def button(update: Update, _: CallbackContext) -> None:
    update_query = update.callback_query
    update_query.answer('Você escolheu: SIM')
    new_hash = hash(anterior['memo'])
    update_db(new_hash)
    anterior['memo'] = new_hash
    update_query.edit_message_text(text=f"Seu novo hash é: {new_hash}")


def main() -> None:
    """Start the bot."""

    # Create the Updater and pass it your bot's token.
    updater = Updater("1671846790:AAHzzv8qZOF86ZU5GK3yvdVC5SqXwu8Hqws")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("n", new_code))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(~Filters.command, help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
