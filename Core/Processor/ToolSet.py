from mcp.server.fastmcp import FastMCP
import os
import json
import requests

# Create MCP server with AI integration
mcp = FastMCP("AI-Weather-API")

# WEATHER TOOLSET
@mcp.tool()
def get_weather(query: str) -> dict:
    """Get current weather for a location"""
    access_key = os.getenv("WEATHERSTACK_API_KEY")
    url = f"http://api.weatherstack.com/current?access_key={access_key}&query={query}"
    response = requests.get(url)
    return response.json()

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