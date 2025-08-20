from mcp.server.fastmcp import FastMCP
from Core.Processor.ToolSet import register_tools
import sys

# Expose a top-level FastMCP instance so `mcp dev mainone.py` can import it
mcp = FastMCP("Relay-Tools")
register_tools(mcp)


def main():
    """Run the MCP development server and expose tools from ToolSet."""
    # Start server (stdio transport by default)
    print("Running Relay MCP Server (stdio)...", file=sys.stderr)
    mcp.run()

if __name__ == "__main__":
    main()
