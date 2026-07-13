from telethon import TelegramClient

from utils.helpers import V26_USERBOT_NAME

# Backward-compatible client reference used across existing plugins.
CipherElite = None
V26Userbot = None
BOT_DISPLAY_NAME = V26_USERBOT_NAME


def init_client(client_instance):
    global CipherElite, V26Userbot
    CipherElite = client_instance
    V26Userbot = client_instance
    