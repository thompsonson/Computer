"settings for the project"
import os
import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="output.log",
    encoding="utf-8",
    level=logging.INFO,
)

# OpenAI secret Key
API_KEY = os.getenv("OPENAI_API_KEY")
# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
GPT_MODEL = "text-davinci-003"
T2S_MODEL = "whisper-1"
# Telegram secret access bot token
BOT_TOKEN = os.getenv("TELEGRAM_COMPUTERBOT")
API_ID = os.getenv("TELEGRAM_APP_ID")
API_HASH = os.getenv("TELEGRAM_APP_HASH")
