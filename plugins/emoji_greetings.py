# =============================================================================
#  V26 Userbot Plugin
#
#  Plugin Name:    emoji_greetings
#  Author:         V26 Dev
#  Repository:     https://github.com/lackx741-tech/V26Userbot
#
#  License:        MIT
#
#  IMPORTANT:
#    • If you copy, fork, or include this plugin in your own bot,
#
#  Thank you for respecting open-source software!
# =============================================================================

import asyncio
import re
from telethon import events
from telethon.errors.rpcerrorlist import MessageNotModifiedError

from utils.utils import V26Userbot
from utils.decorators import rishabh
from plugins.bot import add_handler

def init(client):
    commands = [
        "hii       - Big ‘HI’ in emojis",
        "thanks    - Big ‘THANKS’ in emojis",
        "ok        - Sparkling OK in emojis",
        "gn        - Sparkling GN in emojis",
        "bye       - Waving ‘BYE’ in emojis",
        "welc      - Festive ‘WELCOME’ in emojis",
        "love      - Heartfelt ‘LOVE’ in emojis"
    ]
    add_handler("emoji_greetings", commands, "Emoji Greetings Plugin")
    
async def edit_or_reply(event, text):
    """
    Try to edit the triggering message; if that fails, send a reply.
    """
    try:
        return await event.edit(text)
    except (MessageNotModifiedError, Exception):
        return await event.reply(text)



@V26Userbot.on(events.NewMessage(pattern=r"(?i)^bye$", outgoing=True))
@rishabh()
async def bye(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        """
██████╗░██╗░░░██╗███████╗
██╔══██╗╚██╗░██╔╝██╔════╝
██████╦╝░╚████╔╝░█████╗░░
██╔══██╗░░╚██╔╝░░██╔══╝░░
██║░░██║░░░██║░░░███████╗
╚═╝░░╚═╝░░░╚═╝░░░╚══════╝
👋✨🄱🅈🄴✨👋
"""
    )
    await edit_or_reply(event, art)

@V26Userbot.on(events.NewMessage(pattern=r"(?i)^welc$", outgoing=True))
@rishabh()
async def welcome(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        """
██╗██╗██╗██╗██╗██╗██╗██╗██╗██╗
██║██║██║██║██║██║██║██║██║██║
██║██║██║██║██║██║██║██║██║██║
╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝
🎉✨🅆🄴🄻🄲🄾🄼🄴✨🎉
"""
    )
    await edit_or_reply(event, art)

@V26Userbot.on(events.NewMessage(pattern=r"(?i)^love$", outgoing=True))
@rishabh()
async def love(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        """
██╗░░░░░░█████╗░██╗░░░██╗███████╗
██║░░░░░██╔══██╗██║░░░██║██╔════╝
██║░░░░░██║░░██║██║░░░██║█████╗░░
██║░░░░░██║░░██║██║░░░██║██╔══╝░░
███████╗╚█████╔╝╚██████╔╝███████╗
╚══════╝░╚════╝░░╚═════╝░╚══════╝
💖✨🄻🄾🅅🄴✨💖
"""
    )
    await edit_or_reply(event, art)


@V26Userbot.on(events.NewMessage(pattern=r"(?i)^hii$", outgoing=True))
@rishabh()
async def hi(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        """
██╗░░██╗██╗
██║░░██║██║
███████║██║
██╔══██║██║
██║░░██║██║
╚═╝░░╚═╝╚═╝
🦋✨🄷🄴🄻🄻🄾✨🦋\n
"""
    )
    await edit_or_reply(event, art)

@V26Userbot.on(events.NewMessage(pattern=r"(?i)^thanks$", outgoing=True))
@rishabh()
async def thanks(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        """
▀█▀ █░█ ▄▀█ █▄░█ █▄▀ █▀
░█░ █▀█ █▀█ █░▀█ █░█ ▄█
"""
    )
    await edit_or_reply(event, art)

@V26Userbot.on(events.NewMessage(pattern=r"(?i)^ok$", outgoing=True))
@rishabh()
async def ok(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        """
░█████╗░██╗░░██╗
██╔══██╗██║░██╔╝
██║░░██║█████═╝░
██║░░██║██╔═██╗░
╚█████╔╝██║░╚██╗
░╚════╝░╚═╝░░╚═╝
🦋✨🄾🄺🄰🅈✨🦋
"""
    )
    await edit_or_reply(event, art)

@V26Userbot.on(events.NewMessage(pattern=r"(?i)^gn$", outgoing=True))
@rishabh()
async def good_night(event):
    if getattr(event.message, "fwd_from", None):
        return
    art = (
        "░██████╗░███╗░░██╗\n"
        "██╔════╝░████╗░██║\n"
        "██║░░██╗░██╔██╗██║\n"
        "╚██████╔╝██║░╚███║\n"
        "░╚═════╝░╚═╝░░╚══╝\n"
        "🦋✨🄶🄾🄾🄳 🄽🄸🄶🄷🅃✨🦋"
    )
    await edit_or_reply(event, art)
