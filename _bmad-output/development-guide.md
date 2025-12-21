# ForkMonkey - Development Guide

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.11+ | Core runtime |
| pip | Latest | Package management |
| Git | 2.0+ | Version control |
| GitHub Account | — | Fork/deploy |

### Optional

| Requirement | Purpose |
|-------------|---------|
| Anthropic API Key | Claude AI evolution |
| Docker | Container deployment |
| Google Cloud SDK | Cloud Run deployment |

## Quick Start

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/roeiba/forkMonkey.git
cd forkMonkey

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize a Monkey

```bash
# Create your first monkey
python src/cli.py init

# Output:
# ✅ Monkey initialized!
# DNA Hash: 576a6a3c176765b4
# Generation: 1
# Rarity Score: 26.7/100
```

### 3. View Your Monkey

```bash
# Show stats
python src/cli.py show

# View evolution history
python src/cli.py history

# Generate and open SVG
python src/cli.py visualize
```

### 4. Start Web Interface

```bash
# Option 1: Use the start script
./start_web.sh

# Option 2: Manual
cd web
python serve.py
# Opens http://localhost:8000
```

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize new monkey | `python src/cli.py init` |
| `init --from-fork` | Initialize from parent DNA | `python src/cli.py init --from-fork` |
| `evolve` | Random evolution | `python src/cli.py evolve --strength 0.2` |
| `evolve --ai` | AI-powered evolution | `python src/cli.py evolve --ai` |
| `show` | Display monkey stats | `python src/cli.py show` |
| `history` | View evolution history | `python src/cli.py history` |
| `visualize` | Generate & view SVG | `python src/cli.py visualize` |
| `update-readme` | Update README with stats | `python src/cli.py update-readme` |
| `share` | Generate shareable tweet | `python src/cli.py share` |

## Environment Variables

Create a `.env` file in the project root:

```bash
# AI Evolution (choose one or both)
ANTHROPIC_API_KEY=sk-ant-...          # For Claude
OPENAI_API_KEY=sk-...                  # For GPT-4

# GitHub Integration
GITHUB_TOKEN=ghp_...                   # Personal access token
GITHUB_REPOSITORY=username/forkMonkey # Your repo

# AI Provider Selection
AI_PROVIDER=claude                     # or 'openai'
```

## Testing

### Run All Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_genetics.py -v
```

### Test Structure

| File | Tests | Coverage |
|------|-------|----------|
| `test_genetics.py` | 12 | DNA, traits, breeding, evolution |
| `test_storage.py` | 6 | Persistence, loading, history |
| `test_visualizer.py` | 6 | SVG generation, traits |
| `test_scan_community.py` | — | Community scanning |
| `test_e2e_fork.py` | — | End-to-end fork flow |

### Expected Output

```
======================== 24 passed in 0.09s ========================
```

## Development Workflows

### Adding a New Trait

1. Edit `src/genetics.py`:
```python
TRAIT_POOLS = {
    "new_category": {
        "common": ["value1", "value2"],
        "uncommon": ["value3"],
        "rare": ["value4"],
        "legendary": ["value5"]
    }
}
```

2. Update `src/visualizer.py` to render the new trait

3. Add tests in `tests/test_genetics.py`

### Modifying Evolution Logic

1. Edit `src/evolution.py` for AI prompts
2. Edit `src/genetics.py` for mutation logic
3. Test with: `python src/cli.py evolve --ai`

### Updating the Dashboard

1. Edit `web/index.html` for structure
2. Edit `web/style.css` for styling
3. Edit `web/script.js` for behavior
4. Test locally: `cd web && python serve.py`

## Server Development

### Local API Server

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
# Runs on http://localhost:5000
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/adopt/start` | POST | Start adoption flow |
| `/api/adopt/oauth/callback` | GET | OAuth callback |
| `/api/stats` | GET | Community stats |

## Deployment

### GitHub Pages (Frontend)

Automatic via `.github/workflows/deploy-pages.yml`:
1. Push to `main` branch
2. Workflow copies `web/` + `monkey_data/` to Pages
3. Available at `https://username.github.io/forkMonkey/`

### Cloud Run (API)

```bash
# Manual trigger
gcloud builds submit --config=cloudbuild.yaml

# Or use GitHub Actions
# .github/workflows/deploy-backend.yml
```

### Docker Local Build

```bash
cd server
docker build -t forkmonkey-api .
docker run -p 5000:5000 forkmonkey-api
```

## Project Structure Details

### Core Modules

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| `genetics.py` | DNA engine | `DNA`, `generate_dna()`, `breed()`, `mutate()` |
| `evolution.py` | AI evolution | `AIEvolver`, `evolve_with_ai()` |
| `visualizer.py` | SVG art | `MonkeyVisualizer`, `generate_svg()` |
| `storage.py` | Persistence | `save_dna()`, `load_dna()`, `get_history()` |
| `achievements.py` | Achievements | `check_achievements()`, `ACHIEVEMENTS` |
| `cli.py` | CLI interface | Click commands |

### Data Files

| File | Location | Purpose |
|------|----------|---------|
| `dna.json` | `monkey_data/` | Current DNA |
| `stats.json` | `monkey_data/` | Age, generation, mutations |
| `history.json` | `monkey_data/` | Evolution log |
| `monkey.svg` | `monkey_data/` | Current visualization |

## Debugging

### Common Issues

**"Failed to load monkey data"**
```bash
# Ensure monkey is initialized
python src/cli.py init
```

**"AI evolution failed"**
```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Falls back to random evolution automatically
```

**"SVG not displaying"**
```bash
# Regenerate SVG
python src/cli.py visualize
```

### Logging

Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance

| Operation | Time |
|-----------|------|
| DNA generation | ~1ms |
| Evolution (random) | ~2ms |
| SVG generation | ~5ms |
| AI evolution | 2-5s |
| Full test suite | ~0.1s |

## Code Style

- **Formatting**: Black (default settings)
- **Linting**: Flake8
- **Type Hints**: Yes (Pydantic models)
- **Docstrings**: Google style

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/
```

---

*Generated by BMad Document Project workflow*

