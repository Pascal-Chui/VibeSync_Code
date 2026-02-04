"""Test script for VibeSync_Code decision graph synchronization."""

import logging
import sys
import os

# Add .sys to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".sys")))

from core.ledger_sync import log_action, configure_logging
from core.decision_sync import log_decision

def run_test():
    configure_logging()
    logger = logging.getLogger("test_decision")
    
    print("🧪 Starting Decision Graph Sync Test...")
    
    try:
        # 1. Create a ledger entry first
        ledger_id = log_action(
            agent_id="macbot-tester",
            vibe_id="vibe-decision-test",
            intent="Testing decision graph linkage",
            files_touched=["core/decision_sync.py"],
            status="success"
        )
        print(f"✅ Ledger entry created: {ledger_id}")
        
        # 2. Link a decision to it
        decision_id = log_decision(
            ledger_id=ledger_id,
            decision="Adopt modular adapter-based architecture for V6.1 evolution.",
            rationale="Improves extensibility and isolates integrations without touching core.",
        )
        print(f"✅ Decision logged and linked: {decision_id}")
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_test()
