
import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv



# WEATHER TOOLSET

def get_weather(query: str) -> Dict[str, Any]:
    """Get current weather for a location."""
    # Ensure env is loaded for both CLI and server use
    load_dotenv()
    access_key = os.getenv("WEATHERSTACK_API_KEY")
    if not access_key:
        return {"error": "Missing WEATHERSTACK_API_KEY env var"}

    url = f"http://api.weatherstack.com/current?access_key={access_key}&query={query}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        # Weatherstack sometimes returns success:false inside 200 responses
        if isinstance(data, dict) and data.get("success") is False and data.get("error"):
            return {"error": data.get("error")}
        return data
    except requests.RequestException as e:
        return {"error": f"request_failed: {str(e)}"}

# # DISCORD TOOLSET
# def DataBase_query(name: str, pricebought: str, priceSold: str, profit:str ):
#     return "Query Result"  # Replace with actual result from database

# # MARKETPLACE TOOLSET
# def Scrape_Description_Data(url: str):
#     return "Scraped Data"  # Replace with actual scraped data

# # EMAIL TOOLSET
# def Create_ticket(subject: str, description: str, priority: str):
#     return "Ticket Created"  # Replace with actual ticket creation logic

# Dictionary of available functions mapped by name
available_functions = {
    "get_weather": get_weather,
    # "DataBase_query": DataBase_query,
    # "Scrape_Description_Data": Scrape_Description_Data,
    # "Create_ticket": Create_ticket,
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
    # Additional tools can be added here
]


def register_tools(mcp) -> None:
    """Register available tools with a FastMCP instance.

    This keeps MCP specifics out of import-time side effects and allows reuse
    of the same functions by both LLM function-calling and MCP.
    """

    @mcp.tool()
    def get_weather_tool(query: str) -> Dict[str, Any]:
        """Get current weather for a location"""
        return get_weather(query)