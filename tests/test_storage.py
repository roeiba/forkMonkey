"""
Tests for storage system
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from src.genetics import GeneticsEngine
from src.storage import MonkeyStorage


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing"""
    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp())
    original_dir = Path.cwd()
    
    # Change to temp directory
    import os
    os.chdir(temp_dir)
    
    storage = MonkeyStorage()
    
    yield storage
    
    # Cleanup
    os.chdir(original_dir)
    shutil.rmtree(temp_dir)


class TestMonkeyStorage:
    """Test monkey storage"""
    
    def test_save_and_load_dna(self, temp_storage):
        """Test saving and loading DNA"""
        dna = GeneticsEngine.generate_random_dna()
        
        # Save
        success = temp_storage.save_dna_locally(dna)
        assert success
        
        # Load
        loaded = temp_storage.load_dna()
        assert loaded is not None
        assert loaded.dna_hash == dna.dna_hash
        assert loaded.generation == dna.generation
    
    def test_load_nonexistent_dna(self, temp_storage):
        """Test loading when no DNA exists"""
        dna = temp_storage.load_dna()
        assert dna is None
    
    def test_save_stats(self, temp_storage):
        """Test saving stats"""
        dna = GeneticsEngine.generate_random_dna()
        
        success = temp_storage.save_stats(dna, age_days=5)
        assert success
        
        # Check file exists
        stats_file = Path("monkey_data/stats.json")
        assert stats_file.exists()
        
        # Check content
        with open(stats_file) as f:
            stats = json.load(f)
        
        assert stats["dna_hash"] == dna.dna_hash
        assert stats["age_days"] == 5
        assert "rarity_score" in stats
    
    def test_save_history_entry(self, temp_storage):
        """Test saving history entry"""
        dna = GeneticsEngine.generate_random_dna()
        
        success = temp_storage.save_history_entry(dna, "Test story")
        assert success
        
        # Load history
        history = temp_storage.get_history()
        assert len(history) == 1
        assert history[0]["dna_hash"] == dna.dna_hash
        assert history[0]["story"] == "Test story"
    
    def test_multiple_history_entries(self, temp_storage):
        """Test multiple history entries"""
        dna1 = GeneticsEngine.generate_random_dna()
        dna2 = GeneticsEngine.generate_random_dna()
        
        temp_storage.save_history_entry(dna1, "First")
        temp_storage.save_history_entry(dna2, "Second")
        
        history = temp_storage.get_history()
        assert len(history) == 2
        assert history[0]["story"] == "First"
        assert history[1]["story"] == "Second"
    
    def test_get_empty_history(self, temp_storage):
        """Test getting history when empty"""
        history = temp_storage.get_history()
        assert history == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
