#!/usr/bin/env python3
"""Test OSO SDK connection"""

import sys
sys.path.insert(0, './sdk')

from oso_client import OSOClient, initialize_vm
import subprocess
import time
import signal

def test_sdk():
    # Start server
    print("🚀 Starting API server...")
    proc = subprocess.Popen(
        ["python", "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3)
    
    try:
        # Connect
        print("🔌 Connecting to API...")
        client = OSOClient()
        
        # Get state
        state = client.get_state()
        print(f"✅ Connected! State keys: {list(state.keys())}")
        
        # Initialize opcodes
        print("⚙️ Initializing VM opcodes...")
        initialize_vm(client)
        
        # Verify
        opcodes = client.get_opcodes()
        print(f"✅ VM initialized: {len(opcodes)} opcodes")
        
        # Add Layer 1 contract
        print("📝 Adding Layer 1 contract...")
        result = client.add_layer1_contract(
            name="witness_delivery",
            description="Track package arrival",
            triggers=["package_arrived"],
            ase_reward=0.5
        )
        print(f"✅ Contract added: {result}")
        
        # Export
        print("💾 Exporting state...")
        path = client.export_json()
        print(f"✅ Exported to: {path}")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        proc.kill()
        proc.wait()

if __name__ == "__main__":
    test_sdk()
