import os
import json
import requests
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras


load_dotenv()

def getweather(longitude: float, latitude: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(url)
    data = response.json()
    return data['current']['temperature_2m'], data['current']['wind_speed_10m']  
    
# print(getweather(-122.4194, 37.7749))  # Example coordinates for San Francisco
    
client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)


    
tools = [
    {
        "type": "function",
        "function": {
            "name": "getweather",
            "strict": True,
            "description": "Get current weather conditions",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "number",
                        "description": "The longitude for the location."
                    },
                    "latitude": {
                        "type": "number",
                        "description": "The latitude for the location."
                    }
                },
                "required": ["longitude", "latitude"]
            },
        },
    }
]


messages = [
    {"role": "system", "content": "You are a helpful assistant with access to the weather. Use the weather to provide useful information."},
    {"role": "user", "content": "whats the weather like in lagos nigeria"},
]

response = client.chat.completions.create(
    model="llama3.3-70b",
    messages=messages,
    tools=tools,
    parallel_tool_calls=False,
)

choice = response.choices[0].message

if choice.tool_calls:
    function_call = choice.tool_calls[0].function
    if function_call.name == "getweather":
        # Logging that the model is executing a function named "getweather".
        print(f"Model executing function '{function_call.name}' with arguments {function_call.arguments}")

        # Parse the arguments from JSON format and perform the requested calculation.
        arguments = json.loads(function_call.arguments)
        result = getweather(arguments["longitude"], arguments["latitude"])

        # Note: This is the result of executing the model's request (the tool call), not the model's own output.
        print(f"weather sent to the rmodel: {result}")
       
       # Send the result back to the model to fulfill the request.
        messages.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": choice.tool_calls[0].id
        })
 
       # Request the final response from the model, now that it has the calculation result.
        final_response = client.chat.completions.create(
            model="llama3.3-70b",
            messages=messages,
        )
        
        # Handle and display the model's final response.
        if final_response:
            print("Final model output:", final_response.choices[0].message.content)
        else:
            print("No final response received")
else:
    # Handle cases where the model's response does not include expected tool calls.
    print("Unexpected response from the model")