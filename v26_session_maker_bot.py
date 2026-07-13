"""
V26 Session Maker Bot
=====================
A standalone Telegram bot that generates V26_SESSION strings for the V26 Userbot.

Usage:
    1. Set BOT_TOKEN, API_ID, API_HASH environment variables (or edit the config below).
    2. Run:  python3 v26_session_maker_bot.py
    3. On Telegram, start the bot and follow the prompts.

Requirements:
    pip install telethon aiogram python-dotenv
"""

import asyncio
import logging
import os
import random
from typing import List

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberBannedError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# Configuration — edit here or set environment variables
# ──────────────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("SESSION_BOT_TOKEN", "")
API_ID: int = int(os.getenv("API_ID", "0"))
API_HASH: str = os.getenv("API_HASH", "")

# ──────────────────────────────────────────────────────────────────────────────
# V26 Session Protection — same salts as utils/v26_security.py
# ──────────────────────────────────────────────────────────────────────────────
_s1 = [chr(c) for c in [118, 50, 54, 88, 75, 55, 112, 81, 110, 68]]
_s2 = [chr(c) for c in [77, 57, 118, 50, 67, 120, 76, 52, 114, 84, 97, 81, 56, 107, 80]]

_SALT1: str = "".join(_s1)  # 10-char V26 salt
_SALT2: str = "".join(_s2)  # 15-char V26 salt

if len(_SALT1) != 10 or len(_SALT2) != 15:
    raise RuntimeError("V26 salt integrity check failed")


def _positions(length: int, count: int, seed: str) -> List[int]:
    """Return sorted pseudo-random positions for salt insertion."""
    rng = random.Random(seed)
    return sorted(rng.sample(range(length + count), count))


def _v26_embed(plain: str) -> str:
    """
    Embed V26 salts into a plain Telethon StringSession to produce
    the obfuscated V26_SESSION string.

    This is the inverse of v26_protect() in utils/v26_security.py.
    """
    # Step 1: embed SALT1 into the plain session
    pos1 = _positions(len(plain), len(_SALT1), seed=_SALT1)
    lst1 = list(plain)
    for i, idx in enumerate(pos1):
        lst1.insert(idx, _SALT1[i])
    s1 = "".join(lst1)

    # Step 2: embed SALT2 into the result of step 1
    pos2 = _positions(len(s1), len(_SALT2), seed=_SALT2)
    lst2 = list(s1)
    for i, idx in enumerate(pos2):
        lst2.insert(idx, _SALT2[i])

    return "".join(lst2)


# ──────────────────────────────────────────────────────────────────────────────
# FSM States
# ──────────────────────────────────────────────────────────────────────────────
class SessionStates(StatesGroup):
    waiting_phone = State()
    waiting_code = State()
    waiting_password = State()


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
# In-memory store for active Telethon clients during the sign-in flow.
_pending_clients: dict[int, TelegramClient] = {}

logging.basicConfig(
    format="[%(levelname)5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING,
)

WELCOME_TEXT = """
🔐 **V26 Session Maker Bot**

Welcome! This bot generates a **V26_SESSION** string for the **V26 Userbot**.

⚠️ **Security Notice:**
• Your phone number and credentials are used only to generate the session.
• The session is processed in memory and never stored on a server.
• Only share your session string with your own V26 Userbot — never with anyone else.

📝 **How it works:**
1. Send your Telegram phone number (with country code, e.g. +1234567890)
2. Enter the verification code Telegram sends you
3. Enter your 2FA password if you have one set
4. Receive your V26_SESSION string — paste it into your .env file

➡️ **Send /generate to begin.**
"""

INSTRUCTIONS_TEXT = """
ℹ️ **V26 Session — Quick Setup**

After you receive your V26_SESSION string:

1. Open your `.env` file (or set the environment variable)
2. Set `V26_SESSION=<your_session_string>`
3. Start your V26 Userbot with `python3 main.py`

The V26_SESSION is encrypted with V26-specific salts.
It is **not compatible** with standard Telethon tools or other userbots.

➡️ **Send /generate to create a new session.**
"""


# ──────────────────────────────────────────────────────────────────────────────
# Bot handlers
# ──────────────────────────────────────────────────────────────────────────────
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME_TEXT, parse_mode="Markdown")


async def cmd_help(message: Message) -> None:
    await message.answer(INSTRUCTIONS_TEXT, parse_mode="Markdown")


async def cmd_generate(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SessionStates.waiting_phone)
    await message.answer(
        "📱 **Step 1 of 3 — Phone Number**\n\n"
        "Send your Telegram phone number with the country code.\n"
        "Example: `+1234567890`\n\n"
        "_Send /cancel to abort._",
        parse_mode="Markdown",
    )


