"""
GitHub Repository Synchronization
Manages cloning, pulling, and pushing repositories
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class GitHubSync:
    """Handle GitHub repository operations"""
    
    def __init__(self, base_path: str = "./repos"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def clone_repo(self, owner: str, name: str, branch: str = "main") -> Dict[str, str]:
        """Clone a repository"""
        url = f"git@github.com:{owner}/{name}.git"
        local_path = self.base_path / name
        
        try:
            subprocess.run(
                ["git", "clone", "-b", branch, url, str(local_path)],
                check=True,
                capture_output=True
            )
            return {
                "status": "success",
                "path": str(local_path),
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def pull_repo(self, local_path: str, branch: str = "main") -> Dict[str, str]:
        """Pull latest changes"""
        try:
            subprocess.run(
                ["git", "-C", local_path, "pull", "origin", branch],
                check=True,
                capture_output=True
            )
            return {
                "status": "success",
                "message": f"Pulled {branch}",
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def push_repo(self, local_path: str, branch: str = "main", 
                  message: str = "Update from control center") -> Dict[str, str]:
        """Push changes to repository"""
        try:
            # Add all changes
            subprocess.run(
                ["git", "-C", local_path, "add", "."],
                check=True,
                capture_output=True
            )
            
            # Commit
            subprocess.run(
                ["git", "-C", local_path, "commit", "-m", message],
                check=False,  # OK if nothing to commit
                capture_output=True
            )
            
            # Push
            subprocess.run(
                ["git", "-C", local_path, "push", "origin", branch],
                check=True,
                capture_output=True
            )
            
            return {
                "status": "success",
                "message": f"Pushed to {branch}",
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status(self, local_path: str) -> Dict[str, str]:
        """Get git status of repository"""
        try:
            result = subprocess.run(
                ["git", "-C", local_path, "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Get current branch
            branch_result = subprocess.run(
                ["git", "-C", local_path, "rev-parse", "--abbrev-ref", "HEAD"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Get latest commit
            log_result = subprocess.run(
                ["git", "-C", local_path, "log", "-1", "--format=%h %s"],
                check=True,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "success",
                "branch": branch_result.stdout.strip(),
                "changes": result.stdout.strip() or "clean",
                "latest_commit": log_result.stdout.strip(),
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def sync_all_oso_repos(self) -> Dict[str, Dict]:
        """Sync all OSO ecosystem repositories"""
        oso_repos = [
            ("jbino85", "techgnosis", "main"),
            ("jbino85", "osovm", "main"),
            ("jbino85", "ifascript", "main"),
            ("jbino85", "zangbeto", "main"),
            ("jbino85", "twelve-thrones-genesis", "main"),
            ("jbino85", "ase-mirror", "master")
        ]
        
        results = {}
        for owner, name, branch in oso_repos:
            local_path = self.base_path / name
            
            if local_path.exists():
                # Pull
                results[name] = self.pull_repo(str(local_path), branch)
            else:
                # Clone
                results[name] = self.clone_repo(owner, name, branch)
        
        return results


if __name__ == "__main__":
    sync = GitHubSync()
    print("Syncing OSO repositories...")
    results = sync.sync_all_oso_repos()
    print(json.dumps(results, indent=2))
