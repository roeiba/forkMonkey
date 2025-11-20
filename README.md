# 🐵 ForkMonkey

> **Your digital pet that lives forever on GitHub and evolves with AI**

ForkMonkey is an autonomous, self-evolving digital collectible that combines:
- 🎮 **Tamagotchi-style** digital pets
- 🎨 **CryptoKitties** genetic breeding
- 🐵 **Bored Ape** collectible traits
- 🤖 **AI-powered** daily evolution

## What is ForkMonkey?

Each ForkMonkey is a unique digital creature that:
- **Lives on GitHub** as a repository
- **Evolves daily** through AI-powered mutations
- **Changes appearance** based on its DNA
- **Breeds through forks** - create new generations
- **Grows a family tree** across the GitHub network

### The Magic

1. **Your Monkey**: The owner of the GitHub repo owns the monkey
2. **Fork to Breed**: Fork the repo to create a child monkey with inherited + mutated traits
3. **AI Evolution**: Every day, an AI agent slightly modifies your monkey's appearance
4. **Secret DNA**: Monkey traits are stored as GitHub Secrets (only you can see them)
5. **Public Art**: The monkey's visual representation updates daily in the README
6. **Network Effect**: All monkeys form a family tree across GitHub

## How It Works

```
Day 1: 🐵 Born with random DNA
Day 2: 🐵 AI mutates color slightly
Day 3: 🐵 Grows a hat
Day 4: 🐵 Expression changes
...
Day 365: 🐵 Completely unique creature

Fork it: 👶 Child inherits 50% parent DNA + 50% random + daily mutations
```

## Features

### 🧬 Genetics System
- **DNA Traits**: Color, size, accessories, expressions, patterns
- **Inheritance**: Children inherit traits from parents with mutations
- **Rarity System**: Some traits are rarer than others
- **Generation Tracking**: Know your monkey's lineage

### 🤖 AI Evolution
- **Daily Mutations**: Claude AI subtly evolves your monkey
- **Smart Changes**: AI understands aesthetics and makes coherent changes
- **Personality Development**: Monkeys develop unique personalities over time

### 🎨 Visual System
- **SVG Generation**: Procedurally generated monkey art
- **Real-time Updates**: README shows current monkey state
- **History Tracking**: See how your monkey evolved over time

### 🌳 Network
- **Family Trees**: Visualize monkey genealogy
- **Rarity Rankings**: See the rarest monkeys in the network
- **Discovery**: Find and follow other monkeys

## Quick Start

### 1. Fork This Repo
Click "Fork" to create your own monkey!

### 2. Set Up Secrets
Go to Settings → Secrets and variables → Actions → New repository secret:

```
ANTHROPIC_API_KEY: your_claude_api_key
```

### 3. Enable GitHub Actions
Go to Actions tab → Enable workflows

### 4. Watch Your Monkey Grow!
Every day at midnight UTC, your monkey evolves automatically.

### 5. View Your Monkey (Web Interface)
```bash
# Start the beautiful web interface
./start_web.sh

# Or manually:
python web/serve.py
```

Then open http://localhost:8000/web/index.html in your browser!

## Your Monkey

<!-- MONKEY_DISPLAY_START -->
<div align="center">

<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">

<defs>
    <!-- Rainbow gradient -->
    <linearGradient id="rainbow-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#FF0000;stop-opacity:1" />
        <stop offset="16%" style="stop-color:#FF7F00;stop-opacity:1" />
        <stop offset="33%" style="stop-color:#FFFF00;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#00FF00;stop-opacity:1" />
        <stop offset="66%" style="stop-color:#0000FF;stop-opacity:1" />
        <stop offset="83%" style="stop-color:#4B0082;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#9400D3;stop-opacity:1" />
    </linearGradient>
    
    <!-- Galaxy gradient -->
    <radialGradient id="galaxy-gradient">
        <stop offset="0%" style="stop-color:#9400D3;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#4B0082;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#000033;stop-opacity:1" />
    </radialGradient>
    
    <!-- Holographic gradient -->
    <linearGradient id="holo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#FF00FF;stop-opacity:0.8" />
        <stop offset="50%" style="stop-color:#00FFFF;stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:#FFFF00;stop-opacity:0.8" />
    </linearGradient>
    
    <!-- Multiverse gradient -->
    <radialGradient id="multiverse-gradient">
        <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
        <stop offset="33%" style="stop-color:#FF00FF;stop-opacity:1" />
        <stop offset="66%" style="stop-color:#00FFFF;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
    </radialGradient>
    
    <!-- Dimension rift gradient -->
    <linearGradient id="rift-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#000000;stop-opacity:1" />
        <stop offset="25%" style="stop-color:#9400D3;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#00FFFF;stop-opacity:1" />
        <stop offset="75%" style="stop-color:#9400D3;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
    </linearGradient>
</defs>

