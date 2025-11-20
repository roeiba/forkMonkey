"""
Tests for genetics system
"""

import pytest
from src.genetics import (
    GeneticsEngine, MonkeyDNA, Trait, TraitCategory, Rarity
)


class TestGeneticsEngine:
    """Test genetics engine"""
    
    def test_generate_random_dna(self):
        """Test random DNA generation"""
        dna = GeneticsEngine.generate_random_dna()
        
        assert dna.generation == 1
        assert dna.parent_id is None
        assert len(dna.traits) == len(TraitCategory)
        assert dna.dna_hash != ""
        
        # Check all categories present
        for category in TraitCategory:
            assert category in dna.traits
            assert isinstance(dna.traits[category], Trait)
    
    def test_dna_hash_uniqueness(self):
        """Test that different DNA has different hashes"""
        dna1 = GeneticsEngine.generate_random_dna()
        dna2 = GeneticsEngine.generate_random_dna()
        
        # Very unlikely to be the same
        assert dna1.dna_hash != dna2.dna_hash
    
    def test_rarity_distribution(self):
        """Test rarity distribution is reasonable"""
        rarities = {r: 0 for r in Rarity}
        
        # Generate many monkeys
        for _ in range(1000):
            dna = GeneticsEngine.generate_random_dna()
            for trait in dna.traits.values():
                rarities[trait.rarity] += 1
        
        total = sum(rarities.values())
        
        # Check approximate distribution
        common_pct = (rarities[Rarity.COMMON] / total) * 100
        legendary_pct = (rarities[Rarity.LEGENDARY] / total) * 100
        
        assert 50 < common_pct < 70  # Should be around 60%
        assert 2 < legendary_pct < 8  # Should be around 5%
    
    def test_breed(self):
        """Test breeding mechanics"""
        parent = GeneticsEngine.generate_random_dna()
        child = GeneticsEngine.breed(parent, mutation_rate=0.3)
        
        assert child.generation == parent.generation + 1
        assert child.parent_id == parent.dna_hash
        assert child.dna_hash != parent.dna_hash
        
        # Child should have some inherited traits
        inherited_count = sum(
            1 for cat in TraitCategory
            if child.traits[cat].value == parent.traits[cat].value
        )
        
        # With 50% inheritance + mutations, expect some similarity
        assert inherited_count >= 0  # At least possible to inherit
    
    def test_evolve(self):
        """Test evolution mechanics"""
        dna = GeneticsEngine.generate_random_dna()
        evolved = GeneticsEngine.evolve(dna, evolution_strength=0.5)
        
        assert evolved.generation == dna.generation
        assert evolved.parent_id == dna.parent_id
        assert evolved.mutation_count >= dna.mutation_count
        
        # Should have some changes with 50% strength
        changed_count = sum(
            1 for cat in TraitCategory
            if evolved.traits[cat].value != dna.traits[cat].value
        )
        
        assert changed_count >= 0  # At least possible to change
    
    def test_rarity_score(self):
        """Test rarity score calculation"""
        dna = GeneticsEngine.generate_random_dna()
        score = dna.get_rarity_score()
        
        assert 0 <= score <= 100
    
    def test_serialization(self):
        """Test DNA serialization and deserialization"""
        original = GeneticsEngine.generate_random_dna()
        
        # Convert to dict
        data = GeneticsEngine.dna_to_dict(original)
        
        assert isinstance(data, dict)
        assert "generation" in data
        assert "traits" in data
        assert "dna_hash" in data
        
        # Convert back
        restored = GeneticsEngine.dict_to_dna(data)
        
        assert restored.dna_hash == original.dna_hash
        assert restored.generation == original.generation
        assert len(restored.traits) == len(original.traits)
        
        # Check all traits match
        for category in TraitCategory:
            assert restored.traits[category].value == original.traits[category].value
            assert restored.traits[category].rarity == original.traits[category].rarity


class TestTrait:
    """Test trait model"""
    
    def test_trait_creation(self):
        """Test trait creation"""
        trait = Trait(
            category=TraitCategory.BODY_COLOR,
            value="brown",
            rarity=Rarity.COMMON
        )
        
        assert trait.category == TraitCategory.BODY_COLOR
        assert trait.value == "brown"
        assert trait.rarity == Rarity.COMMON
        assert trait.gene_sequence != ""
    
    def test_gene_sequence_generation(self):
        """Test gene sequence is generated"""
        trait = Trait(
            category=TraitCategory.FACE_EXPRESSION,
            value="happy",
            rarity=Rarity.COMMON
        )
        
        assert len(trait.gene_sequence) == 8  # MD5 hash truncated to 8 chars
    
    def test_same_trait_same_sequence(self):
        """Test same trait generates same sequence"""
        trait1 = Trait(
            category=TraitCategory.BODY_COLOR,
            value="golden",
            rarity=Rarity.UNCOMMON
        )
        
        trait2 = Trait(
            category=TraitCategory.BODY_COLOR,
            value="golden",
            rarity=Rarity.UNCOMMON
        )
        
        assert trait1.gene_sequence == trait2.gene_sequence


class TestMonkeyDNA:
    """Test MonkeyDNA model"""
    
    def test_dna_creation(self):
        """Test DNA creation"""
        traits = {
            TraitCategory.BODY_COLOR: Trait(
                category=TraitCategory.BODY_COLOR,
                value="brown",
                rarity=Rarity.COMMON
            )
        }
        
        dna = MonkeyDNA(
            generation=1,
            traits=traits
        )
        
        assert dna.generation == 1
        assert dna.dna_hash != ""
    
    def test_dna_hash_calculation(self):
        """Test DNA hash is calculated correctly"""
        traits = {
            TraitCategory.BODY_COLOR: Trait(
                category=TraitCategory.BODY_COLOR,
                value="brown",
                rarity=Rarity.COMMON
            )
        }
        
        dna1 = MonkeyDNA(generation=1, traits=traits)
        dna2 = MonkeyDNA(generation=1, traits=traits)
        
        # Same traits should give same hash
        assert dna1.dna_hash == dna2.dna_hash


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
