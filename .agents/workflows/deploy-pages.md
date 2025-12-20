# GitHub Pages Deployment Workflow

## Overview

The `deploy-pages.yml` workflow automatically deploys the ForkMonkey web app to GitHub Pages.

## Triggers

The workflow runs in the following scenarios:

1. **Push to main** - When changes are made to:
   - `web/**` - Web app files
   - `monkey_data/**` - Monkey data files
   - `.github/workflows/deploy-pages.yml` - The workflow itself

2. **After Evolution** - Automatically after these workflows complete:
   - `Daily Evolution` - Daily monkey evolution
   - `Initialize Forked Monkey` - Fork initialization

3. **Manual** - Via workflow_dispatch (Actions tab → Deploy to GitHub Pages → Run workflow)

## Integration with Other Workflows

```
┌─────────────────────┐     ┌─────────────────────┐
│  Initialize Forked  │     │   Daily Evolution   │
│       Monkey        │     │                     │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           │  workflow_run trigger     │
           └───────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Deploy to GitHub      │
              │        Pages           │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │   Live Web App at      │
              │ username.github.io/    │
              │     forkMonkey         │
              └────────────────────────┘
```

## Setup Requirements

GitHub Pages is automatically enabled when the workflow runs for the first time. The workflow uses the `enablement: true` parameter in the `configure-pages` action to automatically enable GitHub Pages with GitHub Actions as the build source.

No manual configuration is required - this works out of the box for forked repositories!

## What Gets Deployed

- `web/index.html` - Main web app
- `web/style.css` - Styles
- `web/script.js` - JavaScript logic
- `web/monkey_data/` - Copied from root `monkey_data/` during build

## URL

After deployment, your monkey will be live at:
```
https://<username>.github.io/<repo-name>/
```
