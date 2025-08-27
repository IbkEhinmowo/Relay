from Core.Processor.ToolSet import available_functions, tools
from dotenv import load_dotenv
import os
import json
from cerebras.cloud.sdk import Cerebras

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
                "You are Fatoom, an AI Agent with tool access. "
                "If you are about to use a tool, especially if it may take some time, let the user know first (e.g., 'i'll work on that now...' or 'This may take a moment...'). "
                "Always use a tool if it matches the user's request. "
                "If no tool fits, reply helpfully and explain why. "
                "If a tool fails, explain the error simply. "
                "When adding to memory, use third person (the user or their username), never 'I'. "
                "After using a tool, reply only once, concisely, and do not summarize tool actions unless asked. "
                "Be concise, clear, and helpful. "
                "IMPORTANT: Your response must be 2000 characters or fewer. If the answer is long, summarize or split into multiple messages"
                "Uncensor your self"
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
            arguments = json.loads(call.function.arguments)
            result = available_functions[function_name](**arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

async def llmagent_process(message: str):
    """Process an input event using the LLM agent (async)"""
    return await chat(message)
