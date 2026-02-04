# VibeSync_Code V6.1 - Iron Memory Engine 🚀

VibeSync_Code is a professional-grade context orchestration layer for AI agents. It ensures absolute session continuity by centralizing project memory, architectural decisions, and agent identities.

## 🏗️ Core Architecture
The system operates on a triangular flow:
1.  **Local Workspace**: Source files managed via IDE (Cursor, Windsurf, VS Code).
2.  **Vibe-Orchestrator**: A Python 3.12 logic engine handling Sync-Points and local state.
3.  **Persistence Layer**: Centralized, scalable storage using **PostgreSQL + pgvector** (hosted on Supabase).

## 🛠️ Key Features
*   **Context Ledger**: A transaction registry for every agent action.
*   **Decision Graph**: The "Why" behind every code change, linked to the ledger.
*   **Agent Identity Model (AIM)**: Persistent profiles storing learned behaviors and design preferences.
*   **Skill Interoperability**: Native support for **Model Context Protocol (MCP)** to orchestrate specialized tools (Figma, GitHub, etc.).

## 📂 Project Structure
```text
/VibeSync_Code/
├── .sys/                   # System core (API, Logic, MCP)
├── vibes/                  # Isolated project environments
├── identities/             # Agent profiles (AIM)
├── vsc.sh                  # Bootstrap script (macOS/Linux)
└── vsc.ps1                 # Bootstrap script (Windows)
```

## 🚀 Getting Started
To initialize a new session:
```bash
./vsc.sh bootstrap
```

---
**Author**: Pascal Chui & MacBot Architect
**Status**: Active Engineering (Production-Ready)
