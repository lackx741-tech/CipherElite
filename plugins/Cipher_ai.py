# =============================================================================
#  CipherElite Userbot Plugin - Cipher AI (Google Gemini)
#  With Repository Data Access & Real Chat Memory
#
#  Plugin Name:    cipher_ai
#  Author:         CipherElite Dev (@rishabhops)
#  Repository:     https://github.com/rishabhops/CipherElite
#
#  LICENSE:        MIT
# =============================================================================

import asyncio
import google.generativeai as genai
import aiohttp
import json
from telethon import events
from utils.utils import CipherElite
from utils.decorators import rishabh
from utils.helpers import (
    V26_REPOSITORY_BRANCH,
    V26_REPOSITORY_NAME,
    V26_REPOSITORY_OWNER,
    V26_REPOSITORY_URL,
)
from plugins.bot import add_handler

# Store conversation history per chat
conversation_history = {}

# System prompt - Custom identity and behavior
SYSTEM_PROMPT = f"""You are **V26 AI**, a specialized AI assistant created for the **V26 Userbot**.

**ABOUT YOU (ONLY MENTION IF EXPLICITLY ASKED):**
• **Name:** V26 AI
• **Created by:** Rishabh Anand (@rishabhops)
• **Owner/Creator's Telegram:** @thanosceo
• **Project:** V26 Userbot - Advanced Telegram Userbot
• **Repository:** {V26_REPOSITORY_URL}
• **Primary Repo Branch:** elite

**YOUR PURPOSE:**
You are integrated into the V26 Telegram Userbot. Your primary focus is helping with V26 features, deployment, and coding. 
HOWEVER, you are also a general-purpose AI. You MUST answer general everyday questions (like career advice, education, general knowledge, etc.) naturally and helpfully without restricting yourself to technical topics.

**PERSONALITY & BEHAVIOR:**
1. ONLY introduce yourself or mention your creators if the user EXPLICITLY asks questions like "who are you", "who made you", or "what is your name". Do NOT inject your identity into normal answers.
2. Answer whatever the user asks directly. Do not pivot the conversation back to V26 unless the user's question is actually about the bot.
3. Be helpful, concise, and professional. Act like a natural conversational partner.
4. Use **bold formatting** for important keywords.
5. For simple questions: Keep SHORT (1-2 paragraphs).
6. For complex questions: Provide COMPLETE detailed answers using bullet points and numbered lists.
7. Never apologize unnecessarily or add disclaimers about being an AI.
8. When asked about deployment or setup for V26: Provide accurate, step-by-step instructions based on V26's actual structure (Telethon, Python 3.8+, VPS deployment, SQLite databases).
"""

