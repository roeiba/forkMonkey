# ForkMonkey - Documentation Index

> 🐵 **Your Digital Pet That Lives Forever on GitHub**
>
> *AI-powered evolution • Genetic breeding • Community leaderboard*

---

## Project Overview

| Attribute | Value |
|-----------|-------|
| **Type** | Multi-part (CLI + API + Dashboard) |
| **Primary Language** | Python 3.11 |
| **Architecture** | Event-Driven + Static Site Generation |
| **Status** | ✅ Production Ready |

### Quick Reference

| Part | Path | Type | Purpose |
|------|------|------|---------|
| **cli** | `src/` | CLI/Library | Core genetics, evolution, visualization |
| **api** | `server/` | Backend (Flask) | GitHub OAuth, adoption flow |
| **dashboard** | `web/` | Static Frontend | Leaderboard, family tree, community |

---

## Generated Documentation

### Core Documentation

- [Project Overview](./project-overview.md) — Executive summary, features, tech stack
- [Architecture](./architecture.md) — System design, data flow, components
- [Source Tree Analysis](./source-tree-analysis.md) — Directory structure, critical files
- [Development Guide](./development-guide.md) — Setup, CLI, testing, deployment

### Additional Documentation _(To be generated)_

- [API Contracts](./api-contracts.md) _(To be generated)_
- [Data Models](./data-models.md) _(To be generated)_

---

## Existing Documentation

These files exist in the repository and provide additional context:

| Document | Path | Description |
|----------|------|-------------|
| **Main README** | [README.md](../README.md) | User-facing documentation, quick start |
| **Development Guide** | [DEVELOPMENT.md](../DEVELOPMENT.md) | Detailed dev guide with trait reference |
| **Web README** | [web/README.md](../web/README.md) | Dashboard design system, features |
| **GitHub App Setup** | [server/GITHUB_APP_SETUP.md](../server/GITHUB_APP_SETUP.md) | OAuth configuration guide |

### Marketing Materials (`promotion/`)

| Document | Purpose |
|----------|---------|
| [MARKETING_PLAN.md](../promotion/MARKETING_PLAN.md) | Go-to-market strategy |
| [LAUNCH_CHECKLIST.md](../promotion/LAUNCH_CHECKLIST.md) | Launch preparation |
| [IMPLEMENTATION_CHECKLIST.md](../promotion/IMPLEMENTATION_CHECKLIST.md) | Feature tracking |
| [VIRAL_CTAs.md](../promotion/VIRAL_CTAs.md) | Call-to-action templates |

---

## Getting Started

### For New Developers

1. Clone the repo: `git clone https://github.com/roeiba/forkMonkey.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize monkey: `python src/cli.py init`
4. View your monkey: `python src/cli.py show`

### For Users

1. **Fork** this repository
2. **Enable** GitHub Actions
3. **Run** the "Initialize New Monkey" workflow
4. **Watch** your monkey evolve daily!

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Core Logic | Python 3.11, Pydantic |
| CLI | Click, Rich |
| API | Flask, Flask-CORS, Gunicorn |
| Frontend | HTML5, CSS3, JavaScript |
| AI | Anthropic Claude, OpenAI GPT-4o |
| Visualization | CairoSVG, Pillow |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages, Google Cloud Run |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      GITHUB INFRASTRUCTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   GitHub Actions ──▶ GitHub Repos ──▶ GitHub Pages              │
│   (Daily Evolution)   (DNA Storage)   (Dashboard)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
         │                                         │
         ▼                                         ▼
┌─────────────────┐                     ┌─────────────────┐
│    src/ (CLI)   │                     │   web/ (Dashboard)
│  ┌───────────┐  │                     │  ┌───────────┐  │
│  │ genetics  │  │                     │  │Leaderboard│  │
│  │ evolution │  │                     │  │Family Tree│  │
│  │ visualizer│  │                     │  │ Community │  │
│  └───────────┘  │                     │  └───────────┘  │
└─────────────────┘                     └─────────────────┘
         │                                         │
         └────────────────┬────────────────────────┘
                          ▼
                  ┌───────────────┐
                  │  server/ (API)│
                  │  GitHub OAuth │
                  │  Adoption Flow│
                  └───────────────┘
```

---

## Entry Points

| Entry | Command | Purpose |
|-------|---------|---------|
| CLI | `python src/cli.py` | Development, testing |
| Web Server | `./start_web.sh` | Local dashboard |
| API Server | `python server/app.py` | OAuth flow |

---

## Key Files Quick Reference

| Purpose | File |
|---------|------|
| DNA Logic | `src/genetics.py` |
| AI Evolution | `src/evolution.py` |
| SVG Generation | `src/visualizer.py` |
| CLI Commands | `src/cli.py` |
| Flask API | `server/app.py` |
| Dashboard | `web/index.html` |
| Daily Workflow | `.github/workflows/daily-evolution.yml` |

---

## Scan Metadata

| Field | Value |
|-------|-------|
| Generated | 2025-12-21 |
| Scan Level | Quick |
| Mode | Initial Scan |
| Parts Documented | 3 (cli, api, dashboard) |
| Files Generated | 5 |

---

*Generated by BMad Document Project workflow v1.2.0*

