"""
OSO Control Center Python SDK
Client for Amp or local interaction with the control center
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class OSOClient:
    """Client for interacting with OSO Control Center"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8888, api_prefix: str = "/api/v1"):
        self.base_url = f"http://{host}:{port}{api_prefix}"
        self.session = requests.Session()
    
    # ============ STATE ============
    def get_state(self) -> Dict[str, Any]:
        """Get entire control state"""
        resp = self.session.get(f"{self.base_url}/state")
        return resp.json()
    
    def update_state(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update control state"""
        resp = self.session.post(f"{self.base_url}/state", json=data)
        return resp.json()
    
    # ============ OPCODES ============
    def get_opcodes(self) -> Dict[int, Dict[str, Any]]:
        """Get all opcodes"""
        resp = self.session.get(f"{self.base_url}/opcodes")
        return resp.json()
    
    def add_opcode(self, code: int, name: str, description: str, 
                   category: str = "core", gas_cost: int = 1) -> Dict[str, Any]:
        """Add an opcode"""
        data = {
            "code": code,
            "name": name,
            "description": description,
            "category": category,
            "gas_cost": gas_cost
        }
        resp = self.session.post(f"{self.base_url}/opcodes", json=data)
        return resp.json()
    
    def get_opcode(self, code: int) -> Dict[str, Any]:
        """Get specific opcode"""
        resp = self.session.get(f"{self.base_url}/opcodes/{code}")
        return resp.json()
    
    # ============ LANGUAGE ============
    def get_language(self) -> Dict[str, Any]:
        """Get language spec"""
        resp = self.session.get(f"{self.base_url}/language")
        return resp.json()
    
    def update_language(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Update language spec"""
        resp = self.session.post(f"{self.base_url}/language", json=spec)
        return resp.json()
    
    def add_syntax_rule(self, rule_name: str, pattern: str, 
                       description: str, example: str) -> Dict[str, Any]:
        """Add syntax rule"""
        data = {
            "rule_name": rule_name,
            "pattern": pattern,
            "description": description,
            "example": example
        }
        resp = self.session.post(f"{self.base_url}/language/syntax-rule", json=data)
        return resp.json()
    
    # ============ VM ============
    def get_vm_config(self) -> Dict[str, Any]:
        """Get VM configuration"""
        resp = self.session.get(f"{self.base_url}/vm")
        return resp.json()
    
    def update_vm_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update VM config"""
        resp = self.session.post(f"{self.base_url}/vm", json=config)
        return resp.json()
    
    # ============ LAYER 1 ============
    def get_layer1_contracts(self) -> List[Dict[str, Any]]:
        """Get Layer 1 contracts"""
        resp = self.session.get(f"{self.base_url}/layer1")
        return resp.json()
    
    def add_layer1_contract(self, name: str, description: str, 
                           triggers: List[str], ase_reward: float) -> Dict[str, Any]:
        """Add Layer 1 contract"""
        data = {
            "name": name,
            "description": description,
            "triggers": triggers,
            "ase_reward": ase_reward
        }
        resp = self.session.post(f"{self.base_url}/layer1", json=data)
        return resp.json()
    
    # ============ LAYER 2 ============
    def get_layer2_config(self) -> Dict[str, Any]:
        """Get Layer 2 config"""
        resp = self.session.get(f"{self.base_url}/layer2")
        return resp.json()
    
    def update_layer2_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update Layer 2 config"""
        resp = self.session.post(f"{self.base_url}/layer2", json=config)
        return resp.json()
    
    # ============ FILES ============
    def list_all_files(self) -> Dict[str, Any]:
        """List all files by section"""
        resp = self.session.get(f"{self.base_url}/files")
        return resp.json()
    
    def list_section_files(self, section: str) -> Dict[str, Any]:
        """List files in a section"""
        resp = self.session.get(f"{self.base_url}/files/{section}")
        return resp.json()
    
    def upload_file(self, section: str, filepath: str) -> Dict[str, Any]:
        """Upload file to section"""
        with open(filepath, 'rb') as f:
            files = {'file': f}
            resp = self.session.post(
                f"{self.base_url}/files/upload?section={section}",
                files=files
            )
        return resp.json()
    
    # ============ GITHUB ============
    def get_repos(self) -> List[Dict[str, Any]]:
        """Get synced repositories"""
        resp = self.session.get(f"{self.base_url}/github/repos")
        return resp.json()
    
    def sync_repo(self, owner: str, name: str, url: str, 
                  local_path: str, branch: str = "main") -> Dict[str, Any]:
        """Sync a GitHub repository"""
        data = {
            "owner": owner,
            "name": name,
            "url": url,
            "local_path": local_path,
            "branch": branch
        }
        resp = self.session.post(f"{self.base_url}/github/sync", json=data)
        return resp.json()
    
    # ============ COPILOT ============
    def get_copilot_suggestion(self, section: str, query: str, 
                              context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get AI copilot suggestion"""
        data = {
            "section": section,
            "query": query,
            "context": context or {}
        }
        resp = self.session.post(f"{self.base_url}/copilot/suggest", json=data)
        return resp.json()
    
    # ============ EXECUTION ============
    def execute_bytecode(self, bytecode: str) -> Dict[str, Any]:
        """Execute bytecode"""
        data = {"bytecode": bytecode}
        resp = self.session.post(f"{self.base_url}/execute", json=data)
        return resp.json()
    
    # ============ EXPORT ============
    def export_json(self, output_path: str = "oso_state.json") -> str:
        """Export state as JSON"""
        resp = self.session.get(f"{self.base_url}/export/json")
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return output_path
    
    def export_markdown(self, output_path: str = "oso_state.md") -> str:
        """Export state as Markdown"""
        resp = self.session.get(f"{self.base_url}/export/markdown")
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return output_path


# ============ HELPER FUNCTIONS ============
def initialize_vm(client: OSOClient):
    """Initialize VM with 25 core opcodes"""
    opcodes = {
        0x00: ("HALT", "Stop execution"),
        0x01: ("NOOP", "No operation"),
        0x02: ("PUSH", "Push value to stack"),
        0x03: ("DUP", "Duplicate stack top"),
        0x04: ("SWAP", "Swap stack top 2 values"),
        0x05: ("VERIFY_SIG", "Verify signature"),
        0x06: ("TIMESTAMP", "Get current timestamp"),
        0x07: ("GEO_HASH", "Hash geolocation"),
        0x08: ("MERKLE_ROOT", "Get merkle root"),
        0x09: ("MINT_ASE", "Mint Àṣẹ token"),
        0x0A: ("BURN_ASE", "Burn Àṣẹ token"),
        0x0B: ("CALL_LAYER1", "Call Layer 1 contract"),
        0x0C: ("CALL_LAYER2", "Call Layer 2 oracle"),
        0x0D: ("ATTEST", "Create attestation"),
        0x0E: ("SIM_SCORE", "Score simulation"),
        0x0F: ("BRANCH_IF", "Conditional branch"),
        0x10: ("HASH256", "SHA256 hash"),
        0x11: ("ECDSA_VERIFY", "Verify ECDSA"),
        0x12: ("ADD", "Add stack values"),
        0x13: ("SUB", "Subtract"),
        0x14: ("MUL", "Multiply"),
        0x15: ("DIV", "Divide"),
        0x16: ("JUMP", "Jump to address"),
        0x17: ("STOP", "Stop execution"),
        0x18: ("EMIT_EVENT", "Emit event")
    }
    
    for code, (name, desc) in opcodes.items():
        client.add_opcode(code, name, desc, category="core")
    
    print(f"✓ Initialized {len(opcodes)} opcodes")


if __name__ == "__main__":
    # Test client
    client = OSOClient()
    print("🔥 OSO Client initialized")
    print(f"State: {client.get_state()}")
