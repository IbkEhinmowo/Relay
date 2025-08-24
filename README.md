<!-- @format -->

# Relay: The Agentic Discord Bot

Relay is an open-source, agentic Discord bot that goes far beyond simple chat. Powered by LLMs and designed for extensibility, Relay can use tools, remember user-specific information, and automate real-world workflows—all from your Discord server.

## ✨ Features

- **Conversational AI**: Natural, multi-turn conversations powered by LLMs.
- **Tool Use**: Relay can call external APIs and integrations (weather, Notion, reminders, and more).
- **Persistent Memory**: Per-user memory—Relay remembers facts, preferences, and context for each user.
- **Automation**: Orchestrate multi-step workflows (e.g., “Summarize this article and send it to my Notion”).
- **Extensible**: Easily add new tools, integrations, and memory types.

## 🚀 Example Interactions

> **User:** What’s the weather in Tokyo?  
> **Relay:** It’s 27°C and sunny in Tokyo.

> **User:** Remember that my favorite color is green.  
> **Relay:** Got it! I’ll remember your favorite color.

> **User:** What’s my favorite color?  
> **Relay:** You told me it’s green.

> **User:** Summarize this link and add it to my Notion.  
> **Relay:** (Summarizes and updates your Notion page)

> **User:** Summarize the latest AI news, add the summary to my Notion, and update me when you're done.
> **Relay:** (Fetches news, summarizes, updates Notion, and sends a Discord message)

> **User:** Summarize this link and add it to my Notion.  
> **Relay:** (Summarizes and updates your Notion page)

## 🛠️ How It Works

- **LLM-Powered**: Uses a large language model for understanding and reasoning.
- **Tool Calling**: Relay can call Python functions (“tools”) to fetch data, send messages, or update external services.
- **Memory**: User-specific memory is stored in Redis for fast, scalable recall.
- **Discord Integration**: All features are accessible via Discord chat.

## 🧩 Extending Relay

Want to add a new tool or integration? Just drop a new Python function in the tools directory and register it. Relay’s architecture makes it easy to plug in new capabilities.


## ⚠️ Safety & Confirmation

Relay always confirms irreversible or potentially destructive actions (like deleting memory, sending emails, or overwriting data) before proceeding.

**Example:**

> **User:** Delete all my memory.
> **Relay:** Are you sure you want to delete all your memory? Reply with 'yes' to confirm.

Relay will only proceed if you explicitly confirm, ensuring your data and actions are always protected from accidental loss.