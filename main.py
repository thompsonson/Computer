"Main script for launching the web interface and telegram bot (using the async `loop`)"

from quart import Quart

from telethon import events

from controllers.controller_bot import TelethonWrapper
from interfaces.bot_telegram import *

import utils.settings as settings

app = Quart(__name__)


# Quart handlers
@app.route("/", methods=["GET"])
async def root():
    "computer,"
    return "Tea, Earl Grey, Hot."


# logic for below from: https://github.com/LonamiWebs/Telethon/blob/2a7d4317bd20c171a36abe93aac417a460643c99/telethon_examples/quart_login.py
bot = TelethonWrapper()  # type: ignore

bot.add_event_handler(correct_handler, events.NewMessage(pattern="/correct"))
bot.add_event_handler(translate_handler, events.NewMessage(pattern="/translate"))
bot.add_event_handler(enrich_handler, events.NewMessage(pattern="/enrich"))

bot.add_event_handler(correct_handler, events.CallbackQuery(data=b"correct"))
bot.add_event_handler(translate_handler, events.CallbackQuery(data=b"translate"))
bot.add_event_handler(enrich_handler, events.CallbackQuery(data=b"enrich"))
bot.add_event_handler(corriger_handler, events.CallbackQuery(data=b"corriger"))

bot.add_event_handler(new_message_handler, events.NewMessage(outgoing=False))

bot.start_bot()  # type: ignore

app.run(
    loop=bot.get_loop(), host="0.0.0.0", port=8080
)  # <- same event loop as telethon
