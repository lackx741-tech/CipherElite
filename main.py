import asyncio
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from config.config import Config
from utils.v26_security import v26_protect
from startup.startup import start_bot

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

# Initialize Telegram client
v26_session = v26_protect(Config.V26_SESSION)
client = TelegramClient(
    StringSession(v26_session),
    Config.API_ID,
    Config.API_HASH
)

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(start_bot(client))