async def fetch_repository_data(
    owner=V26_REPOSITORY_OWNER,
    repo=V26_REPOSITORY_NAME,
    branch=V26_REPOSITORY_BRANCH,
):
    """Fetch repository structure and README from GitHub"""
    try:
        async with aiohttp.ClientSession() as session:
            # Fetch README
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
            async with session.get(readme_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    readme_content = await resp.text()
                else:
                    readme_content = ""
            
            # Fetch setup/requirements file
            setup_urls = [
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/requirements.txt",
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/setup.md",
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/SETUP.md",
            ]
            
            setup_content = ""
            for url in setup_urls:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        setup_content = await resp.text()
                        break
            
            return {
                "readme": readme_content[:2000] if readme_content else "",  # Limit size
                "setup": setup_content[:2000] if setup_content else "",
                "has_data": bool(readme_content or setup_content)
            }
    except Exception as e:
        print(f"⚠️ Failed to fetch repo data: {e}")
        return {
            "readme": "",
            "setup": "",
            "has_data": False
        }


def init(client):
    """Initialize the V26 AI plugin"""
    try:
        from plugins.ai_setup import ai_config  # Import centralized config
    except ImportError:
        print("❌ ERROR: ai_setup.py not found! Please create it first.")
        return False
    
    commands = [
        f".ai <question>   — Ask V26 AI a question",
        f".aiclear         — Clear conversation history",
        f".aiinfo          — Show AI info"
    ]
    add_handler("cipher_ai", commands, "V26 AI - Powered by Google Gemini with Repo Access")
    
    async def make_ai_request(messages, repo_context=""):
        """Make request to Google Generative AI using native chat history"""
        try:
            api_key = ai_config.get_api_key()
            if not api_key:
                return "❌ **API Key not configured!**\n\nUse `.setai <key>` to set up Google Gemini API.\n\n🔗 Get key: https://aistudio.google.com/"
            
            genai.configure(api_key=api_key)
            
            # Create enhanced system instruction with repo context
            enhanced_prompt = SYSTEM_PROMPT
            if repo_context:
                enhanced_prompt += f"\n\n**CURRENT REPOSITORY CONTEXT:**\n{repo_context}"
            
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=enhanced_prompt
            )
            
            # Convert messages to Gemini's native history format for better context memory
            gemini_history = []
            for msg in messages:
                # Gemini expects roles to be 'user' or 'model'
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg["content"]]})
            
            # Allow complete responses and pass the properly structured history array
            response = model.generate_content(
                gemini_history,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.7,
                    top_p=0.9,
                )
            )
            return response.text
            
        except Exception as e:
            return f"❌ **Error:** {str(e)[:100]}"
    
    def estimate_response_type(query):
        """Estimate if question needs short or detailed answer"""
        short_keywords = ["what is", "who is", "when", "where", "how many", "define", "meaning", "your name", "who made", "who created"]
        complex_keywords = ["how to", "deploy", "setup", "install", "tutorial", "guide", "step", "process", "configure", "build", "create", "write code", "cipherelite", "v26", "userbot"]
        
        query_lower = query.lower()
        
        # Check for complex/tutorial questions
        if any(keyword in query_lower for keyword in complex_keywords):
            return "detailed"
        
        # Check if it's a simple question
        if any(keyword in query_lower for keyword in short_keywords):
            return "short"
        
        return "medium"
    
    def format_response(response, response_type):
        """Format response based on type"""
        response = response.strip()
        
        # Remove only truly unnecessary phrases
        unnecessary_phrases = [
            "I'm glad you asked. ",
            "Great question! ",
            "Thank you for asking. ",
            "Let me explain: ",
            "Sure, here's ",
        ]
        
        for phrase in unnecessary_phrases:
            if response.startswith(phrase):
                response = response[len(phrase):]
        
        response = response.strip()
        
        # For short answers, be strict about length
        if response_type == "short" and len(response) > 500:
            sentences = response.split(". ")
            response = ". ".join(sentences[:3]) + "."
        
        # For detailed answers, keep complete
        elif response_type == "detailed" and len(response) > 3500:
            response = response + "\n\n💡 *Response may continue in next message if too long*"
        
        return response
    
    @CipherElite.on(events.NewMessage(pattern=r"\.ai(?:\s+(.*))?"))
    @rishabh()
    async def ai_handler(event):
        """Handle AI queries with repository context"""
        try:
            if not ai_config.is_enabled():
                await event.reply(
                    "❌ **API Key Not Set**\n\n"
                    "Use `.setai <your_gemini_api_key>`\n\n"
                    "🔗 Get key: https://aistudio.google.com/"
                )
                return
            
            query = event.pattern_match.group(1)
            if not query:
                await event.reply(
                    "❓ **How to use V26 AI:**\n\n"
                    "**About Me:**\n"
                    "`.ai Who are you?`\n"
                    "`.ai Who made you?`\n\n"
                    "**V26 Help:**\n"
                    "`.ai How to deploy V26?`\n"
                    "`.ai What is V26 Userbot?`\n"
                    "`.ai V26 setup guide`\n\n"
                    "**General Questions:**\n"
                    "`.ai What is Python?`"
                )
                return
            
            if len(query) > 2000:
                await event.reply("📝 **Query too long!** Max 2000 characters.")
                return
            
            thinking_msg = await event.reply("🤔 **V26 AI thinking...**")
            print(f"🤖 Processing AI query: {query[:50]}...")
            
            # Estimate response type
            response_type = estimate_response_type(query)
            print(f"📊 Detected response type: {response_type}")
            
            # Fetch repository data ONLY if question is specifically about V26
            repo_context = ""
            # Keep legacy CipherElite terms during the V26 migration so old phrasing still resolves repo help.
            userbot_keywords = ["cipherelite", "cipher elite", "v26", "v26 userbot", "userbot setup", "userbot deploy", "this bot's repo"]
            
            if any(keyword in query.lower() for keyword in userbot_keywords):
                await thinking_msg.edit("🤔 **V26 AI thinking...** (scanning repository...)")
                print("📚 Fetching V26 repository data...")
                repo_data = await fetch_repository_data()
                if repo_data["has_data"]:
                    repo_context = f"README excerpt:\n{repo_data['readme']}\n\nSetup guide:\n{repo_data['setup']}"
                    print("✅ Repository data fetched successfully")
                else:
                    print("⚠️ Could not fetch repository data")
            
            chat_id = event.chat_id
            if chat_id not in conversation_history:
                conversation_history[chat_id] = []
            
            # Add user query to history
            conversation_history[chat_id].append({"role": "user", "content": query})
            
            # Keep history limited to last 20 messages (10 exchanges) for longer memory
            if len(conversation_history[chat_id]) > 20:
                conversation_history[chat_id] = conversation_history[chat_id][-20:]
                # Google Gemini API requires the first message in the history array to be from a 'user'
                if conversation_history[chat_id][0]["role"] == "assistant":
                    conversation_history[chat_id] = conversation_history[chat_id][1:]
            
            try:
                response = await asyncio.wait_for(
                    make_ai_request(conversation_history[chat_id], repo_context),
                    timeout=40.0
                )
            except asyncio.TimeoutError:
                response = "⏰ **Timeout:** Request took too long. Try again or use `.aiclear` to reset."
            
            if response.startswith("❌"):
                await thinking_msg.edit(response)
                # If it failed, pop the last user message off so it doesn't break future context
                conversation_history[chat_id].pop()
                print(f"❌ AI error: {response}")
                return
            
            # Format response intelligently
            response = format_response(response, response_type)
            
            # Add AI response to history
            conversation_history[chat_id].append({"role": "assistant", "content": response})
            
            # Prepare final formatted message based on response type
            if response_type == "short":
                formatted = f"🤖 **Cipher AI:**\n\n{response}"
            
            elif response_type == "detailed":
                formatted = (
                    f"🤖 **Detailed Response:**\n\n"
                    f"{response}\n\n"
                    f"═════════════════════\n"
                    f"📌 **Q:** `{query[:60]}{'...' if len(query) > 60 else ''}`"
                )
            
            else:  # medium
                formatted = (
                    f"🤖 **Cipher AI Response:**\n\n"
                    f"{response}\n\n"
                    f"─────────────────\n"
                    f"💭 Q: `{query[:60]}{'...' if len(query) > 60 else ''}`"
                )
            
            # Handle message splitting for Telegram's 4096 char limit
            if len(formatted) > 4096:
                messages = []
                current_msg = ""
                
                # Split by double newline (paragraphs)
                parts = formatted.split("\n\n")
                
                for part in parts:
                    if len(current_msg) + len(part) + 4 > 4000:
                        if current_msg:
                            messages.append(current_msg.strip())
                        current_msg = part
                    else:
                        current_msg += "\n\n" + part if current_msg else part
                
                if current_msg.strip():
                    messages.append(current_msg.strip())
                
                # Send first message by editing thinking message
                if messages:
                    await thinking_msg.edit(messages[0])
                    
                    # Send remaining messages
                    for msg in messages[1:]:
                        await asyncio.sleep(0.5)
                        await event.reply(msg)
                    
                    print(f"✅ Response sent in {len(messages)} messages ({response_type} response)")
            else:
                await thinking_msg.edit(formatted)
                print(f"✅ AI response sent ({response_type} response, {len(response)} chars)")
            
        except Exception as e:
            print(f"❌ AI Handler Error: {e}")
            try:
                await event.reply(f"❌ **Error:** {str(e)[:100]}")
            except:
                pass
    
    @CipherElite.on(events.NewMessage(pattern=r"\.aiclear"))
    @rishabh()
    async def aiclear_handler(event):
        """Clear conversation history"""
        chat_id = event.chat_id
        if chat_id in conversation_history:
            msg_count = len(conversation_history[chat_id])
            del conversation_history[chat_id]
            await event.reply(f"🗑️ **Cleared!** {msg_count} messages removed. My memory is now fresh.")
        else:
            await event.reply("📭 **No history** in this chat.")
    
    @CipherElite.on(events.NewMessage(pattern=r"\.aiinfo"))
    @rishabh()
    async def aiinfo_handler(event):
        """Show AI info"""
        is_enabled = ai_config.is_enabled()
        status_emoji = "✅" if is_enabled else "❌"
        
        info = f"""🤖 **V26 AI - About Me**

**Name:** V26 AI
**Creator:** Rishabh Anand (@rishabhops)
**Owner:** @thanosceo
**Project:** V26 Userbot

{status_emoji} **Status:** {'Active' if is_enabled else 'Inactive'}
🔧 **Model:** Gemini 2.5 Flash
🌐 **Provider:** Google AI
💬 **Active Chats:** {len(conversation_history)}

📝 **Features:**
• Real Chat Memory Integration
• Custom Identity
• Repository Data Access
• V26-aware responses
• Intelligent response length

📚 **Commands:**
• `.ai <question>` - Ask me anything
• `.aiclear` - Clear memory in this chat
• `.aiinfo` - About me

🔗 **Links:**
• GitHub: https://github.com/lackx741-tech/CipherElite
• Creator: @rishabhops
• Owner: @thanosceo"""
        
        await event.reply(info)
    
    print("✅ V26 AI Plugin initialized (With Real Chat Memory)")
    return True
