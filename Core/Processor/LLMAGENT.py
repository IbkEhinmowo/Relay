from Core.Processor.ToolSet import available_functions, tools
from dotenv import load_dotenv
import os
import json
import inspect
import requests
import redis

# Import Celery app for task registration
from Core.Integrations.Schedular import app
# Import Celery for task decorator (not strictly needed since we use app, but for clarity)
from celery import shared_task

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

import asyncio


def _openrouter_chat_completion(messages: list[dict]) -> dict:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Missing OPENROUTER_API_KEY environment variable")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "tools": tools,
        "parallel_tool_calls": True,
        "reasoning": {"enabled": True},
    }

    response = requests.post(
        url=OPENROUTER_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=90,
    )
    response.raise_for_status()
    return response.json()

async def chat(user_message: str) -> str:
    """Chat with AI that can use tools (async, non-blocking)"""
    import datetime
    today = datetime.date.today().strftime('%B %d, %Y')
    now = datetime.datetime.now().strftime('%H:%M:%S')
    messages = [
        {
            "role": "system",
            "content": (
                f"Today is {today}, {now}. "
                "You are Relay, an autonomous AI Agent with tool access. "
                "Memory: Only store explicit user info and key facts, in third person. No assumptions. "
                "Tools: Use the right tool for each request. Explain errors simply. "
                "Code: Use `execute_python_code` for computation or automation. Format code, errors, and output in Discord-style code blocks. If code is executed, show it in your reply. "
                "Tasks: Add clear details for cron/timer tasks. Write prompts for yourself to understand later. "
                "Communication: Keep replies under 2000 characters. Don't queue Discord replies for Discord inputs. Don't name tools, just say what you did."
            )
        },
        {"role": "user", "content": user_message}
    ]
    loop = asyncio.get_running_loop()
    while True:
        response = await loop.run_in_executor(
            None,
            lambda: _openrouter_chat_completion(messages)
        )
        choice = response["choices"][0]["message"]
        tool_calls = choice.get("tool_calls") or []

        if not tool_calls:
            return choice.get("content", "")

        assistant_message = {
            "role": "assistant",
            "content": choice.get("content"),
            "tool_calls": tool_calls,
        }
        if "reasoning_details" in choice:
            assistant_message["reasoning_details"] = choice.get("reasoning_details")
        messages.append(assistant_message)

        for call in tool_calls:
            function_name = call.get("function", {}).get("name")
            if function_name not in available_functions:
                return f"Unknown tool requested: {function_name}"
            
            function_to_call = available_functions[function_name]
            raw_arguments = call.get("function", {}).get("arguments") or "{}"
            try:
                arguments = json.loads(raw_arguments)
            except json.JSONDecodeError:
                arguments = {}
            
            if inspect.iscoroutinefunction(function_to_call):
                result = await function_to_call(**arguments)
            else:
                result = function_to_call(**arguments)
            
            print(f"Tool {function_name} called")

            # Log tool response to Redis
            try:
                result_str = str(result)
                if len(result_str) < 8000:  # Don't log very long results
                    r = redis.Redis(host='redis', port=6379, db=2)
                    log_entry = f"Tool Used: {function_name} || Result: {result_str}"
                    r.lpush("tool_responses_log", log_entry)
                    r.ltrim("tool_responses_log", 0, 3)  
                    r.expire("tool_responses_log", 1200)
            except Exception as e:
                print(f"Failed to log tool response to Redis: {e}")

            try:
                result_content = json.dumps(result)
            except TypeError:
                result_content = json.dumps(str(result))
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.get("id"),
                "content": result_content,
            })
            

# Make it a proper Celery task


async def llmagent_process(message: str):
    """Process an input event using the LLM agent (async)"""
    return await chat(message)

# Synchronous wrapper for Celery
@app.task(name="Core.Processor.LLMAGENT.llmagent_process")
def llmagent_process_task(message: str):
    """Celery task wrapper for llmagent_process async function."""
    import asyncio
    return asyncio.run(llmagent_process(message))
