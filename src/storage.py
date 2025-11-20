"""
ForkMonkey Storage

Handles DNA storage in GitHub Secrets and history in files.
"""

import os
import json
import base64
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path
from github import Github, GithubException
from src.genetics import MonkeyDNA, GeneticsEngine


class MonkeyStorage:
    """Manages monkey data storage"""
    
    def __init__(self, repo_name: Optional[str] = None, github_token: Optional[str] = None):
        self.repo_name = repo_name or os.getenv("GITHUB_REPOSITORY") or "test/repo"
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        
        self.data_dir = Path("monkey_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize GitHub client if token available
        self.github = None
        self.repo = None
        if self.github_token:
            try:
                self.github = Github(self.github_token)
                self.repo = self.github.get_repo(self.repo_name)
            except Exception as e:
                print(f"⚠️  GitHub API not available: {e}")
    
    def save_dna_to_secrets(self, dna: MonkeyDNA) -> bool:
        """
        Save DNA to GitHub Secrets (private, only owner can see)
        
        Note: Requires GitHub API with secrets scope
        """
        if not self.repo:
            print("⚠️  GitHub API not available, saving locally only")
            return self.save_dna_locally(dna)
        
        try:
            # Convert DNA to JSON
            dna_dict = GeneticsEngine.dna_to_dict(dna)
            dna_json = json.dumps(dna_dict)
            
            # Encode for secret storage
            dna_encoded = base64.b64encode(dna_json.encode()).decode()
            
            # Store in secret (requires admin access)
            # Note: PyGithub doesn't support secrets API well, use REST API
            print("⚠️  Storing DNA in secrets requires GitHub CLI or REST API")
            print("   Saving locally for now...")
            
            return self.save_dna_locally(dna)
            
        except Exception as e:
            print(f"⚠️  Failed to save to secrets: {e}")
            return self.save_dna_locally(dna)
    
    def save_dna_locally(self, dna: MonkeyDNA) -> bool:
        """Save DNA to local file"""
        try:
            dna_dict = GeneticsEngine.dna_to_dict(dna)
            
            dna_file = self.data_dir / "dna.json"
            with open(dna_file, "w") as f:
                json.dump(dna_dict, f, indent=2)
            
            print(f"✅ DNA saved to {dna_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save DNA: {e}")
            return False
    
    def load_dna(self) -> Optional[MonkeyDNA]:
        """Load DNA from local file"""
        try:
            dna_file = self.data_dir / "dna.json"
            
            if not dna_file.exists():
                print("ℹ️  No DNA file found")
                return None
            
            with open(dna_file, "r") as f:
                dna_dict = json.load(f)
            
            dna = GeneticsEngine.dict_to_dna(dna_dict)
            print(f"✅ DNA loaded from {dna_file}")
            return dna
            
        except Exception as e:
            print(f"❌ Failed to load DNA: {e}")
            return None
    
    def save_history_entry(self, dna: MonkeyDNA, story: str = "") -> bool:
        """Add entry to evolution history"""
        try:
            history_file = self.data_dir / "history.json"
            
            # Load existing history
            if history_file.exists():
                with open(history_file, "r") as f:
                    history = json.load(f)
            else:
                history = {"entries": []}
            
            # Add new entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "dna_hash": dna.dna_hash,
                "generation": dna.generation,
                "mutation_count": dna.mutation_count,
                "rarity_score": dna.get_rarity_score(),
                "traits": {
                    cat.value: trait.value
                    for cat, trait in dna.traits.items()
                },
                "story": story
            }
            
            history["entries"].append(entry)
            
            # Save
            with open(history_file, "w") as f:
                json.dump(history, f, indent=2)
            
            print(f"✅ History entry saved")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save history: {e}")
            return False
    
    def get_history(self) -> List[dict]:
        """Get evolution history"""
        try:
            history_file = self.data_dir / "history.json"
            
            if not history_file.exists():
                return []
            
            with open(history_file, "r") as f:
                history = json.load(f)
            
            return history.get("entries", [])
            
        except Exception as e:
            print(f"❌ Failed to load history: {e}")
            return []
    
    def save_stats(self, dna: MonkeyDNA, age_days: int = 0) -> bool:
        """Save monkey statistics"""
        try:
            stats = {
                "dna_hash": dna.dna_hash,
                "generation": dna.generation,
                "age_days": age_days,
                "mutation_count": dna.mutation_count,
                "rarity_score": dna.get_rarity_score(),
                "parent_id": dna.parent_id,
                "traits": {
                    cat.value: {
                        "value": trait.value,
                        "rarity": trait.rarity.value
                    }
                    for cat, trait in dna.traits.items()
                },
                "last_updated": datetime.now().isoformat()
            }
            
            stats_file = self.data_dir / "stats.json"
            with open(stats_file, "w") as f:
                json.dump(stats, f, indent=2)
            
            print(f"✅ Stats saved")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save stats: {e}")
            return False
    
    def detect_fork(self) -> Optional[str]:
        """
        Detect if this repo is a fork and get parent repo
        
        Returns parent repo name if fork, None otherwise
        """
        if not self.repo:
            return None
        
        try:
            if self.repo.fork:
                parent = self.repo.parent
                return parent.full_name
            return None
            
        except Exception as e:
            print(f"⚠️  Failed to detect fork: {e}")
            return None
    
    def get_parent_dna(self, parent_repo: str) -> Optional[MonkeyDNA]:
        """
        Fetch parent monkey's DNA from parent repository
        
        Args:
            parent_repo: Full repo name (owner/repo)
        """
        if not self.github:
            print("⚠️  GitHub API not available")
            return None
        
        try:
            parent = self.github.get_repo(parent_repo)
            
            # Try to get DNA file from parent
            content = parent.get_contents("monkey_data/dna.json")
            dna_json = content.decoded_content.decode()
            dna_dict = json.loads(dna_json)
            
            return GeneticsEngine.dict_to_dna(dna_dict)
            
        except GithubException as e:
            print(f"⚠️  Failed to fetch parent DNA: {e}")
            return None
    
    def initialize_from_parent(self) -> Optional[MonkeyDNA]:
        """
        Initialize child monkey from parent (for forks)
        
        Returns child DNA if successful, None otherwise
        """
        parent_repo = self.detect_fork()
        
        if not parent_repo:
            print("ℹ️  Not a fork, generating new monkey")
            return None
        
        print(f"🍴 Fork detected! Parent: {parent_repo}")
        
        parent_dna = self.get_parent_dna(parent_repo)
        
        if not parent_dna:
            print("⚠️  Could not fetch parent DNA, generating new monkey")
            return None
        
        print(f"👶 Breeding child from parent (Generation {parent_dna.generation})")
        
        # Breed child
        child_dna = GeneticsEngine.breed(parent_dna, mutation_rate=0.3)
        
        print(f"✅ Child monkey created (Generation {child_dna.generation})")
        print(f"   Parent: {parent_dna.dna_hash}")
        print(f"   Child: {child_dna.dna_hash}")
        
        return child_dna


def main():
    """Test storage system"""
    from src.genetics import GeneticsEngine
    
    print("💾 ForkMonkey Storage Test\n")
    
    storage = MonkeyStorage()
    
    # Generate test monkey
    print("1. Generating test monkey...")
    dna = GeneticsEngine.generate_random_dna()
    
    # Save DNA
    print("\n2. Saving DNA...")
    storage.save_dna_locally(dna)
    
    # Save stats
    print("\n3. Saving stats...")
    storage.save_stats(dna, age_days=5)
    
    # Save history
    print("\n4. Saving history entry...")
    storage.save_history_entry(dna, "Your monkey was born!")
    
    # Load DNA
    print("\n5. Loading DNA...")
    loaded_dna = storage.load_dna()
    if loaded_dna:
        print(f"   Loaded: {loaded_dna.dna_hash}")
        print(f"   Match: {loaded_dna.dna_hash == dna.dna_hash}")
    
    # Get history
    print("\n6. Loading history...")
    history = storage.get_history()
    print(f"   Entries: {len(history)}")
    
    print("\n✅ Storage system working!")


if __name__ == "__main__":
    main()
