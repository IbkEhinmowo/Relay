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

def chat(user_message: str) -> str:
    """Chat with AI that can use tools"""
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to tools. "
                "When the user asks for something that matches a tool description, "
                "you MUST call that tool using the tool calling mechanism, not by responding in text, otherwise state why not"
            )
        },
        {"role": "user", "content": user_message}
    ]
    while True:
        response = client.chat.completions.create(
            model="qwen-3-32b",
            messages=messages,
            tools=tools,
            parallel_tool_calls=True
        )
        choice = response.choices[0].message
        # If the assistant didn’t ask for a tool, we’re done
        if not choice.tool_calls:
            return choice.content
        # Save the assistant turn exactly as returned
        messages.append(choice.model_dump())
        # Run the requested tool(s)
        for call in choice.tool_calls:
            function_name = call.function.name
            if function_name not in available_functions:
                return f"Unknown tool requested: {function_name}"
            arguments = json.loads(call.function.arguments)
            result = available_functions[function_name](**arguments)
            # Feed the tool result back
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

def llmagent_process(message: str):
    """Process an input event using the LLM agent"""
    return chat(message)
