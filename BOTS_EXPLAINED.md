# V26 Ecosystem: The 3 Bots Explained

This document explains how the V26 stack is split into **three separate components**:

1. **V26 Session Maker Bot** — creates a protected `V26_SESSION`
2. **V26 Userbot (Main)** — runs on your personal Telegram account and executes `.commands`
3. **V26 Assistant Bot** — provides help UI, inline menus, and owner-facing bot interactions

---

## Overview Table

| Feature | Session Bot | Userbot | Assistant |
|---|---|---|---|
| Type | Utility service | Personal account automation | Telegram bot UI |
| Main file(s) | `v26_session_maker_bot.py` | `main.py`, `startup/startup.py`, `plugins/` | `plugins/bot.py`, `bot_plugins/assistant.py` |
| Identity | Bot token | Your Telegram account session | Separate bot token |
| Primary job | Generate protected sessions | Run commands and automation | Help menu, inline buttons, message relay |
| Interaction style | Telegram chat flow | Telegram messages with `.` prefix | `/start`, `/help`, inline queries, buttons |
| Setup first? | **Yes — deploy this first** | Second | Third |
| Must run 24/7? | No, only when generating sessions | **Yes** | Best when bundled with userbot |
| Best deployment | Separate VPS / separate process | Main VPS / host | Same host as userbot or separate host |
| Sensitive data handled | Phone number, login code, 2FA password | Your account session and admin settings | Bot token, forwarded user messages |

### Which one to deploy first?

1. **Session Maker Bot** — because you need a valid `V26_SESSION` first
2. **V26 Userbot** — the main runtime
3. **Assistant Bot** — after the userbot is ready and `BOT_TOKEN` is configured

---

## Bot #1: V26 Session Maker Bot

### Purpose & why it's needed

The session maker is a **standalone Python bot** that creates a Telegram `StringSession`, then wraps it into a **V26-only protected session**.

It is **not** your userbot UI. Its only job is:

- accept phone number
- send login code
- accept 2FA password if needed
- generate a session string
- obfuscate it with `_v26_embed()`
- return a ready-to-use `V26_SESSION`

### Architecture & how it works

Relevant file: `v26_session_maker_bot.py`

- Uses **Aiogram** for Telegram bot messaging
- Uses **Telethon** for account login/session generation
- Stores active login clients in memory via `_pending_clients`
- Uses FSM states:
  - `waiting_phone`
  - `waiting_code`
  - `waiting_password`
- After successful login, calls `_v26_embed(plain_session)`
- Returns the protected string to the user
- Clears memory and disconnects the pending client on completion/cancel

### Session flow

```text
User
  |
  | /generate
  v
Session Bot (Aiogram)
  |
  | ask for phone number
  v
Telethon login client
  |
  | send_code_request(phone)
  v
User enters OTP
  |
  | if needed -> ask for 2FA password
  v
client.session.save()
  |
  | _v26_embed()
  v
Protected V26_SESSION returned to user
```

### Setup instructions

1. Create a Telegram bot using **@BotFather**
2. Save the token as `SESSION_BOT_TOKEN`
3. Get `API_ID` and `API_HASH` from `https://my.telegram.org`
4. Install dependencies
5. Run `python3 v26_session_maker_bot.py`
6. Open the bot in Telegram and use `/generate`

### Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `SESSION_BOT_TOKEN` | Yes | Token for the standalone session bot |
| `API_ID` | Yes | Telegram API ID |
| `API_HASH` | Yes | Telegram API hash |

### Security details

- `SESSION_BOT_TOKEN` is separate from the main assistant `BOT_TOKEN`
- The bot keeps login state in memory with `_pending_clients`
- Session protection matches `utils/v26_security.py`
- Two salts are embedded before the string is returned
- The bot disconnects clients on cancel, finish, or failure
- Users should never share the generated `V26_SESSION`

### How to run it

```bash
cd /path/to/CipherElite
export SESSION_BOT_TOKEN="123456:session-bot-token"
export API_ID="12345678"
export API_HASH="your_api_hash"
python3 v26_session_maker_bot.py
```

### Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `SESSION_BOT_TOKEN is not set` | Missing env var | Export `SESSION_BOT_TOKEN` first |
| `API_ID / API_HASH are not set` | Telegram API creds missing | Add both values from my.telegram.org |
| Invalid phone number | Wrong format | Use `+countrycodephonenumber` |
| Code expired | Delay during OTP step | Restart with `/generate` |
| 2FA failed | Wrong password | Retry with correct password |
| Flood wait | Too many login attempts | Wait for the reported time |

---

## Bot #2: V26 Userbot (Main)

### What it does

