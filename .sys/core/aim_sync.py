"""Synchronize Agent Identity Model (AIM) with Supabase."""

from __future__ import annotations

import logging
from typing import Any

from core.ledger_sync import load_supabase_client

LOGGER = logging.getLogger("aim_sync")


def get_agent_identity(agent_id: str) -> dict[str, Any] | None:
    """Fetch agent identity preferences from Supabase.

    Args:
        agent_id: The unique identifier for the agent (e.g., 'macbot-core').

    Returns:
        A dictionary containing the agent's identity data (design_preferences,
        coding_style, etc.) or None if not found.
    """
    client = load_supabase_client()

    try:
        response = (
            client.table("agent_identities")
            .select("*")
            .eq("agent_id", agent_id)
            .execute()
        )
    except Exception as exc:
        LOGGER.exception("Failed to fetch agent identity for %s", agent_id)
        return None

    if not response.data:
        LOGGER.warning("No identity found for agent: %s", agent_id)
        return None

    return response.data[0]


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    # Simple test
    identity = get_agent_identity("macbot-core")
    if identity:
        LOGGER.info("Fetched Identity: %s", identity)
    else:
        LOGGER.warning("Identity not found.")


if __name__ == "__main__":
    main()
