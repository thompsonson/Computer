"settings for the project"
import os
import logging
from time import strftime

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    filename=f"./logs/info_{strftime('%Y_%m_%d')}.log",
    encoding="utf-8",
    level=logging.INFO,
)

# OpenAI secret Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
GPT_MODEL = "text-davinci-003"
T2S_MODEL = "whisper-1"
# Telegram secret access bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_COMPUTERBOT")
TELEGRAM_API_ID = os.getenv("TELEGRAM_APP_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_APP_HASH")
TELEGRAM_SESSION = ".db/telegram.session"

# database related
SQLA_CONNECTION_STRING = "sqlite:///.db/database.db"
SQLA_ECHO = False
SQLA_FUTURE = True
TEST_DATABASE_URL = "sqlite:///.db/test_database.db"  # "sqlite:///:memory:"

# TOOLS
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
