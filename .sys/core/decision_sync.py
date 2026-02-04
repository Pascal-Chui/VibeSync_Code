"""Synchronize decisions with Supabase decision_graph."""

from __future__ import annotations

import logging
import os
from typing import Any

from dotenv import load_dotenv
from supabase import Client, create_client
from core.ledger_sync import load_supabase_client

LOGGER = logging.getLogger("decision_sync")

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