The userbot is the **main V26 runtime**. It logs into **your personal Telegram account** and loads plugins from `plugins/`.

Key behavior:

- Runs from `main.py`
- Converts protected `V26_SESSION` back into a usable Telethon session with `v26_protect()`
- Loads all plugin files from `plugins/`
- Uses `.` as the default command prefix via `V26_BOT_PREFIX`
- Restricts sensitive commands with the `@rishabh()` / owner-sudo decorators
- Starts both userbot logic and helper-bot logic during startup

### Architecture

Core files:

- `main.py`
- `startup/startup.py`
- `config/config.py`
- `vars.py`
- `utils/v26_security.py`
- `utils/decorators.py`
- `plugins/`

Runtime path:

```text
main.py
  -> v26_protect(Config.V26_SESSION)
  -> Telethon client(StringSession(...))
  -> startup.start_bot(client)
       -> init_client(client)
       -> init_bot(client)                # assistant bot client
       -> load_plugins(client)            # userbot plugins
       -> load_bot_plugins(bot, client)   # assistant-side plugins
       -> run_until_disconnected()
```

### How plugins work

- Each plugin lives in `plugins/*.py`
- `startup.load_plugins()` imports each plugin dynamically
- Plugin `init(client)` hooks Telethon events
- Some plugins also expose `register_commands()`
- Help metadata is registered through `plugins.bot.add_handler()` and stored in `CMD_LIST`
- The inline help system paginates plugins using `PLUGINS_PER_PAGE = 9`

### Setup & deployment

1. Generate `V26_SESSION` with the session maker bot
2. Copy `sample.env` to `.env`
3. Fill in `API_ID`, `API_HASH`, `V26_SESSION`, `BOT_TOKEN`, `V26_BOT_USERNAME`, `SUDO_USERS`, and `LOG_CHAT_ID`
4. Install requirements from `requirements.txt`
5. Start `python3 main.py`
6. Keep it alive with `tmux`, a VPS supervisor, Docker, or your preferred host

### Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `API_ID` | Yes | Telegram API ID |
| `API_HASH` | Yes | Telegram API hash |
| `V26_SESSION` | Yes | Protected session created by the session maker bot |
| `BOT_TOKEN` | Yes in current startup flow | Token for the assistant/help bot |
| `V26_BOT_USERNAME` | Yes | Assistant bot username, including `@` |
| `SUDO_USERS` | Yes | Comma-separated Telegram user IDs with elevated access |
| `LOG_CHAT_ID` | Recommended | Startup logs and status channel/group |
| `ALIVE_NAME` | Optional | Display name used by some plugins |
| `BRANCH` | Optional | Branch used by updater logic |

### Commands reference

- Prefix: `.`
- Examples:
  - `.help`
  - `.help spam`
  - `.plugins`
  - `.findplugin tool`
  - `.alive`
  - `.stats`
  - plugin-specific commands exposed by each module

### Access control

V26 protects sensitive operations with decorators in `utils/decorators.py`:

- `@rishabh()` — owner and `SUDO_USERS` only
- `@rishabh_help()` — protected help/inline interactions
- `authorized_users_only()` — broader admin-aware restriction for group usage

### Plugin categories breakdown

> **Repository snapshot:** the current repo contains **56 core userbot plugins** in `plugins/`, plus **2 assistant-side bot plugins** in `bot_plugins/`. The broader V26 ecosystem exceeds **60 active modules/components** when you include the assistant-side plugins, session maker, and startup/help runtime.

#### Security & Privacy (8)

- `antiflood`
- `autokick`
- `flashvault`
- `forcesub`
- `ghostvault`
- `pmpermit`
- `scrubber`
- `warn`

#### AI & Smart Features (3)

- `Cipher_ai`
- `ai_setup`
- `clone`

#### Media & Image Tools (12)

- `animation`
- `arts`
- `autoprofile`
- `carbon`
- `giftools`
- `glitch`
- `imagetools`
- `stickertools`
- `text2img`
- `videotools`
- `words`
- `zip`

#### Communication (7)

- `autoforword` *(auto-forward plugin)*
- `broadcast`
- `echo`
- `raid`
- `send`
- `spam`
- `whisper`

#### Group Management & Admin (6)

- `admin`
- `chats`
- `emoji_greetings`
- `greetings`
- `purge`
- `tagger`

#### Fun & Entertainment (5)

- `Bait`
- `fun`
- `fun_animations`
- `Shayri`
- `namestyle`

#### Utility & Tools (12)

- `afk`
- `alive`
- `android_tools`
- `fontchanger`
- `globaltools`
- `help`
- `info`
- `install`
- `stats`
- `toolkit`
- `tools`
- `updater`

#### External Integrations (2)

