"""Synchronize decisions with Supabase decision_graph."""

from __future__ import annotations

import logging
from typing import Sequence

from core.ledger_sync import load_supabase_client

LOGGER = logging.getLogger("decision_sync")


def log_decision_with_ledger(
    agent_id: str,
    vibe_id: str,
    intent: str,
    decision: str,
    rationale: str,
    files_touched: Sequence[str] | None = None,
    status: str = "decision",
    embedding: list[float] | None = None,
) -> dict[str, str]:
    """Insert ledger + decision in one RPC transaction.

    Expects a Supabase RPC function named ``log_decision_with_ledger`` that
    returns ``ledger_id`` and ``decision_id``.
    """
    client = load_supabase_client()

    payload = {
        "p_agent_id": agent_id,
        "p_vibe_id": vibe_id,
        "p_intent": intent,
        "p_files_touched": list(files_touched or []),
        "p_status": status,
        "p_decision": decision,
        "p_rationale": rationale,
        "p_embedding": embedding,
    }

    try:
        response = client.rpc("log_decision_with_ledger", payload).execute()
    except Exception as exc:
        LOGGER.exception("Supabase RPC log_decision_with_ledger failed.")
        raise RuntimeError("Supabase RPC log_decision_with_ledger failed.") from exc

    if not response.data:
        raise RuntimeError("Supabase RPC log_decision_with_ledger returned no data.")

    row = response.data[0] if isinstance(response.data, list) else response.data
    ledger_id = row.get("ledger_id")
    decision_id = row.get("decision_id")

    if not ledger_id or not decision_id:
        raise RuntimeError("Supabase RPC log_decision_with_ledger missing ids.")

    return {"ledger_id": str(ledger_id), "decision_id": str(decision_id)}

def log_decision(
    ledger_id: str,
    decision: str,
    rationale: str,
    embedding: list[float] | None = None
) -> str:
    """Insert a decision row into the Supabase decision_graph table.

    Args:
        ledger_id: UUID of the related ledger entry.
        decision: The technical choice made.
        rationale: Why this choice was made.
        embedding: Optional vector embedding (VECTOR(1536)).

    Returns:
        The UUID string of the inserted decision row.
    """
    client = load_supabase_client()

    payload = {
        "ledger_id": ledger_id,
        "decision": decision,
        "rationale": rationale,
    }

    if embedding:
        payload["embedding"] = embedding

    try:
        response = client.table("decision_graph").insert(payload).execute()
    except Exception as exc:
        LOGGER.exception("Supabase decision insert failed.")
        raise RuntimeError("Supabase decision insert failed.") from exc

    if not response.data:
        raise RuntimeError("Supabase decision insert returned no data.")

    return str(response.data[0]["id"])

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    LOGGER.info("Decision sync module ready.")

if __name__ == "__main__":
    main()
