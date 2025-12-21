# ForkMonkey - Source Tree Analysis

## Repository Structure

```
forkMonkey/
│
├── 📁 src/                          # Core Python Library (CLI Part)
│   ├── __init__.py                  # Package init
│   ├── cli.py                       # 🎯 CLI entry point (Click-based)
│   ├── genetics.py                  # DNA generation, traits, breeding, evolution
│   ├── evolution.py                 # AI-powered intelligent mutations (Claude)
│   ├── visualizer.py                # SVG monkey art generation
│   ├── storage.py                   # Data persistence, GitHub integration
│   ├── achievements.py              # Achievement system (12 achievements)
│   └── scan_community.py            # Community scanning for leaderboard
│
├── 📁 server/                       # Flask API Backend (API Part)
│   ├── app.py                       # 🎯 Flask application entry point
│   ├── github_service.py            # GitHub App OAuth, repo creation
│   ├── requirements.txt             # API-specific dependencies
│   ├── Dockerfile                   # Container deployment
│   └── GITHUB_APP_SETUP.md          # OAuth setup guide
│
├── 📁 web/                          # Static Frontend (Dashboard Part)
│   ├── index.html                   # 🎯 Main dashboard page
│   ├── script.js                    # Frontend logic, API calls
│   ├── style.css                    # Blocky/retro design system
│   ├── serve.py                     # Local development server
│   ├── community_data.json          # Community monkey data
│   ├── family_tree.json             # Fork relationships
│   ├── leaderboard.json             # Rarity rankings
│   └── network_stats.json           # Network statistics
│
├── 📁 tests/                        # Test Suite (24 tests)
│   ├── test_genetics.py             # Genetics system tests (12 tests)
│   ├── test_storage.py              # Storage tests (6 tests)
│   ├── test_visualizer.py           # Visualizer tests (6 tests)
│   ├── test_scan_community.py       # Community scanning tests
│   └── test_e2e_fork.py             # End-to-end fork flow tests
│
├── 📁 .github/workflows/            # GitHub Actions Automation
│   ├── daily-evolution.yml          # ⏰ Daily midnight evolution
│   ├── on-create.yml                # 🍴 Fork initialization
│   ├── deploy-pages.yml             # 🌐 GitHub Pages deployment
│   ├── deploy-backend.yml           # ☁️ Cloud Run deployment
│   └── community_scan.yml           # 📊 Community data update
│
├── 📁 monkey_data/                  # Runtime Data (Git-tracked)
│   ├── dna.json                     # Current monkey DNA
│   ├── stats.json                   # Monkey statistics
│   ├── history.json                 # Evolution history
│   └── monkey.svg                   # Current visual representation
│
├── 📁 monkey_evolution/             # Evolution History Snapshots
│   ├── YYYY-MM-DD_HH-MM_monkey.svg  # Timestamped evolution snapshots
│   └── evolution.gif                # Animated evolution history
│
├── 📁 promotion/                    # Marketing Materials
│   ├── MARKETING_PLAN.md            # Go-to-market strategy
│   ├── LAUNCH_CHECKLIST.md          # Launch preparation
│   ├── IMPLEMENTATION_CHECKLIST.md  # Feature implementation tracking
│   ├── VIRAL_CTAs.md                # Call-to-action templates
│   ├── SALES_PLAYBOOK.md            # Sales strategy
│   ├── reddit/                      # Reddit post templates (12 subreddits)
│   ├── twitter/                     # Twitter thread templates
│   ├── linkedin/                    # LinkedIn post templates
│   ├── hackernews/                  # HackerNews Show HN template
│   └── press/                       # Press kit
│
├── 📁 hooks/                        # Git Hooks
│   ├── install.sh                   # Hook installer
│   └── pre-push                     # Pre-push validation
│
├── 📁 creds/                        # Credentials (gitignored)
│   └── gcp-key.json                 # GCP service account
│
├── 📄 requirements.txt              # Python dependencies (root)
├── 📄 README.md                     # Main project README
├── 📄 DEVELOPMENT.md                # Developer guide
├── 📄 cloudbuild.yaml               # Google Cloud Build config
├── 📄 start_web.sh                  # Web server starter script
├── 📄 create_animation.py           # Evolution GIF generator
├── 📄 extract_history.py            # History extraction utility
└── 📄 regenerate_svgs.py            # SVG regeneration utility
```

## Critical Directories by Part

### CLI Part (`src/`)

| File | Purpose | Key Functions |
|------|---------|---------------|
| `cli.py` | Entry point | `init`, `evolve`, `show`, `history`, `visualize`, `update-readme` |
| `genetics.py` | Core logic | `DNA`, `generate_dna()`, `breed()`, `mutate()`, `calculate_rarity()` |
| `evolution.py` | AI integration | `AIEvolver`, `evolve_with_ai()` |
| `visualizer.py` | SVG generation | `MonkeyVisualizer`, `generate_svg()` |
| `storage.py` | Persistence | `save_dna()`, `load_dna()`, `fetch_parent_dna()` |

### API Part (`server/`)

| File | Purpose | Key Endpoints |
|------|---------|---------------|
| `app.py` | Flask app | `/api/adopt/*`, `/api/health`, `/api/stats` |
| `github_service.py` | GitHub integration | OAuth flow, repo creation, Actions enablement |

### Dashboard Part (`web/`)

| File | Purpose | Key Features |
|------|---------|---------------|
| `index.html` | Main page | Monkey display, stats, leaderboard, family tree |
| `script.js` | Logic | Data loading, particle effects, interactions |
| `style.css` | Design | Blocky/retro theme, NES.css integration |

## Integration Points

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions                                │
│  (daily-evolution.yml, deploy-pages.yml, community_scan.yml)        │
└────────────┬─────────────────────────────────────────┬──────────────┘
             │                                         │
             ▼                                         ▼
┌────────────────────────┐                ┌────────────────────────┐
│     src/ (CLI)         │                │    web/ (Dashboard)    │
│  - Genetics engine     │                │  - Leaderboard         │
│  - Evolution logic     │                │  - Family tree         │
│  - SVG generation      │                │  - Community view      │
│  - CLI commands        │                │  - Monkey display      │
└────────────┬───────────┘                └────────────┬───────────┘
             │                                         │
             │    ┌─────────────────────────┐         │
             └───▶│   monkey_data/          │◀────────┘
                  │  (dna.json, stats.json) │
                  └─────────────────────────┘
                              ▲
                              │
             ┌────────────────┴────────────────┐
             │        server/ (API)            │
             │  - GitHub OAuth                 │
             │  - Adoption flow                │
             │  - Repo creation                │
             └─────────────────────────────────┘
```

## Data Flow

1. **Fork/Adopt** → `server/` handles OAuth → creates repo with `monkey_data/`
2. **Daily Evolution** → GitHub Actions runs `src/cli.py evolve --ai`
3. **Visualization** → `src/visualizer.py` generates `monkey_data/monkey.svg`
4. **Deployment** → GitHub Pages serves `web/` with `monkey_data/` copied in
5. **Community** → `src/scan_community.py` updates `web/*.json` files

---

*Generated by BMad Document Project workflow*

