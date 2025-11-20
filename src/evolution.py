"""
ForkMonkey Evolution Engine

AI-powered evolution using Claude to make intelligent mutations.
"""

import os
import json
from typing import Optional
from anthropic import Anthropic
from src.genetics import MonkeyDNA, GeneticsEngine, TraitCategory


class EvolutionAgent:
    """AI agent that evolves monkeys intelligently"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        self.client = Anthropic(api_key=self.api_key)
    
    def evolve_with_ai(self, dna: MonkeyDNA, days_passed: int = 1) -> MonkeyDNA:
        """
        Use AI to intelligently evolve the monkey
        
        Args:
            dna: Current monkey DNA
            days_passed: Number of days since last evolution
        """
        
        # Get current traits as readable format
        current_traits = {
            cat.value: {
                "value": trait.value,
                "rarity": trait.rarity.value
            }
            for cat, trait in dna.traits.items()
        }
        
        # Create prompt for Claude
        prompt = self._create_evolution_prompt(current_traits, days_passed, dna.generation)
        
        try:
            # Call Claude
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response
            evolution_decision = self._parse_ai_response(response.content[0].text)
            
            # Apply AI-suggested changes
            evolved_dna = self._apply_evolution(dna, evolution_decision)
            
            return evolved_dna
            
        except Exception as e:
            print(f"⚠️  AI evolution failed: {e}")
            print("   Falling back to random evolution...")
            # Fallback to random evolution
            return GeneticsEngine.evolve(dna, evolution_strength=0.1)
    
    def _create_evolution_prompt(self, traits: dict, days: int, generation: int) -> str:
        """Create prompt for Claude"""
        return f"""You are an AI evolution agent for ForkMonkey - a digital pet that lives on GitHub.

Your task is to evolve this monkey's appearance in a subtle, aesthetically pleasing way.

Current Monkey Traits:
{json.dumps(traits, indent=2)}

Context:
- Generation: {generation}
- Days since last evolution: {days}
- Evolution should be subtle (1-2 traits max)
- Maintain aesthetic coherence
- Rarer traits should change less frequently

Available trait options:
- body_color: brown, tan, beige, gray, golden, silver, copper, bronze, blue, purple, green, pink, rainbow, galaxy, holographic, crystal
- face_expression: happy, neutral, curious, sleepy, excited, mischievous, wise, cool, surprised, laughing, winking, zen, enlightened, cosmic, legendary, divine
- accessory: none, simple_hat, bandana, bow, sunglasses, crown, headphones, monocle, laser_eyes, halo, horns, wizard_hat, golden_crown, diamond_chain, jetpack, wings
- pattern: solid, spots, stripes, gradient, swirls, stars, hearts, diamonds, fractals, nebula, lightning, flames, aurora, quantum, cosmic_dust, void
- background: white, blue_sky, green_grass, sunset, forest, beach, mountains, city, space, underwater, volcano, aurora, multiverse, black_hole, dimension_rift, heaven
- special: none, sparkles, glow, shadow, aura, particles, energy, transcendent, godlike, mythical

Rarity levels (from common to legendary):
- common (60% chance): Basic traits
- uncommon (25% chance): Special traits
- rare (10% chance): Unique traits
- legendary (5% chance): Ultra-rare traits

Respond with a JSON object indicating which traits to change:
{{
  "changes": [
    {{
      "category": "body_color",
      "new_value": "golden",
      "new_rarity": "uncommon",
      "reason": "Subtle shift to warmer tone"
    }}
  ],
  "evolution_story": "Your monkey is maturing, developing a golden sheen..."
}}

Keep changes minimal (0-2 traits). Consider the monkey's current aesthetic."""
    
    def _parse_ai_response(self, response_text: str) -> dict:
        """Parse Claude's response"""
        try:
            # Extract JSON from response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"⚠️  Failed to parse AI response: {e}")
            return {"changes": [], "evolution_story": "No changes today."}
    
    def _apply_evolution(self, dna: MonkeyDNA, decision: dict) -> MonkeyDNA:
        """Apply AI-decided evolution"""
        from src.genetics import Trait, Rarity
        
        # Copy current traits
        new_traits = {cat: trait.model_copy() for cat, trait in dna.traits.items()}
        mutations = 0
        
        # Apply changes
        for change in decision.get("changes", []):
            try:
                category = TraitCategory(change["category"])
                new_value = change["new_value"]
                new_rarity = Rarity(change["new_rarity"])
                
                # Create new trait
                new_traits[category] = Trait(
                    category=category,
                    value=new_value,
                    rarity=new_rarity
                )
                mutations += 1
                
            except Exception as e:
                print(f"⚠️  Failed to apply change: {e}")
        
        # Create evolved DNA
        evolved = MonkeyDNA(
            generation=dna.generation,
            parent_id=dna.parent_id,
            traits=new_traits,
            mutation_count=dna.mutation_count + mutations,
            birth_timestamp=dna.birth_timestamp
        )
        
        return evolved
    
    def generate_evolution_story(self, old_dna: MonkeyDNA, new_dna: MonkeyDNA) -> str:
        """Generate a story about the evolution"""
        
        changes = []
        for category in TraitCategory:
            old_trait = old_dna.traits[category]
            new_trait = new_dna.traits[category]
            
            if old_trait.value != new_trait.value:
                changes.append(f"{category.value}: {old_trait.value} → {new_trait.value}")
        
        if not changes:
            return "Your monkey rested today. No visible changes."
        
        prompt = f"""Generate a short, whimsical story (2-3 sentences) about a monkey's evolution.

Changes that occurred:
{chr(10).join(changes)}

Make it fun and engaging, like a Tamagotchi update message."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except:
            return f"Your monkey evolved! Changes: {', '.join(changes)}"


def main():
    """Test evolution agent"""
    from src.genetics import GeneticsEngine
    
    print("🧬 ForkMonkey Evolution Agent Test\n")
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set. Set it in .env file.")
        print("   Testing with random evolution instead...\n")
        
        dna = GeneticsEngine.generate_random_dna()
        evolved = GeneticsEngine.evolve(dna, evolution_strength=0.2)
        
        print("Original traits:")
        for cat, trait in dna.traits.items():
            print(f"  {cat.value}: {trait.value}")
        
        print("\nEvolved traits:")
        for cat, trait in evolved.traits.items():
            if trait.value != dna.traits[cat].value:
                print(f"  {cat.value}: {trait.value} (CHANGED)")
            else:
                print(f"  {cat.value}: {trait.value}")
        
        return
    
    # Test with AI
    agent = EvolutionAgent()
    
    print("1. Generating random monkey...")
    dna = GeneticsEngine.generate_random_dna()
    print("   Current traits:")
    for cat, trait in dna.traits.items():
        print(f"     {cat.value}: {trait.value} ({trait.rarity.value})")
    
    print("\n2. Evolving with AI...")
    evolved = agent.evolve_with_ai(dna, days_passed=1)
    
    print("   Evolved traits:")
    for cat, trait in evolved.traits.items():
        if trait.value != dna.traits[cat].value:
            print(f"     {cat.value}: {trait.value} ({trait.rarity.value}) ⭐ CHANGED")
        else:
            print(f"     {cat.value}: {trait.value} ({trait.rarity.value})")
    
    print(f"\n   Mutations: {evolved.mutation_count}")
    
    print("\n3. Generating evolution story...")
    story = agent.generate_evolution_story(dna, evolved)
    print(f"   {story}")
    
    print("\n✅ Evolution agent working!")


if __name__ == "__main__":
    main()
