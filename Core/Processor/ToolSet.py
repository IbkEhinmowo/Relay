from Core.Integrations.websearch import Web
import os
import json
import requests
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from Core.Integrations.Notion import NotionIntegration
from Core.Integrations.memory import Memory
from Core.Integrations.scraper import scrape



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



# Define tool schema according to Cerebras requirements
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search_result",
            "strict": False,
            "description": "Performs a web search and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_news_result",
            "strict": False,
            "description": "Performs a news search and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The news search query."}
                },
                "required": ["query"]
            }
        }
    },
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
            "name": "create_notion_subpage",
            "strict": False,
            "description": "Create a new subpage in Notion with a heading and body",
            "parameters": {
                "type": "object",
                "properties": {
                    "heading": {
                        "type": "string",
                        "description": "The heading/title for the new subpage"
                    },
                    "body": {
                        "type": "string",
                        "description": "The content for the new subpage"
                    }
                },
                "required": ["heading", "body"]
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
            "description": "Add something memorable about a user.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "memory_changing",
            "strict": False,
            "description": "make changes to a memory item for a user by its index.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID."},
                    "index": {"type": "integer", "description": "The index of the memory item to make changes to."},
                    "new_content": {"type": "string", "description": "The new content for the memory item."}
                },
                "required": ["user_id", "index", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_url",
            "strict": False,
            "description": "Scrape a URL and return the text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of URLs to scrape, or just one url"
                    }
                },
                "required": ["urls"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_notion_page",
            "strict": False,
            "description": "Read a Notion page's properties and content blocks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "The ID of the page to read."
                    }
                },
                "required": ["page_id"]
            }
        }
    }
]
# Register MCP tools

@mcp.tool()
def memory_changing(user_id: str, index: int, new_content: str) -> str:
    """Change a memory item for a user by index."""
    mem = Memory(user_id)
    mem.changing(index, new_content)
    return f"Changed memory index {index} for user {user_id} to {new_content}."
    # Additional tools can be added here
    
# Register MCP tools
@mcp.tool()
def get_weather_tool(query: str) -> Dict[str, Any]:
    """Get current weather for a location"""
    return get_weather(query)


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
def send_discord_message_tool(message: str, from_discord: bool = False) -> str:
    """Send a message to a Discord channel, but ignore if called from Discord context."""
    if from_discord:
        return "Ignored: Already in Discord context."
    try:
        import redis
        import json
        r = redis.Redis(host='redis', port=6379, db=0)
        payload = {"content": message}
        r.lpush("discord_queue:default", json.dumps(payload))
        return "Message enqueued to discord_queue:default."
    except Exception as e:
        return f"Failed to enqueue message: {e}"


@mcp.tool()
def web_search_result(query: str):
    """Perform a Brave web search and return the result."""
    return Web().search_result(query)


@mcp.tool()
def web_news_result(query: str):
    """Perform a Brave news search and return the result."""
    return Web().news_result(query)
    
@mcp.tool()
async def scrape_url(urls: list[str]) -> list[str]:
    """Scrape a URL and return the text content."""
    return await scrape(urls)
    
# Adding Notion integration tools
@mcp.tool()
def create_notion_subpage(heading: str, body: str) -> str:
    """Create a new subpage in Notion with a heading and body."""
    load_dotenv()
    # Create a new instance to ensure we have the latest token
    return notion.create_subpage(heading, body)

@mcp.tool()
def read_notion_page(page_id: str):
    """Read a Notion page's properties and content blocks."""
    return notion.read_page(page_id)

# Dictionary of available functions mapped by name for cerebras
available_functions = {
    "get_weather": get_weather,
    "create_notion_subpage": create_notion_subpage,
    "send_discord_message": send_discord_message_tool,
    "memory_add": memory_add,
    "memory_list": memory_list,
    "memory_delete": memory_delete,
    "memory_changing": memory_changing,
    "web_search_result": web_search_result,
    "web_news_result": web_news_result,
    "scrape_url": scrape_url,
    "read_notion_page": read_notion_page
}