<!-- @format -->

# Relay - Extensible Multi-Tool AI Agent

![Demo GIF](https://your-gif-url-here.com/demo.gif) <!-- Replace with a link to your demo GIF -->

Relay is an extensible, multi-tool AI agent built in Python using an asynchronous architecture. It leverages a tool-calling LLM to interact with external APIs, perform complex tasks, and maintain conversation state, demonstrating a robust framework for creating autonomous agents.

> **Disclaimer!** While this demo uses Discord, the core agent logic is decoupled from the chat interface and could be connected to other platforms like Slack, web applications, or automated scripts.

---

## Key Features & Capabilities

This isn't just a chatbot; it's an engineered system with a powerful set of capabilities:

- **Multi-Step Tool Chaining:** Relay can understand complex, multi-part requests and chain multiple tools together to find a solution. For example, it can search for news, scrape an article from the results, and then summarize the content, all from a single prompt.
- **Web Intelligence:**
  - **Web & News Search:** Access up-to-date information from the internet.
  - **Intelligent Web Scraper:** Scrape and parse the content of any URL.
- **Persistent Memory:** Relay remembers key details about users across conversations using a Redis-backed memory store, allowing for personalized interactions.
- **Real-World Knowledge:**
  - **Weather:** Get the current weather for any location.
- **External Integrations:**
  - **Notion:** Update & Create Notion pages directly from Discord.
  - **Discord:** Can send messages programmatically.

---

## System Architecture

The project is designed as a decoupled, event-driven system, showcasing modern software engineering practices.

```mermaid
graph TD
    A[Discord User] -- @mention --> B(Discord Bot);
    B -- Creates Event --> C{LLM Agent (Cerebras)};
    C -- Decides to Use Tool --> D[ToolSet];
    D -- Executes Tool --> E(External APIs & functions e.g., Scraping, Web Search, Notion writing);
    E -- Returns Data --> D;
    D -- Returns Result --> C;
    C -- Needs Memory/History --> F(Redis);
    F -- Returns Data --> C;
    C -- Generates Final Response --> B;
    B -- Sends Message --> A;
```

- **Asynchronous Core:** Built on Python's `asyncio` to handle concurrent I/O operations efficiently, ensuring the bot remains responsive while waiting for API calls.
- **State & History Management:** Utilizes a Redis database to store conversation history and user-specific memories, enabling context-aware interactions and preventing state loss.
- **Modular ToolSet:** Tools are designed as independent modules, making the system easily extensible with new capabilities.

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

> **@Relay Can you find the latest news about the new NVIDIA Blackwell chips, then scrape the first article and tell me the key takeaways?**

This will trigger a chain of actions: `web_news_result` -> `scrape_url` -> Final Answer.
