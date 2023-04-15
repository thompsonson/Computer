"controller for the bots"
import logging
from telethon import TelegramClient

import utils.settings as settings


logger = logging.getLogger(__name__)


class TelethonWrapper:
    "telegram bot controller, using telethon"

    def __init__(self):
        logger.info("creating TelegramClient")
        self._bot = TelegramClient(
            settings.TELEGRAM_SESSION,
            int(settings.TELEGRAM_API_ID),  # type: ignore
            settings.TELEGRAM_API_HASH,  # type: ignore
        )

    def get_loop(self):
        "get the event loop"
        return self._bot.loop  # type: ignore

    def start_bot(self) -> None:
        "start the bot"
        logger.info("starting the bot")
        self._bot.start(bot_token=settings.TELEGRAM_BOT_TOKEN)  # type: ignore
        # self._bot.run_until_disconnected()  # type: ignore
        logger.info("bot started (or finished, depending on how asynio works)")

    def add_event_handler(self, event_handler, event):
        "add an event handler"
        logger.info("adding event handler: %s for event: %s", event_handler, event)
        self._bot.add_event_handler(event_handler, event)


class MessageSend:
    "send and store messages"

    def __init__(self):
        self.messages = []

    async def send(self, event, message, note_id=None, voice_note_id=None):
        """send and add a message"""
        await event.respond(message)
        message_info = {
            "message": message,
            "note_id": note_id,
            "voice_note_id": voice_note_id,
        }
        self.messages.append(message_info)

    def get(self):
        "get all messages"
        return self.messages

    def clear(self):
        "clear all messages"
        self.messages = []

    def get_last(self):
        "get the last message"
        return self.messages[-1]
