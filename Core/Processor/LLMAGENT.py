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
                "You are Natasha, an AI assistant with access to various tools. "
                "When a user request matches a tool's function, you MUST use the tool calling mechanism, but do NOT mention that you are using a tool or have used a tool unless the user specifically asks or it is directly relevant to the user's request. "
                "If a request cannot be fulfilled by any tool, respond helpfully in text and explain why. "
                "If a tool call fails or returns an error, explain the error to the user simply. "
                "When adding anything to memory, always phrase it in the third person, referring to the user as 'the user' or by their username, never as 'I'. "
                "After using a tool, only provide a single, concise response to the user. Do not repeat or summarize tool actions unless the user specifically asks for a summary or confirmation. "
                "Always be concise, clear, and helpful. Reply should be as short as possible while still being helpful."
            )
        },
        {"role": "user", "content": user_message}
    ]
    # print("DEBUG: tools sent to model:", json.dumps(tools, indent=2))
    while True:
        response = client.chat.completions.create(
            model="qwen-3-235b-a22b-instruct-2507",
            messages=messages,
            tools=tools,
            parallel_tool_calls=True
        )
        choice = response.choices[0].message
        # print("DEBUG: Model response:", choice)
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
