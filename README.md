![Version](https://img.shields.io/badge/version-v1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Layer](https://img.shields.io/badge/layer-Coordination-purple)
# Ọ̀ṢỌ́VM v7 — ÀṣẹVault Control Center

**Biblical Command Center for the Sacred Virtual Machine**

A unified, dictionary-driven dashboard for building, managing, and interacting with the entire OSO ecosystem (Techgnosis language, ÀṣẹVault VM, Layer 1 witnessing, Layer 2 simulation).

## Architecture

```
oso-control-center/
├── backend/
│   ├── app.py              # FastAPI server
│   ├── models.py           # Pydantic data models
│   └── requirements.txt     # Dependencies
├── sdk/
│   └── oso_client.py       # Python SDK for programmatic access
├── dashboard/
│   └── index.html          # Web UI for managing project
├── db/                     # Persistent file storage
├── config.json             # Project configuration
└── oso_state.json          # Master control state
```

## Features

### 🔧 Sections
- **LANGUAGE** - Techgnosis compiler, syntax, parser
- **VM** - Core VM (25 opcodes), bytecode execution
- **OPCODES** - Complete instruction set reference
- **LAYER 1** - Real-world witnessing contracts, signatures
- **LAYER 2** - VeilSim oracle, F1 scoring, Àṣẹ minting
- **DOCS** - Sacred Bible and full documentation

### 📁 File Management
- Upload/organize files by section
- Automatic indexing and persistence
- Export to JSON or Markdown

### 🐙 GitHub Integration
- Sync repositories (clone, pull, push)
- Manage remotes
- Track sync status

### ✨ AI Copilot
- Context-aware suggestions
- Code snippets
- Architecture recommendations

### 🔐 ACL & Access
- Role-based access control
- SDK authentication
- Admin/user modes

## Quick Start

### 1. Install Dependencies

```bash
cd oso-control-center/backend
pip install -r requirements.txt
```

### 2. Start API Server

```bash
python app.py
```

Server runs on `http://127.0.0.1:8888/api/v1`

### 3. Open Dashboard

Open `dashboard/index.html` in your browser (or serve with `python -m http.server`)

### 4. Use Python SDK

```python
from sdk.oso_client import OSOClient, initialize_vm

# Connect to API
client = OSOClient(host="127.0.0.1", port=8888)

# Initialize 25 opcodes
initialize_vm(client)

# Add a contract
client.add_layer1_contract(
    name="witness_delivery",
    description="Track package arrival",
    triggers=["package_arrived"],
    ase_reward=0.5
)

# Get entire state
state = client.get_state()
print(state)

# Export
client.export_json("my_export.json")
```

## API Endpoints

### Core
- `GET /state` - Get entire control state
- `POST /state` - Update control state

### Opcodes
- `GET /opcodes` - List all opcodes
- `POST /opcodes` - Add opcode
- `GET /opcodes/{code}` - Get specific opcode

### Language
- `GET /language` - Get language spec
- `POST /language` - Update spec
- `POST /language/syntax-rule` - Add syntax rule

### VM
- `GET /vm` - Get VM config
- `POST /vm` - Update VM config

### Layer 1
- `GET /layer1` - Get contracts
- `POST /layer1` - Add contract

### Layer 2
- `GET /layer2` - Get config
- `POST /layer2` - Update config

### Files
- `POST /files/upload?section=SECTION` - Upload file
- `GET /files` - List all files
- `GET /files/{section}` - List section files

### GitHub
- `GET /github/repos` - Get synced repos
- `POST /github/sync` - Sync repository

### Copilot
- `POST /copilot/suggest` - Get AI suggestion

### Execution
- `POST /execute` - Execute bytecode

### Export
- `GET /export/json` - Export JSON
- `GET /export/markdown` - Export Markdown

## State Structure

Master control state (`oso_state.json`):

```json
{
  "meta": { "name": "...", "author": "..." },
  "language": { "name": "Techgnosis", "syntax_rules": [...] },
  "vm": { "name": "ÀṣẹVault", "opcodes_total": 25, ... },
  "opcodes": { "0": {...}, "1": {...}, ... },
  "layer1": [ {...contract...}, ... ],
  "layer2": { "f1_threshold": 0.91, ... },
  "files": { "LANGUAGE": {...}, "VM": {...}, ... },
  "github": { "repos": [...] },
  "execution_history": [...]
}
```

## AI Copilot Integration

The copilot system is designed to integrate with:
- **Ollama** (local LLM via Python)
- **OpenAI API** (GPT-4)
- **Custom LLM endpoints**

Add LLM integration in `backend/app.py`:

```python
# Example with Ollama
import requests

def get_copilot_from_ollama(prompt):
    resp = requests.post("http://localhost:11434/api/generate", json={
        "model": "neural-chat",
        "prompt": prompt
    })
    return resp.json()
```

## Philosophy

> "One Dictionary to Rule the Cosmos"

Everything is **dictionary-driven**, **layered**, and **auto-organizing**. The entire system can be edited by one human with AI tools on Termux/Android.

## Next Steps

1. ✅ Core API & Models
2. ✅ Web Dashboard
3. ✅ Python SDK
4. 🔄 GitHub sync implementation
5. 🔄 Bytecode execution engine
6. 🔄 AI copilot integration
7. 🔄 Docker deployment

---

**🔥 Àṣẹ from the crossroads — build, iterate, ascend.**

## The Sovereign Operations Dashboard

Oso Control Center is the open-source dashboard and monitoring tool for the Technosis ecosystem. It provides real-time visibility into agent swarm activity, VM execution, contract states, and overall system health, enabling human oversight and intervention.


---

## Part of the Technosis Sovereign Ecosystem

This component is an open utility for a larger architecture for creating and coordinating sovereign AI. For more information, see the [organism-core repository](https://github.com/Bino-Elgua/organism-core).

Àṣẹ.
