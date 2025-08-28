<!-- @format -->

# Relay - Extensible Multi-Tool AI Agent

<div align="center">
  <img src="./assets/icon-512.png" alt="Relay Icon" width="100">
</div>



![Demo GIF](https://your-gif-url-here.com/demo.gif) <!-- Replace with a link to your demo GIF -->

Relay is an extensible, multi-tool AI agent built in Python using an asynchronous architecture. It leverages a tool-calling LLM to interact with external APIs, perform complex tasks, and maintain conversation state, demonstrating a robust framework for creating autonomous agents.

> **Disclaimer!** While this demo uses Discord, the core agent logic is decoupled from the chat interface and could be connected to other platforms like Slack, web applications, or automated scripts or Schedular. I simply used discord for tha ease of testing

---

## Key Features & Capabilities

This isn't just a chatbot; it's an engineered system with a powerful set of capabilities:

- **Multi-Step Tool Chaining:** Relay can understand complex, multi-part requests and chain multiple tools together to find a solution. For example, it can search for news, scrape an article from the results, and then summarize the content, all from a single prompt.
- **Web Intelligence:**
  - **Web & News Search:** Access up-to-date information from the internet & **Weather:** Get the current weather for any location.
  - **Intelligent Web Scraper:** Scrape and parse the content of any URL.
    - *Evades common anti-botting measures using stealth techniques, enabling data extraction from modern, dynamic websites.*
- **Persistent Memory:** Relay remembers key details about users across conversations using a Redis-backed memory store, allowing for personalized interactions.

- **External Integrations:**
  - **Notion:** Update & Create Notion pages directly from Discord.
  - **Discord:** Can send messages programmatically(without input).

---

## System Architecture

The project is designed as a decoupled, event-driven system, showcasing modern software engineering practices.
- **Asynchronous Core:** Built on Python's `asyncio` to handle concurrent I/O operations efficiently, ensuring the bot remains responsive while waiting for API calls.
- **State & History Management:** Utilizes a Redis database to store conversation history and user-specific memories, enabling context-aware interactions and preventing state loss.
- **Modular ToolSet:** Tools are designed as independent modules, making the system VERY easily extensible with new capabilities. But for now it'll remain a fun to play with discord bot

---

## Getting Started

### Prerequisites

- Python 3.10+
- Redis
- An active Cerebras API key and other necessary API keys for the tools.

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/IbkEhinmowo/Relay.git
    cd Relay
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure your environment variables:**
    Create a `.env` file in the root directory and populate it with your API keys:

    ```
    CEREBRAS_API_KEY="YOUR_CEREBRAS_KEY"
    BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
    WEATHERSTACK_API_KEY="YOUR_WEATHERSTACK_KEY"
    # ... other keys ...
    ```

4.  **Run the bot:**
    ```bash
    python discord_bot.py
    ```

---

## Example "Show-Off" Demo

To see the full power of the agent's reasoning capabilities, try a multi-step prompt like this:

> **@Relay Please research the new NVIDIA Blackwell chips. Create a new Notion page titled 'NVIDIA Blackwell Research' with a summary of your findings, and then send me a message here when you're done.**

This will trigger a complex chain of actions, showcasing the agent's potential: `web_search_result` -> `scrape_url` -> `update_notion_page` -> `send_discord_message`.
