"interface for telegram bot"

import logging
from telethon import TelegramClient, events, functions, types
import settings

from models.model_notes import VoiceNoteModel
from controllers.controller_notes import VoiceNoteController
from controllers.controller_bot import MessageSend
from controllers.controller_openai import correct_text, translate_text

logger = logging.getLogger(__name__)
message_store = MessageSend()

logger.info("Hello World")

bot = TelegramClient("session_name", int(settings.API_ID), settings.API_HASH)  # type: ignore
bot.start(bot_token=settings.BOT_TOKEN)  # type: ignore


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
        await message_store.send(event, voice_note.model.content)
    else:
        await event.respond(event.text)


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == "__main__":
    main()
