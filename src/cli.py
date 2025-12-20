"""
ForkMonkey CLI

Command-line interface for managing your monkey.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.genetics import GeneticsEngine, MonkeyDNA
from src.storage import MonkeyStorage
from src.visualizer import MonkeyVisualizer
from src.evolution import EvolutionAgent

console = Console()


@click.group()
def cli():
    """🐵 ForkMonkey - Your AI-powered digital pet on GitHub"""
    pass


@cli.command()
@click.option('--from-fork', is_flag=True, help='Initialize from parent repo (for forks)')
@click.option('--force', '-f', is_flag=True, help='Force overwrite without confirmation (for CI)')
def init(from_fork, force):
    """Initialize a new monkey"""
    console.print("\n🐵 [bold cyan]Initializing ForkMonkey...[/bold cyan]\n")
    
    storage = MonkeyStorage()
    
    # Check if monkey already exists
    existing_dna = storage.load_dna()
    if existing_dna:
        console.print("[yellow]⚠️  Monkey already exists![/yellow]")
        console.print(f"   DNA Hash: {existing_dna.dna_hash}")
        console.print(f"   Generation: {existing_dna.generation}")
        
        # In fork mode or with --force, auto-confirm to allow CI to proceed
        if not force and not from_fork:
            if not click.confirm("\nOverwrite existing monkey?"):
                console.print("[red]Cancelled.[/red]")
                return
        else:
            console.print("[cyan]   Auto-confirming for fork/CI mode...[/cyan]")
    
    # Initialize DNA
    if from_fork:
        console.print("[cyan]🍴 Checking for parent repository...[/cyan]")
        dna = storage.initialize_from_parent()
        
        if not dna:
            console.print("[yellow]⚠️  Not a fork or parent DNA not found[/yellow]")
            console.print("[cyan]   Generating new monkey instead...[/cyan]")
            dna = GeneticsEngine.generate_random_dna()
    else:
        console.print("[cyan]🎲 Generating random monkey...[/cyan]")
        dna = GeneticsEngine.generate_random_dna()
    
    # Save DNA
    storage.save_dna_locally(dna)
    storage.save_stats(dna, age_days=0)
    storage.save_history_entry(dna, "🎉 Your monkey was born!")
    
    # Generate initial visualization
    svg = MonkeyVisualizer.generate_svg(dna)
    svg_file = Path("monkey_data/monkey.svg")
    svg_file.write_text(svg)
    
    # Display info
    console.print("\n[bold green]✅ Monkey initialized![/bold green]\n")
    
    table = Table(title="Your Monkey")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("DNA Hash", dna.dna_hash)
    table.add_row("Generation", str(dna.generation))
    table.add_row("Rarity Score", f"{dna.get_rarity_score():.1f}/100")
    
    console.print(table)
    
    console.print("\n[bold]Traits:[/bold]")
    for cat, trait in dna.traits.items():
        console.print(f"  • {cat.value}: [green]{trait.value}[/green] ([yellow]{trait.rarity.value}[/yellow])")
    
    console.print(f"\n[dim]SVG saved to: {svg_file}[/dim]")


@cli.command()
@click.option('--ai', is_flag=True, help='Use AI-powered evolution')
@click.option('--strength', default=0.1, help='Evolution strength (0-1)')
def evolve(ai, strength):
    """Evolve your monkey"""
    console.print("\n🧬 [bold cyan]Evolving monkey...[/bold cyan]\n")
    
    storage = MonkeyStorage()
    
    # Load current DNA
    dna = storage.load_dna()
    if not dna:
        console.print("[red]❌ No monkey found! Run 'init' first.[/red]")
        return
    
    console.print(f"Current DNA: {dna.dna_hash}")
    console.print(f"Mutations so far: {dna.mutation_count}")
    
    # Evolve
    if ai and os.getenv("ANTHROPIC_API_KEY"):
        console.print("\n[cyan]🤖 Using AI-powered evolution...[/cyan]")
        agent = EvolutionAgent()
        evolved_dna = agent.evolve_with_ai(dna, days_passed=1)
        story = agent.generate_evolution_story(dna, evolved_dna)
    else:
        if ai:
            console.print("\n[yellow]⚠️  ANTHROPIC_API_KEY not set, using random evolution[/yellow]")
        console.print(f"\n[cyan]🎲 Using random evolution (strength: {strength})...[/cyan]")
        evolved_dna = GeneticsEngine.evolve(dna, evolution_strength=strength)
        story = "Your monkey evolved randomly!"
    
    # Show changes
    console.print("\n[bold]Changes:[/bold]")
    changes = []
    for cat in dna.traits.keys():
        old_trait = dna.traits[cat]
        new_trait = evolved_dna.traits[cat]
        
        if old_trait.value != new_trait.value:
            console.print(f"  • {cat.value}: [red]{old_trait.value}[/red] → [green]{new_trait.value}[/green]")
            changes.append(cat.value)
        else:
            console.print(f"  • {cat.value}: {old_trait.value} (unchanged)")
    
    if not changes:
        console.print("  [dim]No changes today[/dim]")
    
    # Save
    storage.save_dna_locally(evolved_dna)
    storage.save_stats(evolved_dna, age_days=0)  # TODO: calculate actual age
    storage.save_history_entry(evolved_dna, story)
    
    # Generate new visualization
    svg = MonkeyVisualizer.generate_svg(evolved_dna)
    svg_file = Path("monkey_data/monkey.svg")
    svg_file.write_text(svg)
    
    console.print(f"\n[bold green]✅ Evolution complete![/bold green]")
    console.print(f"New DNA: {evolved_dna.dna_hash}")
    console.print(f"Total mutations: {evolved_dna.mutation_count}")
    console.print(f"\n[italic]{story}[/italic]")


@cli.command()
def show():
    """Show current monkey stats"""
    console.print("\n🐵 [bold cyan]Your Monkey[/bold cyan]\n")
    
    storage = MonkeyStorage()
    dna = storage.load_dna()
    
    if not dna:
        console.print("[red]❌ No monkey found! Run 'init' first.[/red]")
        return
    
    # Stats table
    table = Table(title="Monkey Stats")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("DNA Hash", dna.dna_hash)
    table.add_row("Generation", str(dna.generation))
    table.add_row("Parent", dna.parent_id or "None (Genesis)")
    table.add_row("Mutations", str(dna.mutation_count))
    table.add_row("Rarity Score", f"{dna.get_rarity_score():.1f}/100")
    
    console.print(table)
    
    # Traits table
    traits_table = Table(title="Traits")
    traits_table.add_column("Category", style="cyan")
    traits_table.add_column("Value", style="green")
    traits_table.add_column("Rarity", style="yellow")
    
    for cat, trait in dna.traits.items():
        traits_table.add_row(cat.value, trait.value, trait.rarity.value)
    
    console.print("\n")
    console.print(traits_table)


@cli.command()
@click.option('--limit', default=10, help='Number of entries to show')
def history(limit):
    """Show evolution history"""
    console.print("\n📜 [bold cyan]Evolution History[/bold cyan]\n")
    
    storage = MonkeyStorage()
    entries = storage.get_history()
    
    if not entries:
        console.print("[yellow]No history yet.[/yellow]")
        return
    
    # Show recent entries
    for entry in entries[-limit:]:
        timestamp = entry.get("timestamp", "Unknown")
        story = entry.get("story", "")
        mutations = entry.get("mutation_count", 0)
        rarity = entry.get("rarity_score", 0)
        
        panel = Panel(
            f"[dim]{timestamp}[/dim]\n\n{story}\n\n"
            f"Mutations: {mutations} | Rarity: {rarity:.1f}/100",
            title=f"Generation {entry.get('generation', '?')}",
            border_style="cyan"
        )
        console.print(panel)
        console.print()


@cli.command()
def visualize():
    """Generate and save monkey visualization"""
    console.print("\n🎨 [bold cyan]Generating visualization...[/bold cyan]\n")
    
    storage = MonkeyStorage()
    dna = storage.load_dna()
    
    if not dna:
        console.print("[red]❌ No monkey found! Run 'init' first.[/red]")
        return
    
    # Generate SVG
    svg = MonkeyVisualizer.generate_svg(dna)
    svg_file = Path("monkey_data/monkey.svg")
    svg_file.write_text(svg)
    
    console.print(f"[green]✅ SVG saved to: {svg_file}[/green]")
    
    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(str(svg_file.absolute()))
        console.print("[dim]Opening in browser...[/dim]")
    except:
        pass


@cli.command()
def update_readme():
    """Update README with current monkey"""
    console.print("\n📝 [bold cyan]Updating README...[/bold cyan]\n")
    
    storage = MonkeyStorage()
    dna = storage.load_dna()
    
    if not dna:
        console.print("[red]❌ No monkey found! Run 'init' first.[/red]")
        return
    
    # Read current README
    readme_file = Path("README.md")
    if not readme_file.exists():
        console.print("[red]❌ README.md not found![/red]")
        return
    
    readme = readme_file.read_text()
    
    # Generate SVG and save it
    svg = MonkeyVisualizer.generate_svg(dna, width=400, height=400)
    svg_file = Path("monkey_data/monkey.svg")
    svg_file.write_text(svg)
    
    # Update monkey display section with image reference
    monkey_section = '''<!-- MONKEY_DISPLAY_START -->
<div align="center">

![Your Monkey](monkey_data/monkey.svg)

</div>
<!-- MONKEY_DISPLAY_END -->'''
    
    # Replace section
    import re
    pattern = r'<!-- MONKEY_DISPLAY_START -->.*?<!-- MONKEY_DISPLAY_END -->'
    readme = re.sub(pattern, monkey_section, readme, flags=re.DOTALL)
    
    # Update stats section
    history = storage.get_history()
    age_days = len(history)
    
    stats_section = f'''<!-- MONKEY_STATS_START -->
- **Generation**: {dna.generation}
- **Age**: {age_days} days
- **Mutations**: {dna.mutation_count}
- **Rarity Score**: {dna.get_rarity_score():.1f}/100
<!-- MONKEY_STATS_END -->'''
    
    pattern = r'<!-- MONKEY_STATS_START -->.*?<!-- MONKEY_STATS_END -->'
    readme = re.sub(pattern, stats_section, readme, flags=re.DOTALL)
    
    # Save
    readme_file.write_text(readme)
    
    console.print("[green]✅ README updated![/green]")


if __name__ == "__main__":
    cli()
