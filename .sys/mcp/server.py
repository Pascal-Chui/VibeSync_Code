from mcp.server.fastmcp import FastMCP
import sys
import os

# Add .sys to python path to allow imports from core
current_dir = os.path.dirname(os.path.abspath(__file__))
sys_dir = os.path.abspath(os.path.join(current_dir, ".."))
if sys_dir not in sys.path:
    sys.path.append(sys_dir)

try:
    from core import ledger_sync, decision_sync
except ImportError as e:
    # Fallback for when running from root without .sys in path
    print(f"Import Warning: {e}. Ensure .sys is in PYTHONPATH.")

# Initialize MCP Server
mcp = FastMCP("VibeSync Core")

@mcp.tool()
def get_status():
    """Returns the current system status."""
    return "VibeSync Core is online. Logic modules loaded."

@mcp.tool()
def read_memory(query: str):
    """
    Search semantic memory for a query using Vector Search.
    Current implementation uses a placeholder embedding for demonstration.
    """
    try:
        # TODO: Replace with actual embedding generation (e.g., OpenAI text-embedding-3-small)
        # embedding = generate_embedding(query) 
        mock_embedding = [0.1] * 1536  # Placeholder vector
        
        client = ledger_sync.load_supabase_client()
        
        # Call Supabase RPC function 'match_decisions' (requires setup in SQL)
        # Falling back to basic text search if RPC not exists
        response = client.table("decision_graph").select("decision, rationale").textSearch("decision", query).execute()
        
        return f"Found {len(response.data)} matches for '{query}': {response.data}"
    except Exception as e:
        return f"Error reading memory: {str(e)}"

@mcp.tool()
def log_action(agent_id: str, vibe_id: str, intent: str, files: list[str] = [], status: str = "done") -> str:
    """
    Log an agent action to the Context Ledger.
    """
    try:
        action_id = ledger_sync.log_action(agent_id, vibe_id, intent, files, status)
        return f"Logged action: {action_id}"
    except Exception as e:
        return f"Error logging action: {str(e)}"

@mcp.tool()
def log_decision(decision: str, rationale: str, vibe_id: str = "default", agent_id: str = "macbot"):
    """
    Log a technical decision to the Decision Graph.
    Creates a parent ledger entry automatically.
    """
    try:
        # 1. Create Ledger Entry
        ledger_id = ledger_sync.log_action(
            agent_id=agent_id,
            vibe_id=vibe_id,
            intent=f"DECISION: {decision}",
            files_touched=[],
            status="decision"
        )
        
        # 2. Log Decision
        decision_id = decision_sync.log_decision(
            ledger_id=ledger_id,
            decision=decision,
            rationale=rationale
        )
        return f"Logged decision {decision_id} (linked to ledger {ledger_id})"
    except Exception as e:
        return f"Error logging decision: {str(e)}"

if __name__ == "__main__":
    mcp.run()
