import os
import json
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not set")
    exit(1)

supabase: Client = create_client(url, key)

# AIM Data (Seed)
aim_data = {
    "agent_id": "macbot-core",
    "design_preferences": {
        "theme": "dark",
        "primary_color": "#00ff00",
        "font": "JetBrains Mono",
        "ux_tone": "minimalist, functional, console-like"
    },
    "coding_style": {
        "language": "python",
        "formatting": "black",
        "comments": "concise",
        "paradigm": "functional-core, imperative-shell"
    }
}

try:
    response = supabase.table("agent_identities").insert(aim_data).execute()
    print("AIM Seed Success:", response.data)
except Exception as e:
    print("AIM Seed Error:", e)
