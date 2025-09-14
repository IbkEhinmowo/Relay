<!-- @format -->

# Relay: An Extensible AI Workflow Agent

<div align="center">
  <img src="./assets/icon-512.png" alt="Relay Icon" width="120">
</div>

<p align="center">
  <strong>An extensible workflow agent implemented as a Discord bot using Python, FastAPI, Redis, and Celery with RedBeat.</strong>
</p>

---

## Overview

Relay is an LLM-driven autonomous scheduling agent that demonstrates how to build complex, multi-step automations. It can queue tasks for itself, trigger delayed actions, and run recurring workflows without hardcoded schedules.

The project showcases advanced orchestration across various services, including:

- **Web Research & Summarization:** Performing web searches, dynamically scraping content with Playwright, and summarizing the findings.
- **Dynamic Content Creation:** Creating and updating documents in Notion.
- **Notifications:** Sending alerts and messages through Discord.

Its Redis-centric architecture manages user-bound memory, message queues, and state, enabling context-aware workflows for multiple concurrent users. The web scraping module is designed with resilience to dynamic HTML and bot detection, ensuring reliable data extraction.

## Key Features

- **LLM-Driven Autonomous Scheduling:** Relay can schedule and execute tasks dynamically. For example, it can set a reminder to research a topic and then create a report at a specified time.
- **Multi-Step Automation:** Chains together multiple tools to complete complex workflows. A single prompt can trigger a sequence of actions like searching the web, scraping a site, summarizing content, and saving it to Notion.
- **Resilient Web Scraping:** The scraping module uses Playwright to handle dynamic websites and is designed to be resilient to anti-bot measures.
- **Redis-Centric Architecture:** Redis is used for:
  - **User-Bound Memory:** Maintaining context for individual users across sessions.
  - **Message Queues:** Managing tasks with Celery.
  - **State Management:** Tracking the state of ongoing workflows.
- **Extensible Toolset:** The agent's capabilities can be easily extended by adding new tools.

## System Architecture

- **Discord Bot Interface:** The primary interface for interacting with the agent for simplicity.
- **Python Backend:** The core logic is built with Python.
- **Redis:** Used as a message broker, for caching, and for storing persistent data.
- **Celery with RedBeat:** Manages and schedules background tasks, enabling recurring and delayed jobs.

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Redis
- API keys for any integrated services (e.g., Notion, Google Search).

## Example Usage

Here’s an example of a complex, multi-step task you can give Relay:

> **@Relay Tomorrow at 10 AM, find the latest news about generative AI, scrape the top 3 articles, summarize them, and create a new page in my Notion database with the summary.**

This single command will cause Relay to:

1.  Schedule a task for 10 AM the next day.
2.  At the scheduled time, it will search the web for "latest news about generative AI".
3.  It will then scrape the content of the top three articles found.
4.  The scraped content will be summarized.
5.  Finally, a new page will be created in Notion with the summarized articles.

This demonstrates the power of combining autonomous scheduling with a versatile toolset to create sophisticated automations.
