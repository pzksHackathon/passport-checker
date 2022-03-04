import re
import os
import django
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler

from records.models import Record

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "passport_checker.settings")
django.conf.settings.configure()
django.setup()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Слава Україні!\n Цей бот перевіряє чи введений номер паспорта є дійсним паспортом громадянина України.')
    update.message.reply_text("Будь-ласка введіть серію та номер паспорта у форматі ХХ УУУУУУ\nХХ - серія паспорта\nУУУУУУ - номер паспорта\nТакож зауважте - вводити необхідно українськими літерами.\nУвага! Бот у стадії розробки, тож можуть бути помилки!")

def accept_number(update: Update, context: CallbackContext):
    expr = re.compile("^[А-Я]{2}\ [0-9]{6}$")
    message = update.effective_message.text
    if not expr.findall(message):
        update.message.reply_text("Будь-ласка введіть серію та номер паспорта у форматі ХХ УУУУУУ\nХХ - серія паспорта\nУУУУУУ - номер паспорта\nТакож зауважте - вводити необхідно українськими літерами.\nУвага! Бот у стадії розробки, тож можуть бути помилки!")
    else:
        series, number = message.split(" ")
        logging.info(Record.objects.filter(series=series))
        if Record.objects.filter(series=series, number=number):
            update.message.reply_text("УВАГА!!! ПАСПОРТ З ЦИМ НОМЕРОМ БУВ ЗНАЙДЕНИЙ У НАШІЙ БАЗІ! НЕГАЙНО ПОВІДОМТЕ ПРАЦІВНИКІВ ПОЛІЦІЇ! ГОЛОВНЕ ЗБЕРІГАЙТЕ СПОКІЙ ТА ДАВАЙТЕ НАШИМ ЗАХИСНИКАМ РОБИТИ ЇХ РОБОТУ!")
        else:
            update.message.reply_text("Все добре! Не хвилюйтесь. Паспорт дійсний")



BOT_TOKEN = os.environ.get("BOT_TOKEN")

updater = Updater(BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(None, accept_number))


updater.start_polling()
updater.idle()