- `Playstore`
- `twitter`

> Note: the issue summary mentions Twitter/Instagram-style integrations. In the current repository snapshot, the dedicated Python modules present in `plugins/` are `twitter` and `Playstore`, while `plugins/insta.txt` exists as a supporting resource rather than a loadable Python plugin.

#### Core UI & Navigation (1)

- `bot` — inline help router and plugin registry

### Assistant-side bot modules (2)

These are not loaded as userbot plugins, but they are part of the ecosystem:

- `bot_plugins/assistant.py`
- `bot_plugins/whisper_bot.py`

### Totals at a glance

| Scope | Count |
|---|---:|
| Core userbot plugins (`plugins/`) | 56 |
| Assistant-side bot plugins (`bot_plugins/`) | 2 |
| Standalone session maker | 1 |
| Main runtime / startup layers | 2+ |
| **Overall ecosystem components** | **60+** |

### Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `Invalid V26 session format` | Session was not generated by the V26 session maker | Generate a fresh `V26_SESSION` |
| Assistant bot fails to start | `BOT_TOKEN` invalid or missing | Set a valid bot token from BotFather |
| `.help` inline menu fails | `V26_BOT_USERNAME` or bot startup issue | Verify bot username and token |
| Commands do nothing | You are not owner/sudo | Add your user ID to `SUDO_USERS` |
| Logs do not arrive | Wrong `LOG_CHAT_ID` | Use a valid private group/channel ID |
| Updater/install issues | Host lacks permissions/network | retry on a VPS with package install access |

---

## Bot #3: V26 Assistant Bot

### Purpose

The assistant bot is the **UI layer** of the ecosystem.

It is responsible for:

- `/start` welcome screens
- owner control menu
- help menus and buttons
- inline query based help display
- pagination
- relaying private user messages to the owner

### How it integrates with the userbot

Relevant files:

- `plugins/bot.py`
- `bot_plugins/assistant.py`
- `startup/startup.py`

Integration flow:

- `startup.start_bot()` calls `init_bot(client)`
- `plugins/bot.py` starts a Telethon bot client using `BOT_TOKEN`
- `startup.load_bot_plugins()` loads `bot_plugins/*.py`
- `bot_plugins/assistant.py` receives owner identity from the userbot account
- Help commands from userbot plugins are exposed through `CMD_LIST`

### Features

- Interactive help menu
- Inline query handler for `.help`
- Button navigation
- Pagination for plugin menus
- Owner-only assistant toggle
- Private message relay between users and owner
- Usage stats stored in `DB/assistant_db.json`

### Deployment notes

- Uses a **separate bot token** from your session maker bot
- Can run on the **same server/process as the userbot** in the current repo
- Can also be isolated onto another host if you refactor startup
- In the current default code path, the assistant bot is started as part of `main.py`

### How to interact with it

#### Owner

- `/start` — open management menu
- `/help` — assistant help
- `/assistant on` — enable relay mode
- `/assistant off` — disable relay mode
- `/assistant status` — see current status

#### Regular users

- `/start` — see greeting/help
- Send a message — it is forwarded to the owner if assistant mode is enabled

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Buttons do not respond | Bot not running or user lacks access | Confirm `BOT_TOKEN` and owner/sudo setup |
| No messages forwarded | Assistant mode disabled | Use `/assistant on` |
| Owner replies do not reach users | Reply not sent to mapped forwarded message | Reply directly to the forwarded bot message |
| Help menu empty | Plugins not registered into `CMD_LIST` | Verify userbot plugins loaded correctly |

---

## Deployment Guide

### Step-by-step setup order

#### 1) Session Maker Bot Setup

```bash
cd /path/to/CipherElite
export SESSION_BOT_TOKEN="your_session_bot_token"
export API_ID="your_api_id"
export API_HASH="your_api_hash"
python3 v26_session_maker_bot.py
```

#### 2) V26 Userbot Setup

```bash
cd /path/to/CipherElite
cp sample.env .env
# edit .env with your real values
pip3 install -r requirements.txt
python3 main.py
```

#### 3) Assistant Bot Setup

Add these to `.env` before starting the userbot:

```env
BOT_TOKEN=123456:your_assistant_bot_token
V26_BOT_USERNAME=@YourAssistantBotUsername
SUDO_USERS=123456789
LOG_CHAT_ID=-1001234567890
```

#### 4) Integration & Testing

- Generate a `V26_SESSION`
- Start `main.py`
- Run `.help` from your Telegram account
- Open the assistant bot and test `/start`
- Toggle `/assistant on`
- Send a private message to the assistant bot from another account
- Confirm relay + reply path works

#### 5) 24/7 Deployment

