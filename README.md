# V26 USERBOT

> 🛑 **STOP PAYING FOR HOSTING!**
> **V26 Userbot comes with FREE 24/7 HOSTING via our exclusive bot.**
> No Credit Card. No VPS needed. [Deploy in 30 seconds](#-deployment).

<p align="center">
  <img src="images/cipher.jpg" alt="V26 Userbot Logo" width="300" height="300">
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=F77247&width=450&lines=The+First+Anti-Hack+Userbot;Built+by+Thanos+Pro+Organization;Native+AI+%7C+Smart+Plugins+%7C+Secure;Deploy+Free+in+30+Seconds" alt="Typing SVG" />
</p>

<p align="center">
    <a href="https://github.com/rishabhops/CipherElite/stargazers"><img src="https://img.shields.io/github/stars/rishabhops/CipherElite?label=Stars&style=for-the-badge&logo=github&color=F10070" alt="GitHub Stars"></a>
    <a href="https://github.com/rishabhops/CipherElite/network/members"><img src="https://img.shields.io/github/forks/rishabhops/CipherElite?label=Forks&style=for-the-badge&logo=github&color=F10070" alt="GitHub Forks"></a>
    <a href="https://github.com/rishabhops/CipherElite/issues"><img src="https://img.shields.io/github/issues/rishabhops/CipherElite?label=Issues&style=for-the-badge&logo=github&color=F10070" alt="GitHub Issues"></a>
    <a href="https://github.com/rishabhops/CipherElite/blob/elite/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&logo=github" alt="License" /></a>
    <a href="https://cipherelite.in"><img src="https://img.shields.io/badge/📖_Docs-cipherelite.in-F10070?style=for-the-badge" alt="Documentation"></a>
</p>

<p align="center">
    <b>The Smartest, Most Secure Telegram Userbot (2026)</b>
</p>

---

## 📑 TABLE OF CONTENTS
- [About](#-about)
- [Why V26 Userbot?](#-features)
- [Deployment](#-deployment)
  - [Method 1: Telegram Deployer (Free)](#-method-1-telegram-deployer-recommended)
  - [Method 2: VPS / Terminal](#-method-2-vps--terminal-manual)
- [Configuration](#️-configuration-vars)
- [Support & Community](#-support--updates)
- [Credits](#-credits)

---

## 📖 ABOUT

**V26 Userbot** isn't just another userbot—it is a **Self-Healing Automation Suite**.

Built on **Telethon** as a V26-branded CipherElite fork, it solves the biggest problems in Telegram automation:
1.  **Security:** Our proprietary `V26_SESSION` prevents hackers from stealing your account.
2.  **Stability:** Our **Smart Plugin Manager** auto-detects and installs missing dependencies (`pip install`) so your bot never crashes.
3.  **Accessibility:** We provide **Free Hosting** so anyone can use it.

### 🛠 Tech Stack
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)
![Telethon](https://img.shields.io/badge/Library-Telethon-orange?style=flat&logo=telegram)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?style=flat&logo=mongodb)

---

## ⚡ FEATURES

| Feature | Description |
| :--- | :--- |
| **🧠 Smart Plugin Manager** | **(Exclusive)** Auto-scans plugin code, installs missing libraries/requirements instantly. Zero crashes. |
| **🛡️ Anti-Hack Session** | Uses `V26_SESSION` encryption. If a hacker steals your string, they **cannot** use it on other tools. |
| **🤖 Native AI** | Integrated AI commands for auto-replies, summaries, and chat assistance. |
| **⚡ Free Hosting** | We provide a dedicated Deployer Bot that hosts your userbot for free (24/7). |
| **🎭 Native Fun Plugins** | Custom-written Games, Animations, and 'Magic' commands with **Zero Lag**. |
| **🔄 Safe Updates** | Update your bot without losing your `vars` or configuration. |
| **📊 Analytics** | Built-in performance monitoring and ping checks. |
| **🔌 60+ Official Plugins** | 60+ official plugins by Rishabh Anand + growing community plugin library. |

---

## 🚀 DEPLOYMENT

> 📚 **For detailed step-by-step guides, screenshots & video tutorials, visit the full documentation:**
>
> **👉 [cipherelite.in/docs](https://cipherelite.in/docs)**

---

### 🎥 Watch: How to Deploy in 60 Seconds (Free)

<div align="center">
  <a href="https://www.youtube.com/watch?v=XBHyZyJcv5c">
    <img src="https://img.youtube.com/vi/XBHyZyJcv5c/maxresdefault.jpg" alt="Watch V26 Userbot Deployment Tutorial" width="100%">
  </a>
  <br>
  <b>▶️ Click here to watch the Tutorial</b>
</div>

<br>

---

### 📲 Method 1: Telegram Deployer (Recommended)
**No coding required. No Credit Card.**

> 📖 **Full Detailed Guide → [cipherelite.in/docs/telegram-deploy](https://cipherelite.in/docs/telegram-deploy)**

**Quick Steps:**

1.  **Fork this Repository:**
    * Click the `Fork` button (top right on GitHub).
    * *Critical:* You must use **your own forked repo link**, not the original.

2.  **Get Your Session:**
    * Start [@v26_session_maker_bot](https://t.me/v26_session_maker_bot) on Telegram.
    * Follow steps to generate your `V26_SESSION`.

3.  **Deploy:**
    * Go to **[@elitedeployerbot](https://t.me/elitedeployerbot)**.
    * Send the link to **your forked repository**.
    * Enter variables when prompted.
    * ✅ Your bot is live!

> **Why use Elite Deployer?**
> * 🖥️ Real Server Hosting — Free 24/7
> * 📡 Live Logs Dashboard in Telegram
> * ⚡ Instant Restart / Variable Editing without re-deploying

---

### 💻 Method 2: VPS / Terminal (Manual)
If you prefer full control (Termux/Ubuntu/Debian), use `tmux` to keep the bot running 24/7.

> 📖 **Full Detailed Guide → [cipherelite.in/docs/vps-deploy](https://cipherelite.in/docs/vps-deploy)**

```bash
# 1. Update System & Install Dependencies (including tmux)
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip git tmux -y

# 2. Clone the Repository
git clone https://github.com/lackx741-tech/CipherElite
cd CipherElite

# 3. Setup Configuration
# Copy the sample env file to a real .env file
cp sample.env .env

# Edit the file to add your API_ID, HASH, and SESSION
nano .env
# (Press Ctrl+O to save, Enter to confirm, Ctrl+X to exit)

# 4. Install Python Requirements
pip3 install -r requirements.txt

# 5. Run 24/7 using Tmux
tmux new -s cipher
python3 main.py

# To check your bot later, type tmux attach -t cipher in your terminal.
# To exit the logs without stopping the bot, press Ctrl+B then D.
```

---

## ⚙️ CONFIGURATION VARS

> 📖 **Full Configuration Reference → [cipherelite.in/docs/configuration](https://cipherelite.in/docs/configuration)**

| Variable | Description |
|---|---|
| `API_ID` | Get from my.telegram.org |
| `API_HASH` | Get from my.telegram.org |
| `V26_SESSION` | Required. Get from @v26_session_maker_bot |
| `V26_BOT_USERNAME` | Assistant bot username with `@` |
| `LOG_CHAT_ID` | Private Channel ID for Logs |
| `SUDO_USERS` | Your User ID (for admin control) |

🛡️ **SECURITY NOTICE:**
> V26 Userbot uses a custom locked session protocol. Standard StringSessions, CipherElite sessions, and generic Telethon tools will NOT work with `V26_SESSION`.
> This creates a security layer: even if your session file is stolen, the embedded V26 salts must be stripped by `v26_protect()` before Telethon can use it.

### 🔐 V26 Session Generation Guide

1. Generate your session only with **[@v26_session_maker_bot](https://t.me/v26_session_maker_bot)**.
2. The session bot wraps your real Telethon session with a V26-only protection layer before you store it.
3. V26 removes that protection internally at startup with `v26_protect()` and then hands the recovered session to Telethon.
4. This design is intentional and **not compatible** with CipherElite / `ELITE_SESSION` strings.
5. If a V26 session leaks, it is not directly usable in generic Telethon tooling without V26's internal protection logic.

---

## 💫 SUPPORT & UPDATES

Join our growing community for plugins, help, and updates.

<p align="center">
<a href="https://t.me/THANOS_PRO"><img src="https://img.shields.io/badge/📢_Updates_Channel-Join-red?style=for-the-badge&logo=telegram"></a>
<a href="https://t.me/thanosprosss"><img src="https://img.shields.io/badge/👥_Support_Group-Join-blue?style=for-the-badge&logo=telegram"></a>
<a href="https://t.me/CipherElite_Userbot"><img src="https://img.shields.io/badge/🔌_Plugin_Channel-Browse-orange?style=for-the-badge&logo=telegram"></a>
<a href="https://cipherelite.in/docs"><img src="https://img.shields.io/badge/📖_Full_Docs-Read-F10070?style=for-the-badge"></a>
</p>

---

## 🌟 CREDITS & OWNER

<h3 align="center">Rishabh Anand</h3>
<p align="center">
<b>Lead Developer & Founder of Thanos Pro Organization</b>
</p>
<p align="center">
<a href="https://t.me/thanosceo"><img src="https://img.shields.io/badge/Contact-Telegram-blue?style=flat-square&logo=telegram"></a>
<a href="https://github.com/rishabhops"><img src="https://img.shields.io/badge/Follow-GitHub-black?style=flat-square&logo=github"></a>
<a href="https://instagram.com/xrishabhanand"><img src="https://img.shields.io/badge/Follow-Instagram-E4405F?style=flat-square&logo=instagram"></a>
</p>

### **Acknowledgments:**
* **Telethon:** For the foundational library.
* **Open Source Community:** For the continuous inspiration.

---

## ⚖️ DISCLAIMER

> This userbot is an open-source educational project. The developers (Rishabh Anand & Thanos Pro Org) are not responsible for any account bans or restrictions caused by improper usage of this tool.

---

<p align="center">
<b>Enjoying V26 Userbot? Please drop a ⭐ Star on the repository!</b>
</p>
