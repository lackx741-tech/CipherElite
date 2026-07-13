from telethon.tl.functions.users import GetFullUserRequest

V26_USERBOT_NAME = "V26 Userbot"
V26_REPOSITORY_URL = "https://github.com/lackx741-tech/CipherElite"
V26_SESSION_ENV_VAR = "V26_SESSION"
V26_SESSION_BOT_USERNAME = "@v26_session_maker_bot"

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client(GetFullUserRequest(previous_message.sender_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        try:
            user_obj = await event.client(GetFullUserRequest(user))
        except Exception as e:
            return None, e
    return user_obj, None
    