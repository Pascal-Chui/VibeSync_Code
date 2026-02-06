from mcp.server.fastmcp import FastMCP
import os
import sys

from openai import OpenAI

# Add .sys to python path to allow imports from core
current_dir = os.path.dirname(os.path.abspath(__file__))
sys_dir = os.path.abspath(os.path.join(current_dir, ".."))
if sys_dir not in sys.path:
    sys.path.append(sys_dir)

try:
    from core import decision_sync, ledger_sync
except ImportError as e:
    # Fallback for when running from root without .sys in path
    print(f"Import Warning: {e}. Ensure .sys is in PYTHONPATH.")

# Initialize MCP Server
mcp = FastMCP("VibeSync Core")


def _generate_embedding(query: str) -> list[float]:
    """Generate OpenAI embedding for semantic memory search."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment.")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model="text-embedding-3-small", input=query)
    return response.data[0].embedding


@mcp.tool()
def get_status():
    """Returns the current system status."""
    return "VibeSync Core is online. Logic modules loaded."


@mcp.tool()
def read_memory(query: str, match_count: int = 5):
    """Search semantic memory via OpenAI embeddings + Supabase RPC match_decisions."""
    try:
        embedding = _generate_embedding(query)
        client = ledger_sync.load_supabase_client()
        response = client.rpc(
            "match_decisions",
            {
                "query_embedding": embedding,
                "match_count": match_count,
            },
        ).execute()

        data = response.data or []
        return {
            "query": query,
            "match_count": len(data),
            "results": data,
        }
    except Exception as e:  # noqa: BLE001
        return f"Error reading memory: {str(e)}"


@mcp.tool()
def log_action(
    agent_id: str,
    vibe_id: str,
    intent: str,
    files: list[str] | None = None,
    status: str = "done",
) -> str:
    """Log an agent action to the Context Ledger."""
    try:
        action_id = ledger_sync.log_action(agent_id, vibe_id, intent, files or [], status)
        return f"Logged action: {action_id}"
    except Exception as e:  # noqa: BLE001
        return f"Error logging action: {str(e)}"


@mcp.tool()
def log_decision(
    decision: str,
    rationale: str,
    vibe_id: str = "default",
    agent_id: str = "macbot",
):
    """Log a technical decision with optimized transaction between ledger and decision graph."""
    embedding = None
    try:
        embedding = _generate_embedding(f"{decision}\n{rationale}")
        result = decision_sync.log_decision_with_ledger(
            agent_id=agent_id,
            vibe_id=vibe_id,
            intent=f"DECISION: {decision}",
            decision=decision,
            rationale=rationale,
            files_touched=[],
            status="decision",
            embedding=embedding,
        )
        return (
            "Logged decision "
            f"{result['decision_id']} (linked to ledger {result['ledger_id']}) via atomic RPC"
        )
    except Exception:  # noqa: BLE001
        try:
            ledger_id = ledger_sync.log_action(
                agent_id=agent_id,
                vibe_id=vibe_id,
                intent=f"DECISION: {decision}",
                files_touched=[],
                status="decision",
            )
            decision_id = decision_sync.log_decision(
                ledger_id=ledger_id,
                decision=decision,
                rationale=rationale,
                embedding=embedding,
            )
            return (
                "Logged decision "
                f"{decision_id} (linked to ledger {ledger_id}) via fallback non-atomic flow"
            )
        except Exception as e:  # noqa: BLE001
            return f"Error logging decision: {str(e)}"


if __name__ == "__main__":
    mcp.run()
