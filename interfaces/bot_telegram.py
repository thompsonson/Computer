"interface for telegram bot"

import logging
import re
from telethon import TelegramClient, events, functions, types
import settings

from models.model_notes import VoiceNoteModel, notes_base
from controllers.controller_notes import VoiceNoteController, NoteController
from controllers.controller_bot import MessageSend
from controllers.controller_openai import correct_text, translate_text


logger = logging.getLogger(__name__)
message_store = MessageSend()

logger.info("Hello World")


async def correct_handler(event):
    """Use OpenAI Da Vinci to correct the previous message"""
    response = await correct_text(message_store.get_last())
    await message_store.send(event, response.choices[0].text)  # type: ignore
    raise events.StopPropagation


async def translate_handler(event):
    """Use OpenAI Da Vinci to translate the previous message"""
    response = await translate_text(message_store.get_last())
    await message_store.send(event, response.choices[0].text)  # type: ignore
    raise events.StopPropagation


async def enrich_handler(event):
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


async def new_message_handler(event):
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
        voice_note.save()  # type: ignore
        await message_store.send(
            event,
            f"Note ID: {voice_note.model.id} Content:\n{voice_note.model.content}",
        )
    else:
        await event.respond(event.text)
