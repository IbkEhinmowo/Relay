<!-- @format -->

# Relay: The Agentic Discord Bot

Relay is an open-source, agentic Discord bot that goes far beyond simple chat. Powered by LLMs and designed for extensibility, Relay can use tools, remember user-specific information, and automate real-world workflows—all from your Discord server.

## ✨ Features

- **Conversational AI**: Natural, multi-turn conversations powered by LLMs.
- **Tool Use**: Relay can call external APIs and integrations (weather, Notion, reminders, and more).
- **Persistent Memory**: Per-user memory—Relay remembers facts, preferences, and context for each user.
- **Automation**: Orchestrate multi-step workflows (e.g., “Summarize this article and send it to my Notion”).
- **Extensible**: Easily add new tools, integrations, and memory types.
- **Open Source**: Community-driven and fully hackable.

## 🚀 Example Interactions

> **User:** What’s the weather in Tokyo?  
> **Relay:** It’s 27°C and sunny in Tokyo.

> **User:** Remember that my favorite color is green.  
> **Relay:** Got it! I’ll remember your favorite color.

> **User:** What’s my favorite color?  
> **Relay:** You told me it’s green.

> **User:** Summarize this link and add it to my Notion.  
> **Relay:** (Summarizes and updates your Notion page)

> **User:** Summarize the latest AI news, add the summary to my Notion, and send a reminder to my Discord.
> **Relay:** (Fetches news, summarizes, updates Notion, and sends a Discord message)

> **User:** Analyze this PDF report, extract all tables, and update our project’s Google Sheet. Then, email the results to my manager.
> **Relay:** (Extracts tables, updates Google Sheet, and sends an email)

> **User:** Monitor this website for changes and alert me on WhatsApp if anything changes. Also, keep a log of all changes in a database.
> **Relay:** (Monitors site, sends WhatsApp alerts, and logs changes)

> **User:** Transcribe this audio file, summarize the key points, and create a Trello card for each action item.
> **Relay:** (Transcribes, summarizes, and creates Trello cards)

> **User:** What’s the weather in Tokyo?  
> **Relay:** It’s 27°C and sunny in Tokyo.

> **User:** Remember that my favorite color is green.  
> **Relay:** Got it! I’ll remember your favorite color.

> **User:** What’s my favorite color?  
> **Relay:** You told me it’s green.

> **User:** Summarize this link and add it to my Notion.  
> **Relay:** (Summarizes and updates your Notion page)

## 🛠️ How It Works

- **LLM-Powered**: Uses a large language model for understanding and reasoning.
- **Tool Calling**: Relay can call Python functions (“tools”) to fetch data, send messages, or update external services.
- **Memory**: User-specific memory is stored in Redis for fast, scalable recall.
- **Discord Integration**: All features are accessible via Discord chat.

## 🧩 Extending Relay

Want to add a new tool or integration? Just drop a new Python function in the tools directory and register it. Relay’s architecture makes it easy to plug in new capabilities.

## 📦 Setup

1. Clone this repo
2. Install requirements: `pip install -r requirements.txt`
3. Set up your `.env` with your Discord bot token and any API keys
4. Start Redis server
5. Run the bot: `python Core/Integrations/discord_bot.py`
6. Invite Relay to your Discord server and start chatting!

## 📝 Community & Contributing

---

## ⚠️ Safety & Confirmation

Relay always confirms irreversible or potentially destructive actions (like deleting memory, sending emails, or overwriting data) before proceeding.

**Example:**

> **User:** Delete all my memory.
> **Relay:** Are you sure you want to delete all your memory? Reply with 'yes' to confirm.

Relay will only proceed if you explicitly confirm, ensuring your data and actions are always protected from accidental loss.

Relay is built for the community—PRs, issues, and feature requests are welcome!  
Join us in building the next generation of agentic Discord bots.
