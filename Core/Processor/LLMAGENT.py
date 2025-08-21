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
        {"role": "system", "content": "You are a helpful assistant with access to various tools."},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=messages,
        tools=tools,
        parallel_tool_calls=True
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
            return f"Unknown tool requested: {function_name}"
    else:
        # If no tool was called, return the direct response
        return choice.content

def llmagent_process(message: str):
    """Process an input event using the LLM agent"""
    return chat(message)
