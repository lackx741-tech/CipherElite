from vars import *
from utils.helpers import V26_USERBOT_NAME

class Config:
    # Core Settings
    API_ID = API_ID
    API_HASH = API_HASH
    V26_SESSION = V26_SESSION
    
    # Bot Configuration
    V26_BOT_PREFIX = V26_BOT_PREFIX
    # Backward-compatible alias used by existing plugins.
    BOT_PREFIX = V26_BOT_PREFIX
    BOT_NAME = V26_USERBOT_NAME
    BOT_TOKEN = BOT_TOKEN
    V26_BOT_USERNAME = V26_BOT_USERNAME
    # Backward-compatible alias used by existing plugins.
    TG_BOT_USERNAME = V26_BOT_USERNAME
    
    # Access Control
    SUDO_USERS = SUDO_USERS
    LOG_CHAT_ID = LOG_CHAT_ID
    # alive picture and name Control
    ALIVE_NAME = ALIVE_NAME
    DEFAULT_PING_PIC = PING_PIC
    DEFAULT_ALIVE_PIC = ALIVE_PIC
    DEFAULT_PMPERMIT_PIC = PMPERMIT_PIC
    # Version Info
    VERSION = "2"
    BRANCH = BRANCH
    # Mirrors the configured fork URL from vars.py for updater compatibility.
    UPSTREAM_REPO = UPSTREAM_REPO
