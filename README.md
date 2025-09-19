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

Relay is an LLM-driven autonomous agent that makes real-time decisions to orchestrate complex, multi-step automations. Instead of following rigid workflows, Relay dynamically determines the best sequence of actions based on user requests and current context. It can queue tasks, trigger delayed actions, and run recurring workflows—adapting its approach as needed.

Relay’s architecture enables it to:

- Select and chain together the most appropriate tools for each situation, making decisions on the fly.
- Perform on-the-fly computation and automation by executing Python code using its integrated exec tool.
- Handle dynamic web research, content creation, and notifications, all while maintaining context for multiple users.

Its Redis-centric architecture manages user-bound memory, message queues, and state, enabling context-aware workflows for multiple concurrent users. The web scraping module is designed with resilience to dynamic HTML and bot detection, ensuring reliable data extraction.

## Key Features

- **Dynamic Decision-Making:** Relay analyzes each request and decides the optimal workflow, adapting to changing requirements and context.
- **Integrated Python Execution:** The agent can execute arbitrary Python code for computation, automation, or custom logic, using its built-in exec tool.
- **LLM-Driven Autonomous Scheduling:** Relay schedules and executes tasks dynamically, choosing the right time and method for each action.
- **Multi-Step Automation:** Chains together multiple tools to complete complex workflows, with each step chosen based on real-time analysis.
- **Resilient Web Scraping:** Uses Playwright to handle dynamic websites and anti-bot measures.
- **Redis-Centric Architecture:** Manages user memory, message queues, and workflow state.
- **Extensible Toolset:** Easily add new tools and capabilities.

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

Here’s an example of how Relay can dynamically solve a real-world problem:




> **@Relay: Monitor major tech news sites this week and send me a daily digest of the most important stories in Discord. If a breaking story emerges, alert me immediately.**

With this single command, Relay will:

1.  Monitor major technology news sources throughout the week.
2.  Summarize and send a daily digest of the most important stories to Discord.
3.  If a breaking story is detected, Relay will send an immediate alert.

Relay flexibly chooses which tools and actions to use, adapting to new information and user needs in real time.
