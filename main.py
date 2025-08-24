from mcp.server.fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os




####THIS IS A TEST PRACTICE FILE FOR WEATHER RETRIEVAL USING MCP SERVER....IGNORE THIS FILE 
class WeatherRetrieval:
    def __init__(self):
        load_dotenv()
        self.fastmcp = FastMCP("WeatherServer")
        
    def _setup_weather(self, query: str):
        access_key = os.getenv("WEATHERSTACK_API_KEY")
        self.url = f"http://api.weatherstack.com/current?access_key={access_key}&query={query}"
        
        
        def registertools(self):
            @self.mcp.tool()    
            def get_weather(self, query: str):
                self._setup_weather(query)
                response = requests.get(self.url)
                return response.json()
        def run(self):
            """Start the MCP server."""
            try:
                print("Running MCP Server for GitHub PR Analysis...", file=sys.stderr)
                self.mcp.run(transport="stdio")
            except Exception as e:
                print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                sys.exit(1)
