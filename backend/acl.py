"""
Access Control Layer
Manages authentication and authorization
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib
import secrets

class ACL:
    """Access Control System"""
    
    ROLES = {
        "admin": ["read", "write", "delete", "sync", "execute", "copilot"],
        "editor": ["read", "write", "sync", "execute", "copilot"],
        "viewer": ["read"],
        "api": ["read", "write", "execute"]  # For Amp/SDK access
    }
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.api_keys = {}
        
        # Initialize default users
        self.create_user("admin", "aso-crown", "admin")
        self.create_api_key("amp-sdk", "api")
    
    def create_user(self, username: str, password: str, role: str = "editor") -> Dict:
        """Create a user account"""
        if username in self.users:
            return {"error": "User already exists"}
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        self.users[username] = {
            "password_hash": password_hash,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "permissions": self.ROLES.get(role, [])
        }
        
        return {
            "status": "User created",
            "username": username,
            "role": role
        }
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session token"""
        if username not in self.users:
            return None
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = self.users[username]
        
        if user["password_hash"] != password_hash:
            return None
        
        # Create session
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            "username": username,
            "role": user["role"],
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=8)
        }
        
        return token
    
    def validate_session(self, token: str) -> bool:
        """Validate session token"""
        if token not in self.sessions:
            return False
        
        session = self.sessions[token]
        if datetime.now() > session["expires_at"]:
            del self.sessions[token]
            return False
        
        return True
    
    def create_api_key(self, name: str, role: str = "api") -> Dict:
        """Create API key for SDK/Amp access"""
        api_key = secrets.token_urlsafe(32)
        
        self.api_keys[api_key] = {
            "name": name,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "permissions": self.ROLES.get(role, []),
            "active": True
        }
        
        return {
            "api_key": api_key,
            "name": name,
            "role": role
        }
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key"""
        if api_key not in self.api_keys:
            return False
        
        key_data = self.api_keys[api_key]
        if not key_data["active"]:
            return False
        
        return True
    
    def check_permission(self, token_or_key: str, action: str) -> bool:
        """Check if user/api has permission for action"""
        # Check session token
        if token_or_key in self.sessions:
            session = self.sessions[token_or_key]
            role = session["role"]
            return action in self.ROLES.get(role, [])
        
        # Check API key
        if token_or_key in self.api_keys:
            key_data = self.api_keys[token_or_key]
            if not key_data["active"]:
                return False
            return action in key_data["permissions"]
        
        return False
    
    def revoke_session(self, token: str) -> Dict:
        """Revoke session"""
        if token in self.sessions:
            del self.sessions[token]
            return {"status": "Session revoked"}
        return {"error": "Session not found"}
    
    def revoke_api_key(self, api_key: str) -> Dict:
        """Revoke API key"""
        if api_key in self.api_keys:
            self.api_keys[api_key]["active"] = False
            return {"status": "API key revoked"}
        return {"error": "API key not found"}
    
    def list_users(self) -> Dict:
        """List all users"""
        return {
            username: {
                "role": user["role"],
                "created_at": user["created_at"]
            }
            for username, user in self.users.items()
        }
    
    def list_api_keys(self) -> Dict:
        """List all API keys"""
        return {
            api_key: {
                "name": key_data["name"],
                "role": key_data["role"],
                "active": key_data["active"]
            }
            for api_key, key_data in self.api_keys.items()
        }


# Global ACL instance
_acl = None

def get_acl() -> ACL:
    """Get or create global ACL"""
    global _acl
    if _acl is None:
        _acl = ACL()
    return _acl


if __name__ == "__main__":
    acl = get_acl()
    
    # Test
    token = acl.authenticate("admin", "aso-crown")
    print(f"Token: {token}")
    print(f"Valid: {acl.validate_session(token)}")
    print(f"Can read: {acl.check_permission(token, 'read')}")
    print(f"Can delete: {acl.check_permission(token, 'delete')}")
    
    # API key test
    print(f"\nAPI Keys: {acl.list_api_keys()}")
