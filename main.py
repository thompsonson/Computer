"Main script for launching the web interface and telegram bot (using the async `loop`)"

from quart import Quart

from telethon import TelegramClient

import settings

app = Quart(__name__)


# Quart handlers
@app.route("/", methods=["GET"])
async def root():
    return "Tea, Earl Grey, Hot."


# below is from: https://github.com/LonamiWebs/Telethon/blob/2a7d4317bd20c171a36abe93aac417a460643c99/telethon_examples/quart_login.py
# By default, `Quart.run` uses `asyncio.run()`, which creates a new asyncio
# event loop. If we create the `TelegramClient` before, `telethon` will
# use `asyncio.get_event_loop()`, which is the implicit loop in the main
# thread. These two loops are different, and it won't work.
#
# So, we have to manually pass the same `loop` to both applications to
# make 100% sure it works and to avoid headaches.
#
# Quart doesn't seem to offer a way to run inside `async def`
# (see https://gitlab.com/pgjones/quart/issues/146) so we must
# run and block on it last.
#
# This example creates a global client outside of Quart handlers.
# If you create the client inside the handlers (common case), you
# won't have to worry about any of this.
bot = TelegramClient(settings.TELEGRAM_SESSION, int(settings.API_ID), settings.API_HASH)  # type: ignore
bot.start(bot_token=settings.BOT_TOKEN)  # type: ignore
app.run(loop=bot.loop, host="0.0.0.0", port=8080)  # <- same event loop as telethon

# there may be a better way to do this, like the typer commands
from interfaces.bot_telegram import start_telegram_bot

start_telegram_bot()
