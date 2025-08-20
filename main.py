from mcp.server.fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os
import sys
import traceback

class WeatherRetrieval:
    def __init__(self):
        load_dotenv()
        self.mcp = FastMCP("WeatherServer")  # Changed from fastmcp to mcp
        self._register_tools()  # Call this in init
        
    def _setup_weather(self, query: str):
        access_key = os.getenv("WEATHERSTACK_API_KEY")
        self.url = f"http://api.weatherstack.com/current?access_key={access_key}&query={query}"
        
    def _register_tools(self): 
        @self.mcp.tool()    
        def get_weather(query: str):  # Removed self parameter
            self._setup_weather(query)
            response = requests.get(self.url)
            return response.json()
            
    def run(self):
        """Start the MCP server."""
        try:
            print("Running Weather MCP Server...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    server = WeatherRetrieval()
    server.run()