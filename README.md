<!-- @format -->

# Relay - An Extensible, Multi-Tool AI Agent

<div align="center">
  <img src="./assets/icon-512.png" alt="Relay Icon" width="120">
</div>

<p align="center">
  <strong>A sophisticated, asynchronous AI agent that intelligently chains tools to perform complex, multi-step tasks.</strong>
</p>

---

## About The Project

Relay is a Python-based AI agent designed to demonstrate advanced concepts in software engineering and AI. It leverages a tool-calling LLM to interact with external APIs, manage state, and execute complex workflows. The system is built with an asynchronous, event-driven architecture, making it scalable and responsive.

While the current interface is a Discord bot, the core logic is decoupled, allowing for easy integration with other platforms like Slack, web apps, or automated scripts.

## Key Features

- **Intelligent Tool Chaining:** Relay can understand complex requests and dynamically chain multiple tools to achieve a goal. For example: _search for news on a topic, scrape a relevant article, and summarize it into a Notion page._
- **Scheduled & Automated Tasks:** Proactively schedule tasks using Celery and RedBeat. Relay can run jobs at specific times or intervals, enabling automated actions like sending daily news summaries or monitoring websites.
- **Web Intelligence:**
  - **Web & News Search:** Access up-to-date information from the internet.
  - **Stealth Web Scraper:** Intelligently scrapes and parses content from modern, dynamic websites, bypassing common anti-bot measures.
- **Persistent Memory:** Utilizes a Redis-backed memory store to remember user-specific details across conversations for personalized interactions.
- **External Integrations:**
  - **Notion:** Create and update Notion pages.
  - **Discord:** Send messages programmatically.
  - **Weather:** Get real-time weather data for any location.

## System Architecture

This project showcases a modern, decoupled software architecture:

- **Asynchronous Core:** Built on Python's `asyncio` for efficient, non-blocking I/O, ensuring the agent remains responsive while handling concurrent API calls.
- **Event-Driven Design:** Normalizes incoming requests into a standard `InputEvent` using Pydantic, making the system adaptable to various input sources.
- **State & History Management:** Employs Redis for robust conversation history and state management, enabling context-aware interactions.
- **Modular Toolset:** Tools are designed as independent, extensible modules, allowing for easy addition of new capabilities.

## Getting Started

### Prerequisites

- Python 3.10+
- Redis

- Cerebras API Key (and other keys for integrated services)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/IbkEhinmowo/Relay.git
    cd Relay
    ```
2.  **Set up a virtual environment and install dependencies:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Configure environment variables:**
    Create a `.env` file and add your API keys:
    ```env
    CEREBRAS_API_KEY="YOUR_CEREBRAS_KEY"
    BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
    WEATHERSTACK_API_KEY="YOUR_WEATHERSTACK_KEY"
    # ... other keys
    ```
4.  **Run the agent:**
    ```bash
    bash run_bot.sh
    ```

## Example "Show-Off" Demo

To see the agent's reasoning capabilities, try a multi-step prompt like this:

> **@Relay Please research the new NVIDIA Blackwell chips, create a Notion page titled 'NVIDIA Blackwell Research' with a summary, and then message me here when you're done.**

This prompt triggers a chain of actions: `web_search_result` → `scrape_url` → `create_notion_subpage` → `send_discord_message`, demonstrating the agent's ability to handle complex, autonomous workflows.
