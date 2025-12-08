"""
OSO Control Center Data Models
Sacred data structures for the entire ecosystem
"""

from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

# ============ OPCODES ============
class Opcode(BaseModel):
    code: int
    name: str
    description: str
    gas_cost: int = 1
    category: str  # "core", "math", "layer1", "layer2", "attestation"
    stack_input: int = 0
    stack_output: int = 0
    
class OpcodeReference(BaseModel):
    opcodes: Dict[int, Opcode]
    version: str = "v7"
    
# ============ LANGUAGE ============
class SyntaxRule(BaseModel):
    rule_name: str
    pattern: str
    description: str
    example: str

class LanguageSpec(BaseModel):
    name: str
    version: str
    stack_based: bool = True
    postfix_notation: bool = True
    syntax_rules: List[SyntaxRule] = []
    bytecode_limit: int = 4096
    reserved_keywords: List[str] = []

# ============ VM ============
class VMConfig(BaseModel):
    name: str
    version: str
    opcodes_total: int = 25
    stack_depth: int = 256
    memory_limit: int = 65536
    gas_model: str = "fixed"
    execution_mode: str = "interpreter"

class StackFrame(BaseModel):
    depth: int
    values: List[Any] = []
    
class ExecutionState(BaseModel):
    pc: int  # program counter
    stack: List[Any] = []
    memory: Dict[int, Any] = {}
    gas_used: int = 0
    halted: bool = False

# ============ LAYER 1: WITNESSING ============
class Witness(BaseModel):
    event_type: str  # "package_arrived", "signature", "location"
    signature: str
    geo_hash: str
    timestamp: datetime
    proof: str  # merkle root or hash

class Layer1Contract(BaseModel):
    name: str
    description: str
    triggers: List[str]  # ["witness_delivery", "impact_attest"]
    ase_reward: float
    proof_required: bool = True

# ============ LAYER 2: SIMULATION & ORACLE ============
class VeilSimScorer(BaseModel):
    veil_id: int
    f1_score: float
    ase_minted: float
    timestamp: datetime
    
class OracleResult(BaseModel):
    oracle_type: str  # "veilsim", "route_optimizer"
    result: Dict[str, Any]
    confidence: float
    timestamp: datetime

class Layer2Config(BaseModel):
    f1_threshold: float = 0.91
    base_ase_reward: float = 1.0
    veilsim_count: int = 747
    monte_carlo_iterations: int = 10000

# ============ FILE MANAGEMENT ============
class FileEntry(BaseModel):
    filename: str
    section: str  # "LANGUAGE", "VM", "LAYER1", "LAYER2", "OPCODES", "DOCS"
    path: str
    content: Optional[str] = None
    size_bytes: int = 0
    uploaded_at: datetime
    
class FileSection(BaseModel):
    section_name: str
    files: List[FileEntry] = []
    description: str = ""

# ============ GITHUB INTEGRATION ============
class GitHubRepo(BaseModel):
    owner: str
    name: str
    url: str
    branch: str = "main"
    local_path: str
    last_sync: Optional[datetime] = None
    status: str  # "synced", "pending", "error"

class RepositorySync(BaseModel):
    repos: List[GitHubRepo]
    
# ============ AI COPILOT ============
class CopilotRequest(BaseModel):
    section: str
    query: str
    context: Optional[Dict[str, Any]] = None
    
class CopilotResponse(BaseModel):
    suggestion: str
    reasoning: str
    code_snippet: Optional[str] = None
    confidence: float

# ============ MASTER CONTROL STATE ============
class OSOControlState(BaseModel):
    """The entire control center state in one structure"""
    meta: Dict[str, Any]
    language: LanguageSpec
    vm_config: VMConfig
    opcode_ref: OpcodeReference
    layer1: List[Layer1Contract]
    layer2: Layer2Config
    files: Dict[str, FileSection]  # section -> files
    github: RepositorySync
    execution_history: List[ExecutionState] = []
    last_updated: datetime
    version: str = "1.0.0"