Recommended order:

- **Session Maker Bot**: separate VPS, container, or temporary process
- **Userbot**: primary VPS / Railway / Docker / tmux session
- **Assistant Bot**: same runtime as the userbot unless you intentionally split it out

### Minimum requirements

- Python 3.10+
- Telegram API credentials (`API_ID`, `API_HASH`)
- One bot token for the assistant bot
- One separate bot token for the session maker bot
- A secure host that can stay online for `main.py`
- Write access to the local `DB/` directory

### Security best practices

- Never share `V26_SESSION`
- Never reuse `SESSION_BOT_TOKEN` as `BOT_TOKEN`
- Keep `SUDO_USERS` limited to accounts you fully trust
- Use a private `LOG_CHAT_ID`
- Rotate bot tokens if leaked
- Limit repeated login attempts to avoid flood waits
- Keep the session maker isolated from your main runtime

---

## Communication Between Bots

### How they interact

The three components are separate, but linked:

- The **session bot** creates the protected session used by the **userbot**
- The **userbot** loads command metadata used by the **assistant bot** help menu
- The **assistant bot** sends inline/menu UI and can relay messages back to the userbot owner

### Message flow diagram

```text
[Telegram User]
     |
     | /generate + phone + OTP + 2FA
     v
[Session Maker Bot]
     |
     | returns V26_SESSION
     v
[Userbot Owner]
     |
     | stores session in .env
     v
[V26 Userbot]
     |
     | loads plugins + registers help data
     +--------------------+
                          |
                          v
                  [Assistant Bot UI]
                          |
                          | /start, /help, inline menus
                          | PM relay to owner
                          v
                  [End users / owner]
```

### Data exchange

| Source | Target | Data |
|---|---|---|
| Session Maker Bot | Userbot owner | Protected `V26_SESSION` |
| Userbot plugins | Assistant help layer | Command names + descriptions in `CMD_LIST` |
| Assistant bot | Owner | Forwarded user messages, stats, toggles |
| Owner | Assistant bot | Replies and control commands |

---

## FAQ & Troubleshooting

### Common issues

#### Why does a normal Telethon StringSession not work?
Because V26 expects a protected string that can be decoded by `utils/v26_security.py`. The repo checks for the V26 format and tells you to regenerate it with the V26 session maker.

#### Is the assistant bot a separate Telegram identity?
Yes. It uses its own `BOT_TOKEN` and `V26_BOT_USERNAME`, even though the current code starts it from the same runtime as the userbot.

#### Should the session bot stay online forever?
No. It can be started only when you need to generate new sessions, though many operators keep it online for convenience.

#### Why do some commands work only for me?
Sensitive commands are restricted by owner/sudo decorators. Add trusted IDs to `SUDO_USERS`.

#### Where is assistant state stored?
In `DB/assistant_db.json`.

### Performance tips

- Run the userbot on a stable VPS
- Avoid repeated restart loops during login flows
- Keep the session maker separate from heavy plugin activity
- Use a minimal sudo list
- Watch plugin count and startup time as you add more modules

---

## Visual Diagrams

### 1) System architecture

```text
+-------------------------+        +-------------------------+
| V26 Session Maker Bot   |        | V26 Userbot             |
| v26_session_maker_bot.py|------->| main.py + startup/      |
| Aiogram + Telethon      | session| Telethon user client    |
+-------------------------+        +------------+------------+
                                                |
                                                | help data / CMD_LIST
                                                v
                                   +------------+------------+
                                   | V26 Assistant Bot       |
                                   | plugins/bot.py          |
                                   | bot_plugins/assistant.py|
                                   +-------------------------+
```

### 2) Deployment flow

```text
Create Session Bot
      -> generate V26_SESSION
      -> configure .env
      -> start main.py
      -> verify .help and /start
      -> enable /assistant on
      -> deploy 24/7
```

### 3) Plugin system architecture

```text
plugins/*.py
   -> init(client)
   -> optional register_commands()
   -> add_handler(plugin_name, commands, description)
   -> stored in CMD_LIST
   -> exposed by assistant inline help menu
```

### 4) Session protection flow

```text
Raw Telethon StringSession
      -> _v26_embed()
      -> V26_SESSION
      -> stored in .env
      -> v26_protect()
      -> restored StringSession
      -> TelegramClient(...)
```

---

## Final Recommendation

If you are setting up V26 from scratch:

1. **Deploy the Session Maker Bot first**
2. **Generate one clean `V26_SESSION`**
3. **Configure and run the Userbot**
4. **Enable and test the Assistant Bot UI**
5. **Move the Userbot to a 24/7 host**

That order keeps the setup clean, secure, and easy to debug.
