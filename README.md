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
│   ├── core/               # Python logic (ledger_sync.py, decision_sync.py)
│   └── supabase/           # SQL schemas & RLS policies
├── scripts/                # Utility scripts (tests, seeds)
├── vibes/                  # Isolated project environments
├── identities/             # Agent profiles (AIM)
├── vsc.sh                  # Bootstrap script (macOS/Linux)
└── vsc.ps1                 # Bootstrap script (Windows)
```

## 🚀 Getting Started

### 1. Environment Setup
Create a `.env` file in `VibeSync_Code/` (do not commit it):
```ini
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
```

### 2. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install supabase
```

### 3. Database Security (RLS)
Apply policies via Supabase SQL Editor:
1. Open [Supabase Dashboard](https://supabase.com/dashboard).
2. Go to **SQL Editor** -> **New Query**.
3. Paste content from `.sys/supabase/policies.sql`.
4. Run to enable Row Level Security (Service Role = Full Access; Anon = Deny).

### 4. Running Tests
```bash
# Test Ledger Insert
python3 scripts/test_ledger.py

# Test Decision Tracking
python3 scripts/test_decision.py
```

### 5. Seeding Data (AIM)
Initialize the agent identity profile:
```bash
python3 scripts/seed_aim.py
```

---
**Author**: Pascal Chui & MacBot Architect
**Status**: Active Engineering (Production-Ready)
