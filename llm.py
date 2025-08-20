from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from cerebras.cloud.sdk import Cerebras

# Simple AI API that uses MCP tools directly
load_dotenv()

# Create MCP server with AI integration
mcp = FastMCP("AI-Weather-API")

client = Cerebras(
  api_key=os.environ.get("CEREBRAS_API_KEY"),
)

# Register your weather tool
@mcp.tool()
def get_weather(query: str) -> dict:
    """Get current weather for a location"""
    import requests
    access_key = os.getenv("WEATHERSTACK_API_KEY")
    url = f"http://api.weatherstack.com/current?access_key={access_key}&query={query}"
    response = requests.get(url)
    return response.json()

# Dictionary of available functions mapped by name
available_functions = {
    "get_weather": get_weather,
    # Add new tools here
}

# Define tool schema according to Cerebras requirements
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "strict": True,
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The location to get weather for (city name, zip code, etc)"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Simple chat function that uses the tools
def chat(user_message: str) -> str:
    """Chat with AI that can use weather tools"""
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to weather data."},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=messages,
        tools=tools,
        parallel_tool_calls=False
    )
    
    choice = response.choices[0].message
    
    # Check if the model wants to use a tool
    if choice.tool_calls:
        function_call = choice.tool_calls[0].function
        function_name = function_call.name
        
        if function_name in available_functions:
            # Parse the arguments and execute the tool
            arguments = json.loads(function_call.arguments)
            result = available_functions[function_name](**arguments)
            
            # Add the assistant's response with the tool call
            messages.append(choice.model_dump())
            
            # Add the tool response back to messages
            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": choice.tool_calls[0].id
            })
            
            # Get the final response from the model
            final_response = client.chat.completions.create(
                model="llama-4-scout-17b-16e-instruct",
                messages=messages,
            )
            
            return final_response.choices[0].message.content
        else:
            return "Unknown tool requested"
    else:
        # If no tool was called, return the direct response
        return choice.content

if __name__ == "__main__":
    # Simple test
    print(chat("What's the weather in lagos nigeria"))