"""Synchronize local actions with Supabase context ledger."""

from __future__ import annotations

import logging
import os
from typing import Iterable, Sequence

from dotenv import load_dotenv
from supabase import Client, create_client

LOGGER = logging.getLogger("ledger_sync")


class SupabaseConfigError(RuntimeError):
    """Raised when Supabase configuration is missing or invalid."""


def load_supabase_client() -> Client:
    """Load Supabase client using environment variables defined in .env."""
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        raise SupabaseConfigError(
            "Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment."
        )

    return create_client(url, key)


def _normalize_files(files_touched: Sequence[str] | None) -> list[str]:
    if not files_touched:
        return []
    return [file for file in files_touched if file]


def log_action(
    agent_id: str,
    vibe_id: str,
    intent: str,
    files_touched: Sequence[str] | None,
    status: str,
) -> str:
    """Insert an action row into the Supabase context_ledger table.

    Args:
        agent_id: Identifier for the agent performing the action.
        vibe_id: Identifier for the vibe or session.
        intent: Description of the action's intent.
        files_touched: Iterable of file paths touched.
        status: Status string for the action.

    Returns:
        The UUID string of the inserted action row.

    Raises:
        SupabaseConfigError: If required configuration is missing.
        RuntimeError: If the insert fails.
    """
    client = load_supabase_client()

    payload = {
        "agent_id": agent_id,
        "vibe_id": vibe_id,
        "intent": intent,
        "files_touched": _normalize_files(files_touched),
        "status": status,
    }

    try:
        response = client.table("context_ledger").insert(payload).execute()
    except Exception as exc: # noqa: BLE001
        LOGGER.exception("Supabase insert failed.")
        raise RuntimeError("Supabase insert failed.") from exc

    if not response.data:
        raise RuntimeError("Supabase insert returned no data.")

    inserted = response.data[0]
    action_id = inserted.get("id")
    if not action_id:
        raise RuntimeError("Supabase insert returned no id.")

    return str(action_id)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def main() -> None:
    configure_logging()
    try:
        client = load_supabase_client()
    except SupabaseConfigError as exc:
        LOGGER.error("Supabase configuration error: %s", exc)
        raise SystemExit(1) from exc
    except Exception as exc: # noqa: BLE001
        LOGGER.exception("Failed to initialize Supabase client.")
        raise SystemExit(1) from exc

    LOGGER.info("Supabase client initialized for URL: %s", client.supabase_url)


if __name__ == "__main__":
    main()
