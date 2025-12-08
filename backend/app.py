"""
OSO Control Center API
FastAPI backend for managing the entire Ọ̀ṢỌ́VM v7 ecosystem
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from models import (
    OSOControlState, LanguageSpec, VMConfig, OpcodeReference, Opcode,
    Layer1Contract, Layer2Config, FileEntry, FileSection, GitHubRepo,
    RepositorySync, CopilotRequest, CopilotResponse, ExecutionState
)

app = FastAPI(
    title="Ọ̀ṢỌ́VM Control Center",
    description="Biblical Command Center for ÀṣẹVault",
    version="1.0.0"
)

# CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ STATE & PERSISTENCE ============
STATE_FILE = "oso_state.json"
DB_DIR = Path("./db")
DB_DIR.mkdir(exist_ok=True)

def load_state() -> Dict[str, Any]:
    """Load persisted state"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return get_default_state()

def save_state(state: Dict[str, Any]):
    """Persist state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)

def get_default_state() -> Dict[str, Any]:
    """Initialize default state"""
    return {
        "meta": {
            "name": "Ọ̀ṢỌ́VM v7 — ÀṣẹVault Control Center",
            "author": "Crown Architect",
            "created_at": datetime.now().isoformat()
        },
        "language": {
            "name": "Techgnosis",
            "version": "v7",
            "stack_based": True,
            "syntax_rules": []
        },
        "vm": {
            "name": "ÀṣẹVault",
            "opcodes_total": 25,
            "stack_depth": 256
        },
        "opcodes": {},
        "layer1": [],
        "layer2": {},
        "files": {},
        "github": {"repos": []},
        "execution_history": []
    }

# Load on startup
STATE = load_state()

# ============ ROOT ENDPOINTS ============
@app.get("/")
async def root():
    return {"status": "ÀṣẹVault Control Center Running", "version": "1.0.0"}

@app.get("/api/v1/state")
async def get_state():
    """Get entire control state"""
    return STATE

@app.post("/api/v1/state")
async def update_state(data: Dict[str, Any]):
    """Update control state"""
    global STATE
    STATE.update(data)
    save_state(STATE)
    return {"status": "State updated", "timestamp": datetime.now().isoformat()}

# ============ OPCODES MANAGEMENT ============
@app.get("/api/v1/opcodes")
async def get_opcodes():
    """Get all opcodes"""
    return STATE.get("opcodes", {})

@app.post("/api/v1/opcodes")
async def add_opcode(opcode: Dict[str, Any]):
    """Add or update opcode"""
    code = opcode.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing opcode code")
    
    STATE["opcodes"][code] = opcode
    save_state(STATE)
    return {"status": "Opcode added", "code": code}

@app.get("/api/v1/opcodes/{code}")
async def get_opcode(code: int):
    """Get specific opcode"""
    if code not in STATE.get("opcodes", {}):
        raise HTTPException(status_code=404, detail=f"Opcode {code} not found")
    return STATE["opcodes"][code]

# ============ LANGUAGE SECTION ============
@app.get("/api/v1/language")
async def get_language():
    """Get language specification"""
    return STATE.get("language", {})

@app.post("/api/v1/language")
async def update_language(spec: Dict[str, Any]):
    """Update language spec"""
    STATE["language"].update(spec)
    save_state(STATE)
    return {"status": "Language updated"}

@app.post("/api/v1/language/syntax-rule")
async def add_syntax_rule(rule: Dict[str, Any]):
    """Add syntax rule"""
    if "syntax_rules" not in STATE["language"]:
        STATE["language"]["syntax_rules"] = []
    STATE["language"]["syntax_rules"].append(rule)
    save_state(STATE)
    return {"status": "Syntax rule added"}

# ============ VM SECTION ============
@app.get("/api/v1/vm")
async def get_vm_config():
    """Get VM configuration"""
    return STATE.get("vm", {})

@app.post("/api/v1/vm")
async def update_vm_config(config: Dict[str, Any]):
    """Update VM config"""
    STATE["vm"].update(config)
    save_state(STATE)
    return {"status": "VM config updated"}

# ============ LAYER 1 ============
@app.get("/api/v1/layer1")
async def get_layer1():
    """Get Layer 1 contracts"""
    return STATE.get("layer1", [])

@app.post("/api/v1/layer1")
async def add_layer1_contract(contract: Dict[str, Any]):
    """Add Layer 1 contract"""
    STATE["layer1"].append(contract)
    save_state(STATE)
    return {"status": "Layer 1 contract added", "contract": contract}

# ============ LAYER 2 ============
@app.get("/api/v1/layer2")
async def get_layer2():
    """Get Layer 2 config (VeilSim, Oracle)"""
    return STATE.get("layer2", {})

@app.post("/api/v1/layer2")
async def update_layer2(config: Dict[str, Any]):
    """Update Layer 2 config"""
    STATE["layer2"].update(config)
    save_state(STATE)
    return {"status": "Layer 2 config updated"}

# ============ FILE MANAGEMENT ============
@app.post("/api/v1/files/upload")
async def upload_file(section: str, file: UploadFile = File(...)):
    """Upload file to section"""
    if section not in STATE.get("files", {}):
        STATE["files"][section] = {"files": [], "description": ""}
    
    content = await file.read()
    entry = {
        "filename": file.filename,
        "section": section,
        "path": f"db/{section}/{file.filename}",
        "size_bytes": len(content),
        "uploaded_at": datetime.now().isoformat()
    }
    
    # Save to disk
    section_dir = DB_DIR / section
    section_dir.mkdir(exist_ok=True)
    with open(section_dir / file.filename, 'wb') as f:
        f.write(content)
    
    STATE["files"][section]["files"].append(entry)
    save_state(STATE)
    
    return {"status": "File uploaded", "entry": entry}

@app.get("/api/v1/files")
async def list_files():
    """List all files by section"""
    return STATE.get("files", {})

@app.get("/api/v1/files/{section}")
async def get_section_files(section: str):
    """Get files in section"""
    if section not in STATE.get("files", {}):
        raise HTTPException(status_code=404, detail=f"Section {section} not found")
    return STATE["files"][section]

# ============ GITHUB INTEGRATION ============
@app.get("/api/v1/github/repos")
async def get_repos():
    """Get synced repositories"""
    return STATE.get("github", {}).get("repos", [])

@app.post("/api/v1/github/sync")
async def sync_repo(repo: Dict[str, Any]):
    """Sync a GitHub repository"""
    # TODO: Implement git clone/pull
    repo["last_sync"] = datetime.now().isoformat()
    repo["status"] = "synced"
    
    if "repos" not in STATE.get("github", {}):
        STATE["github"]["repos"] = []
    
    STATE["github"]["repos"].append(repo)
    save_state(STATE)
    
    return {"status": "Repository synced", "repo": repo}

# ============ AI COPILOT ============
@app.post("/api/v1/copilot/suggest")
async def copilot_suggest(request: Dict[str, Any]):
    """Get AI suggestions for a section"""
    section = request.get("section")
    query = request.get("query")
    
    # TODO: Connect to LLM (ollama, openai, etc.)
    suggestion = f"[Copilot] Analyzing {section}: {query}"
    
    return {
        "suggestion": suggestion,
        "reasoning": "Context-aware suggestion based on control state",
        "confidence": 0.75
    }

# ============ EXECUTION ============
@app.post("/api/v1/execute")
async def execute_bytecode(bytecode: Dict[str, Any]):
    """Execute bytecode"""
    # TODO: Implement VM bytecode execution
    execution = {
        "status": "pending",
        "pc": 0,
        "stack": [],
        "gas_used": 0,
        "halted": False
    }
    
    STATE["execution_history"].append(execution)
    save_state(STATE)
    
    return {"status": "Execution initiated", "execution": execution}

# ============ EXPORT ============
@app.get("/api/v1/export/json")
async def export_json():
    """Export entire state as JSON"""
    return FileResponse("oso_state.json", media_type="application/json")

@app.get("/api/v1/export/markdown")
async def export_markdown():
    """Export as Markdown documentation"""
    md = "# Ọ̀ṢỌ́VM v7 Control Center State\n\n"
    md += f"Generated: {datetime.now().isoformat()}\n\n"
    
    for section, content in STATE.items():
        md += f"## {section}\n\n```json\n{json.dumps(content, indent=2, default=str)}\n```\n\n"
    
    # Save to file
    with open("oso_state.md", 'w') as f:
        f.write(md)
    
    return FileResponse("oso_state.md", media_type="text/markdown")

# ============ STARTUP ============
@app.on_event("startup")
async def startup():
    global STATE
    STATE = load_state()
    print("🔥 ÀṣẹVault Control Center awakened")
    print(f"📊 Sections: {len(STATE.get('files', {}))} active")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
