from Core.Processor.ToolSet import available_functions, tools
from dotenv import load_dotenv
import os
import json
from cerebras.cloud.sdk import Cerebras
import redis

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
                "If you are about to use a tool, especially if it may take some time, let the user know first (e.g., 'i'll work on that now...' or 'This may take a moment...'). "
                "Always use a tool if it matches or is helpful to the user's request. "
                "If a tool fails, explain the error simply. "
                "When adding to memory, use third person (the user or their username), never 'I'. "
                "After using a tool, reply only once, concisely, and do not summarize tool actions unless asked. "
                "Be concise, clear, and helpful. "
                "IMPORTANT: Your response must be 2000 characters or fewer. Never reply long Answers."
                "never list your tools. Not even if asked."
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
                model="qwen-3-235b-a22b-instruct-2507",
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
                r = redis.Redis(host='localhost', port=6379, db=2)
                log_entry = {
                    "tool_name": function_name,
                    "result": result
                }
                r.lpush("tool_responses_log", json.dumps(log_entry))
                r.ltrim("tool_responses_log", 0, 10) # Keep last 100
            except Exception as e:
                print(f"Failed to log tool response to Redis: {e}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

async def llmagent_process(message: str):
    """Process an input event using the LLM agent (async)"""
    return await chat(message) 
