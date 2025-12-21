# ForkMonkey - Architecture Document

## System Overview

ForkMonkey is a distributed system leveraging GitHub's infrastructure as its backbone. The architecture follows a **serverless-first** approach where GitHub Actions provides compute, GitHub Pages provides hosting, and GitHub repositories serve as the data layer.

## Architecture Pattern

**Hybrid Architecture**: Event-Driven + Static Site Generation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GITHUB INFRASTRUCTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                │
│  │   GitHub     │     │   GitHub     │     │   GitHub     │                │
│  │   Actions    │────▶│   Repos      │────▶│   Pages      │                │
│  │   (Compute)  │     │   (Storage)  │     │   (Hosting)  │                │
│  └──────────────┘     └──────────────┘     └──────────────┘                │
│         │                    │                    │                         │
│         │                    │                    │                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                │
│  │   GitHub     │     │   GitHub     │     │   GitHub     │                │
│  │   Models     │     │   API        │     │   OAuth      │                │
│  │   (AI)       │     │   (Forks)    │     │   (Auth)     │                │
│  └──────────────┘     └──────────────┘     └──────────────┘                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐                                      │
│  │   Cloud Run  │     │   Anthropic  │                                      │
│  │   (API)      │     │   (Claude)   │                                      │
│  └──────────────┘     └──────────────┘                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Core Library (`src/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                        CORE LIBRARY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │  cli.py     │──▶│ genetics.py │──▶│ storage.py  │           │
│  │  (Commands) │   │  (DNA/Traits)│   │  (Persist)  │           │
│  └─────────────┘   └─────────────┘   └─────────────┘           │
│         │                │                   │                   │
│         │                ▼                   │                   │
│         │         ┌─────────────┐           │                   │
│         │         │evolution.py │           │                   │
│         │         │  (AI Agent) │           │                   │
│         │         └─────────────┘           │                   │
│         │                │                   │                   │
│         ▼                ▼                   │                   │
│  ┌─────────────────────────────┐            │                   │
│  │      visualizer.py          │◀───────────┘                   │
│  │      (SVG Generation)       │                                │
│  └─────────────────────────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Design Principles:**
- **Separation of Concerns**: Each module handles one domain
- **Dependency Injection**: AI provider is configurable
- **Graceful Degradation**: Falls back to random evolution if AI unavailable

### 2. API Backend (`server/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLASK API                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                     app.py                           │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │        │
│  │  │   /api/     │  │   /api/     │  │   /api/     │  │        │
│  │  │   adopt/*   │  │   health    │  │   stats     │  │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │        │
│  └──────────────────────────┬──────────────────────────┘        │
│                             │                                    │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────┐        │
│  │               github_service.py                      │        │
│  │  - OAuth token exchange                              │        │
│  │  - Repository creation from template                 │        │
│  │  - GitHub Actions enablement                         │        │
│  │  - GitHub Pages activation                           │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Deployment:**
- Containerized with Docker
- Deployed to Google Cloud Run (serverless)
- Auto-scales to zero when idle

### 3. Frontend (`web/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATIC FRONTEND                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                    index.html                        │        │
│  │                                                      │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │        │
│  │  │   Monkey    │  │  Leaderboard│  │ Family Tree │  │        │
│  │  │   Display   │  │             │  │             │  │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │        │
│  │                                                      │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │        │
│  │  │  Community  │  │  Traits     │  │  Evolution  │  │        │
│  │  │  Gallery    │  │  Display    │  │  History    │  │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │        │
│  └─────────────────────────────────────────────────────┘        │
│                             │                                    │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                    script.js                         │        │
│  │  - Loads JSON data files                             │        │
│  │  - Renders dynamic content                           │        │
│  │  - Particle effects (particles.js)                   │        │
│  │  - Keyboard shortcuts                                │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Design System:**
- Blocky/Minecraft-inspired aesthetic
- NES.css retro gaming framework
- Press Start 2P + Space Grotesk fonts
- Neon color palette (#00ff88, #ff6b9d, #ffd93d)

## Data Architecture

### DNA Schema

```json
{
  "dna_hash": "576a6a3c176765b4",
  "generation": 1,
  "traits": {
    "body_color": {"value": "golden", "rarity": "uncommon"},
    "face_expression": {"value": "mischievous", "rarity": "uncommon"},
    "accessory": {"value": "crown", "rarity": "uncommon"},
    "pattern": {"value": "spots", "rarity": "common"},
    "background": {"value": "sunset", "rarity": "common"},
    "special": {"value": "sparkles", "rarity": "uncommon"}
  },
  "parent_dna_hash": null,
  "created_at": "2025-12-21T00:00:00Z"
}
```

### Data Flow

```
User Forks Repo
       │
       ▼
┌─────────────────┐
│ on-create.yml   │  ← GitHub Actions triggered
│ workflow        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ src/cli.py init │────▶│ monkey_data/    │
│ --from-fork     │     │ dna.json        │
└─────────────────┘     │ stats.json      │
                        │ history.json    │
                        │ monkey.svg      │
                        └────────┬────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Daily Evolution │     │ GitHub Pages    │     │ Community Scan  │
│ (daily-evolution│     │ (deploy-pages   │     │ (community_scan │
│  .yml)          │     │  .yml)          │     │  .yml)          │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Automation Architecture

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `daily-evolution.yml` | Cron (00:00 UTC) | Daily AI evolution |
| `on-create.yml` | Repository create | Initialize forked monkey |
| `deploy-pages.yml` | Push to main | Deploy dashboard |
| `deploy-backend.yml` | Manual | Deploy API to Cloud Run |
| `community_scan.yml` | Manual / Scheduled | Update leaderboard data |

### Evolution Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY EVOLUTION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  00:00 UTC ──▶ Checkout ──▶ Check Monkey ──▶ Evolve ──▶ Commit  │
│                   │              │             │           │     │
│                   ▼              ▼             ▼           ▼     │
│              Setup Python   Init if new    AI/Random    Push     │
│              Install deps   from parent    mutation     changes  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Security Considerations

### Secrets Management

| Secret | Scope | Purpose |
|--------|-------|---------|
| `ANTHROPIC_API_KEY` | Repo | Claude AI evolution |
| `GITHUB_TOKEN` | Auto | Repository operations |
| `GITHUB_APP_CLIENT_ID` | Server | OAuth flow |
| `GITHUB_APP_CLIENT_SECRET` | Server | OAuth flow |

### Access Control

- **Fork Users**: Full control of their own repository
- **API**: OAuth 2.0 with minimal scopes
- **Actions**: Repository-scoped GITHUB_TOKEN
- **Cloud Run**: Unauthenticated (public API)

## Scalability

### Current Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| GitHub Actions | 2,000 mins/month (free) | ~66 evolutions/day |
| GitHub Pages | 100GB bandwidth/month | Ample for static assets |
| Cloud Run | 2M requests/month free | Scales automatically |

### Growth Path

1. **Community Growth**: Each fork is self-contained
2. **Leaderboard**: Centralized scanning, distributed data
3. **API**: Serverless auto-scaling

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary Language | Python | AI libraries, ease of use |
| Frontend | Static HTML/JS | No build step, GitHub Pages native |
| API | Flask | Lightweight, quick deployment |
| AI Primary | Claude | Better aesthetic coherence |
| AI Fallback | GPT-4o (GitHub Models) | Free, no API key needed |
| SVG Generation | Custom Python | Full control, no dependencies |
| Deployment | GitHub + Cloud Run | Free tier optimization |

---

*Generated by BMad Document Project workflow*

