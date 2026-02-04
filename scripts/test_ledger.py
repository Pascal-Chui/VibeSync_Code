"""Simple test script for VibeSync_Code ledger synchronization."""

import logging
import sys
import os

# Add .sys to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".sys")))

from core.ledger_sync import log_action, configure_logging

def run_test():
    configure_logging()
    logger = logging.getLogger("test_ledger")
    
    print("🧪 Starting Ledger Sync Test...")
    
    try:
        action_id = log_action(
            agent_id="macbot-tester",
            vibe_id="vibe-test-001",
            intent="Verification of production-ready schema",
            files_touched=["README.md", "ARCHITECTURE.md"],
            status="success"
        )
        print(f"✅ Success! Action logged with ID: {action_id}")
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    run_test()
