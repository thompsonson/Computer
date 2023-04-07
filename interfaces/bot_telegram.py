"interface for telegram bot"

import logging
import re
from telethon import TelegramClient, events, functions, types
import settings

from models.model_notes import VoiceNoteModel, Base
from controllers.controller_notes import VoiceNoteController, NoteController
from controllers.controller_bot import MessageSend
from controllers.controller_openai import correct_text, translate_text

from main import bot

from dal import create_engine_and_session

logger = logging.getLogger(__name__)
message_store = MessageSend()

logger.info("Hello World")


@bot.on(events.NewMessage(pattern="/correct"))
async def correct(event):
    """Use OpenAI Da Vinci to correct the previous message"""
    response = await correct_text(message_store.get_last())
    await message_store.send(event, response.choices[0].text)  # type: ignore
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/translate"))
async def translate(event):
    """Use OpenAI Da Vinci to translate the previous message"""
    response = await translate_text(message_store.get_last())
    await message_store.send(event, response.choices[0].text)  # type: ignore
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/enrich"))
async def enrich(event):
    """Use OpenAI Da Vinci to translate the previous message"""
    match = re.search(r"^/enrich\s(\d+)$", event.text)
    if match:
        # If a number was found, convert it to an integer
        number = int(match.group(1))
        await NoteController(id=number).generate_additonal_info()
        await message_store.send(event, f"Enriched note {number}")
    else:
        # If no number was found, print an error message
        await message_store.send(event, "Error: Invalid message format")
    raise events.StopPropagation


@bot.on(events.NewMessage)  # type: ignore
async def echo(event):
    """Echo the user message."""
    if event.voice:
        # await event.respond("processing the voice message")
        await message_store.send(event, "processing the voice message")
        await event.download_media(f"downloads/voicenotes/{event.message.id}.ogg")
        logger.info(
            "downloaded the voice message: downloads/voicenotes/%s.ogg",
            event.message.id,
        )
        voice_note = VoiceNoteController(
            VoiceNoteModel(
                source=f"telegram/{event.message.id}",
                file_location=f"downloads/voicenotes/{event.message.id}.ogg",
                file_encoding="ogg",
            )
        )
        voice_note.transcribe()
        # await event.respond(f"id:{voice_note_data.id}\n{voice_note_data.content}")
        session = create_engine_and_session(Base)
        session.add(voice_note.model)
        session.commit()
        await message_store.send(
            event,
            f"Note ID: {voice_note.model.id} Content:\n{voice_note.model.content}",
        )
    else:
        await event.respond(event.text)


def start_telegram_bot():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == "__main__":
    bot = TelegramClient(settings.TELEGRAM_SESSION, int(settings.API_ID), settings.API_HASH)  # type: ignore
    bot.start(bot_token=settings.BOT_TOKEN)  # type: ignore
    start_telegram_bot()
