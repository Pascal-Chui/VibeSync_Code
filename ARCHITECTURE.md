# Technical Architecture - VibeSync_Code V6.1

This document outlines the internal logic, data flows, and persistence schemas of the VibeSync_Code system.

## 1. System Philosophy: The Triangular Context Flow
VibeSync_Code operates as an "invisible" state manager. It does not replace the developer's IDE but enhances it by ensuring that every agent turn is grounded in persistent memory.

1.  **Observability (Local)**: The system monitors file changes and agent intents in the local workspace.
2.  **Validation (Orchestrator)**: Actions are summarized and validated against the current `Vibe` constraints.
3.  **Persistence (Cloud)**: Validated actions are committed to PostgreSQL, creating a permanent audit trail.

## 2. Data Models (PostgreSQL Schema)

### 2.1 `context_ledger` (The Registry)
Every significant action taken by an agent (Codex, Gemini, Claude) is recorded here.
*   `id`: UUID (Primary Key)
*   `agent_id`: The identity of the performing agent.
*   `intent`: The goal of the action (e.g., "Refactor auth module").
*   `files_touched`: JSONB array of file paths.
*   `status`: pending | success | failed.

### 2.2 `decision_graph` (The Intelligence)
Records the reasoning behind structural changes.
*   `ledger_id`: Link to the action in the ledger.
*   `decision`: The technical choice made.
*   `rationale`: Why this choice was made (The "Because").
*   `embedding`: Vector(1536) for semantic retrieval.

### 2.3 `agent_identities` (The Aura)
Stores learned preferences to ensure stylistic consistency.
*   `design_preferences`: UI/UX standards (spacing, colors, typography).
*   `coding_style`: Syntax preferences, documentation standards.

## 3. Deployment & Scalability
*   **Infrastructure**: Hosted on Supabase (PostgreSQL) for industrial-grade reliability.
*   **Vector Search**: pgvector is utilized to allow agents to query past decisions using natural language.
*   **Cross-Platform**: Core logic is written in Python 3.12, ensuring compatibility across macOS, Windows, and Linux.

## 4. Model Context Protocol (MCP) Integration
VibeSync_Code acts as an MCP server. This allows it to:
*   Expose the `Context Ledger` directly to Cursor/Windsurf.
*   Provide a "Memory Tool" that agents can call to retrieve the history of a project or a specific decision.
