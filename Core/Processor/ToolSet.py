import os
import json
import requests
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from Core.Integrations.Notion import NotionIntegration
from Core.Integrations.memory import Memory



# Initialize MCP server
mcp = FastMCP("Relay-Tools")
notion = NotionIntegration()

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



# Define tool schema according to Cerebras requirements
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "strict": False,
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
    },
    {
        "type": "function",
        "function": {
            "name": "update_notion_page",
            "strict": False,
            "description": "Update the content of a Notion page with the provided string",
            "parameters": {
                "type": "object",
                "properties": {
                    "written_string": {
                        "type": "string",
                        "description": "The new data for the Notion page"
                    }
                },
                "required": ["written_string"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_discord_message",
            "strict": False,
            "description": "Send a message to a Discord channel ",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send."
                    }
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "memory_add",
            "strict": False,
            "description": "Add a memory item for a user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID."},
                    "content": {"type": "string", "description": "The memory content to add."}
                },
                "required": ["user_id", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "memory_list",
            "strict": False,
            "description": "List all memory items for a user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID."}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "memory_delete",
            "strict": False,
            "description": "Delete a memory item for a user by index.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID."},
                    "index": {"type": "integer", "description": "The index of the memory item to delete."}
                },
                "required": ["user_id", "index"]
            }
        }
    }
    # Additional tools can be added here
]

# Register MCP tools
@mcp.tool()
def get_weather_tool(query: str) -> Dict[str, Any]:
    """Get current weather for a location"""
    return get_weather(query)

@mcp.tool()
def update_notion_page(written_string: str) -> str:
    """Update a Notion page with new data."""
    return notion.update_page(written_string)

# Memory tools
@mcp.tool()
def memory_add(user_id: str, content: str) -> str:
    mem = Memory(user_id)
    mem.add(content)
    return f"Added memory for user {user_id}."

@mcp.tool()
def memory_list(user_id: str):
    mem = Memory(user_id)
    return mem.list()

@mcp.tool()
def memory_delete(user_id: str, index: int) -> str:
    mem = Memory(user_id)
    mem.delete(index)
    return f"Deleted memory index {index} for user {user_id}."

def register_tools(mcp_instance) -> None:
    """Register available tools with a FastMCP instance.

    This keeps MCP specifics out of import-time side effects and allows reuse
    of the same functions by both LLM function-calling and MCP Server for Testing.
    """

@mcp.tool()
def send_discord_message_tool(message: str) -> str:
    """Send a message to a  Discord channel """
    try:
        import redis
        import json
        r = redis.Redis(host='localhost', port=6379, db=0)
        payload = {"content": message}
        r.lpush("discord_queue:default", json.dumps(payload))
        return "Message enqueued to discord_queue:default."
    except Exception as e:
        return f"Failed to enqueue message: {e}"
    
    
    
    
    
# Dictionary of available functions mapped by name for cerebras
available_functions = {
    "get_weather": get_weather,
    "update_notion_page": update_notion_page,
    "send_discord_message": send_discord_message_tool,
    # "DataBase_query": DataBase_query,
    # "Scrape_Description_Data": Scrape_Description_Data,
    # "Create_ticket": Create_ticket,
    # Add new tools here
    "memory_add": memory_add,
    "memory_list": memory_list,
    "memory_delete": memory_delete
}