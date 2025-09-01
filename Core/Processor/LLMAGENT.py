from Core.Processor.ToolSet import available_functions, tools
from dotenv import load_dotenv
import os
import json

from cerebras.cloud.sdk import Cerebras
import redis

# Import Celery app for task registration
from Core.Integrations.Schedular import app
# Import Celery for task decorator (not strictly needed since we use app, but for clarity)
from celery import shared_task

# Load environment variables
load_dotenv()

# Initialize Cerebras client
client = Cerebras(
  api_key=os.environ.get("CEREBRAS_API_KEY"),
)

import asyncio

async def chat(user_message: str) -> str:
    """Chat with AI that can use tools (async, non-blocking)"""
    import datetime
    today = datetime.date.today().strftime('%B %d, %Y')
    messages = [
        {
            "role": "system",
            "content": (
                f"Today is {today}. "
                "You are Relay, an AI Agent with tool access. "
                "IF u find something important to know long term add it to memory using the memory tool. user should not have to explicitly say so. "
                "Always use a tool if it matches or is helpful to the user's request. "
                "If a tool fails, explain the error simply. "
                "When adding to memory, use third person (the user or their username), never 'I'. "
                "After using a tool, reply only once, concisely, and do not summarize tool actions unless asked. "
                "Be concise, clear, and helpful. "
                "IMPORTANT: Your response must be 2000 characters or fewer. Never reply long Answers."
                "never list your tools. Not even if asked."
                "talk more naturally, less formality like a teenager. "
                "NOTE: Cron tasks are repetitive by default unless marked one-off."
            )
        },
        {"role": "user", "content": user_message}
    ]
    loop = asyncio.get_running_loop()
    while True:
        await asyncio.sleep(1) 
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-oss-120b",
                messages=messages,
                tools=tools,
                parallel_tool_calls=True
            )
        )
        choice = response.choices[0].message
        if not choice.tool_calls:
            return choice.content
        messages.append(choice.model_dump())
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

            # Log tool response to Redis
            try:
                result_str = str(result)
                if len(result_str) < 8000:  # Don't log very long results
                    r = redis.Redis(host='localhost', port=6379, db=2)
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