async def cmd_cancel(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    client = _pending_clients.pop(user_id, None)
    if client:
        try:
            await client.disconnect()
        except Exception:
            pass
    await state.clear()
    await message.answer("❌ Session generation cancelled.")


async def handle_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if not phone.startswith("+") or not phone[1:].isdigit():
        await message.answer(
            "⚠️ Invalid phone number format.\n"
            "Please include the country code, e.g. `+1234567890`",
            parse_mode="Markdown",
        )
        return

    user_id = message.from_user.id
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    _pending_clients[user_id] = client

    try:
        await client.connect()
        result = await client.send_code_request(phone)
        await state.update_data(phone=phone, phone_code_hash=result.phone_code_hash)
        await state.set_state(SessionStates.waiting_code)
        await message.answer(
            "✅ Code sent!\n\n"
            "📨 **Step 2 of 3 — Verification Code**\n\n"
            "Check your Telegram for the login code and send it here.\n"
            "Format: `12345` (digits only, no spaces)\n\n"
            "_Send /cancel to abort._",
            parse_mode="Markdown",
        )
    except PhoneNumberInvalidError:
        await _cleanup(user_id)
        await state.clear()
        await message.answer("❌ Invalid phone number. Please check and try again.")
    except PhoneNumberBannedError:
        await _cleanup(user_id)
        await state.clear()
        await message.answer("❌ This phone number is banned from Telegram.")
    except FloodWaitError as e:
        await _cleanup(user_id)
        await state.clear()
        await message.answer(f"⏳ Too many requests. Please wait {e.seconds} seconds and try again.")
    except Exception as e:
        await _cleanup(user_id)
        await state.clear()
        await message.answer(f"❌ Error: {e}\n\nPlease try again with /generate")


async def handle_code(message: Message, state: FSMContext) -> None:
    code = message.text.strip().replace(" ", "")
    user_id = message.from_user.id
    client = _pending_clients.get(user_id)

    if not client:
        await state.clear()
        await message.answer("❌ Session expired. Please start again with /generate")
        return

    data = await state.get_data()
    phone = data.get("phone")
    phone_code_hash = data.get("phone_code_hash")

    try:
        await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
        await _finish_session(message, state, client, user_id)

    except SessionPasswordNeededError:
        await state.set_state(SessionStates.waiting_password)
        await message.answer(
            "🔑 **Step 3 of 3 — Two-Factor Authentication**\n\n"
            "Your account has 2FA enabled. Please send your password.\n\n"
            "_Send /cancel to abort._",
            parse_mode="Markdown",
        )
    except PhoneCodeInvalidError:
        await message.answer(
            "❌ Incorrect verification code. Please check and try again.\n"
            "_The code should be digits only, no spaces._",
            parse_mode="Markdown",
        )
    except PhoneCodeExpiredError:
        await _cleanup(user_id)
        await state.clear()
        await message.answer("❌ The code has expired. Please start again with /generate")
    except Exception as e:
        await _cleanup(user_id)
        await state.clear()
        await message.answer(f"❌ Error: {e}\n\nPlease try again with /generate")


async def handle_password(message: Message, state: FSMContext) -> None:
    password = message.text.strip()
    user_id = message.from_user.id
    client = _pending_clients.get(user_id)

    if not client:
        await state.clear()
        await message.answer("❌ Session expired. Please start again with /generate")
        return

    try:
        await client.sign_in(password=password)
        await _finish_session(message, state, client, user_id)
    except Exception as e:
        await _cleanup(user_id)
        await state.clear()
        await message.answer(f"❌ 2FA failed: {e}\n\nPlease try again with /generate")


async def _finish_session(
    message: Message,
    state: FSMContext,
    client: TelegramClient,
    user_id: int,
) -> None:
    """Extract the raw Telethon session, embed V26 salts, and send it to the user."""
    try:
        plain_session: str = client.session.save()
        v26_session: str = _v26_embed(plain_session)

        # Confirm the session is valid by fetching account info
        me = await client.get_me()
        name = me.first_name or "User"

        await message.answer(
            f"✅ **Session generated successfully for {name}!**\n\n"
            "🔐 **Your V26_SESSION:**\n\n"
            f"`{v26_session}`\n\n"
            "📋 **Next steps:**\n"
            "1. Copy the session string above\n"
            "2. Open your `.env` file\n"
            "3. Set `V26_SESSION=<paste_here>`\n"
            "4. Run `python3 main.py`\n\n"
            "⚠️ **Keep this string private!** Anyone with it can access your Telegram account.",
            parse_mode="Markdown",
        )
    finally:
        await _cleanup(user_id)
        await state.clear()


async def _cleanup(user_id: int) -> None:
    """Disconnect and remove a pending client."""
    client = _pending_clients.pop(user_id, None)
    if client:
        try:
            await client.disconnect()
        except Exception:
            pass


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────
async def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "❌ SESSION_BOT_TOKEN is not set.\n"
            "   Set the SESSION_BOT_TOKEN environment variable and try again."
        )
    if not API_ID or not API_HASH:
        raise SystemExit(
            "❌ API_ID / API_HASH are not set.\n"
            "   Get them from https://my.telegram.org and set them as environment variables."
        )

    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register handlers
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_generate, Command("generate"))
    dp.message.register(cmd_cancel, Command("cancel"))
    dp.message.register(handle_phone, SessionStates.waiting_phone)
    dp.message.register(handle_code, SessionStates.waiting_code)
    dp.message.register(handle_password, SessionStates.waiting_password)

    print("🤖 V26 Session Maker Bot is running...")
    print("   Send /generate on Telegram to begin.")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
