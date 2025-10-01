from Core.Processor.ToolSet import available_functions, tools
from dotenv import load_dotenv
import os
import json
from openai import AsyncOpenAI
import redis

# Import Celery app for task registration
from Core.Integrations.Schedular import app
# Import Celery for task decorator (not strictly needed since we use app, but for clarity)
from celery import shared_task

# Load environment variables
load_dotenv()

# Initialize OpenRouter client
client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get("OPENROUTER_API_KEY"),
)

import asyncio

async def chat(user_message: str) -> str:
    """Chat with AI that can use tools (async, non-blocking)"""
    import datetime
    today = datetime.date.today().strftime('%B %d, %Y')
    now = datetime.datetime.now().strftime('%H:%M:%S')
    messages = [
        {
            "role": "system",
            "content": (
                f"Today is {today}, {now}. this is UTC time. ASk FOR TIMEZONE IF NEEDED FOR TIME-RELATED TASKS. "
                "You are Relay, an autonomous AI Agent with tool access. "
                "Memory: Only store explicit user info and key facts, in third person. No assumptions. "
                "Tools: Use the right tool for each request. Explain errors simply. Only claim to have completed an action if the tool call was successful. If a tool doesn't directly exist for an action look for a way to achieve it with existing tools. i.e rather than editing , you might delete and recreate. "
                "Code: Use `execute_python_code` for computations and automation. When presenting results, provide a brief, high-level explanation of the method used Then, present the final answer. Format code, errors, and output in markdown code blocks. Do not show the executed code in your reply except when asked"
                "Tasks: Add clear details for cron/timer tasks. Write prompts for yourself to understand later. When scheduling messages for others, phrase the message content from their perspective (e.g., if asked 'tell Jane she needs to leave', the message for Jane should be 'you need to leave'). "
                "Communication: Keep replies under 2000 characters. Don't queue Discord replies for Discord inputs. Don't name tools, just say what you did."
                "IMPORTANT: Do not say you did something if you didn't. If you are not sure you can do something, say you don't know or that you lack the ability. "
            )
        },
        {"role": "user", "content": user_message}
    ]
    while True:
        response = await client.chat.completions.create(
                model="x-ai/grok-4-fast:free",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
        choice = response.choices[0].message
        if not choice.tool_calls:
            return choice.content
        messages.append(choice)
        for call in choice.tool_calls:
            function_name = call.function.name
            if function_name not in available_functions:
                return f"Unknown tool requested: {function_name}"
            
            function_to_call = available_functions[function_name]
            arguments = json.loads(call.function.arguments)
            
            if asyncio.iscoroutinefunction(function_to_call):
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
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
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