<rect width="300" height="300" fill="#F0E68C"/>
<circle cx="150" cy="150" r="120" fill="#D2B48C" stroke="#000" stroke-width="3"/>
<circle cx="60" cy="120" r="40" fill="#D2B48C" stroke="#000" stroke-width="2"/>
<circle cx="240" cy="120" r="40" fill="#D2B48C" stroke="#000" stroke-width="2"/>
<circle cx="60" cy="120" r="25" fill="#FFB6C1"/>
<circle cx="240" cy="120" r="25" fill="#FFB6C1"/>
<ellipse cx="150" cy="170" rx="80" ry="70" fill="#F5DEB3"/>
<ellipse cx="110" cy="140" rx="15" ry="20" fill="#000"/>
<line x1="175" y1="140" x2="205" y2="140" stroke="#000" stroke-width="3"/>
<ellipse cx="150" cy="170" rx="12" ry="8" fill="#8B4513"/>
<line x1="130" y1="195" x2="170" y2="195" stroke="#000" stroke-width="2"/>
<rect x="100" y="0" width="100" height="20" fill="#8B0000" stroke="#000" stroke-width="2"/>
<text x="50" y="50" font-size="30" fill="gold">✨</text>
<text x="250" y="50" font-size="30" fill="gold">✨</text>
<text x="50" y="250" font-size="30" fill="gold">✨</text>
<text x="250" y="250" font-size="30" fill="gold">✨</text>
</svg>

</div>
<!-- MONKEY_DISPLAY_END -->

## Monkey Stats

<!-- MONKEY_STATS_START -->
- **Generation**: 1
- **Age**: 5 days
- **Mutations**: 2
- **Rarity Score**: 20.0/100
<!-- MONKEY_STATS_END -->

## Family Tree

<!-- MONKEY_FAMILY_START -->
*Fork this repo to create children!*
<!-- MONKEY_FAMILY_END -->

## Development

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize your monkey
python src/cli.py init

# View in web interface
./start_web.sh

# Evolve monkey manually
python src/cli.py evolve --ai

# Show monkey stats
python src/cli.py show

# Run tests
pytest tests/
```

### Project Structure

```
forkMonkey/
├── .github/
│   └── workflows/
│       ├── daily-evolution.yml    # Daily AI evolution
│       └── on-fork.yml            # Initialize child monkey
├── src/
│   ├── genetics.py                # DNA and trait system
│   ├── evolution.py               # AI-powered evolution
│   ├── visualizer.py              # SVG monkey generator
│   ├── storage.py                 # Data persistence
│   └── cli.py                     # Command-line interface
├── web/
│   ├── index.html                 # Web interface
│   ├── style.css                  # Modern blocky design
│   ├── script.js                  # Interactive features
│   └── serve.py                   # Local web server
├── tests/                         # Comprehensive tests
├── monkey_data/
│   ├── dna.json                   # Monkey DNA
│   ├── history.json               # Evolution history
│   ├── stats.json                 # Monkey statistics
│   └── monkey.svg                 # Visual representation
└── README.md                      # This file (auto-updated)
```

## How to Breed

1. **Fork this repository** - Creates a child monkey
2. **Child inherits traits** - 50% from parent, 50% random
3. **Set up your API key** - Add ANTHROPIC_API_KEY secret
4. **Enable Actions** - Let your child evolve
5. **Watch it grow** - Different from parent, but related

## Rarity System

Traits have different rarity levels:
- **Common** (60%): Basic colors, simple patterns
- **Uncommon** (25%): Special colors, accessories
- **Rare** (10%): Unique patterns, special features
- **Legendary** (5%): Ultra-rare combinations

## Network Stats

<!-- NETWORK_STATS_START -->
- **Total Monkeys**: Calculating...
- **Generations**: Calculating...
- **Rarest Trait**: Calculating...
<!-- NETWORK_STATS_END -->

## API

### View Your Monkey's DNA
```bash
# DNA is stored in GitHub Secrets (private)
# Only the owner can see the full DNA
```

### Get Monkey Stats
```bash
curl https://api.github.com/repos/{owner}/forkMonkey/contents/monkey_data/stats.json
```

### View Family Tree
```bash
python src/cli.py family-tree
```

## Contributing

Want to improve ForkMonkey?
1. Fork this repo
2. Create a feature branch
3. Make your changes
4. Submit a PR to the main ForkMonkey repo

## Inspiration

- 🎮 **Tamagotchi**: Virtual pets that need care
- 🐱 **CryptoKitties**: Genetic breeding on blockchain
- 🐵 **Bored Ape Yacht Club**: Collectible traits
- 🌱 **SeedGPT**: AI-powered autonomous growth

## License

MIT License - Fork, breed, and evolve freely!

---

**Your monkey is unique. Your monkey is alive. Your monkey is forever on GitHub.** 🐵✨
