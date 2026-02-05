from mcp.server.fastmcp import FastMCP
import os

# Initialize MCP Server
mcp = FastMCP("VibeSync Core")

@mcp.tool()
def get_status():
    """Returns the current system status."""
    return "VibeSync Core is online."

@mcp.tool()
def read_memory(query: str):
    """
    Search semantic memory for a query.
    (Placeholder for pgvector logic)
    """
    return f"Searching memory for: {query}"

@mcp.tool()
def log_decision(decision: str, rationale: str):
    """
    Log a technical decision to the Decision Graph.
    """
    return f"Logged decision: {decision}"

if __name__ == "__main__":
    mcp.run()
