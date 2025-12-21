---
stepsCompleted: [1, 2]
inputDocuments: ["_bmad-output/index.md", "_bmad-output/project-overview.md"]
session_topic: "Viral Growth Mechanics for ForkMonkey"
session_goals: "Create irresistible forking triggers & exponential spread"
selected_approach: "ai-recommended"
techniques_used: ["analogical-thinking", "reversal-inversion", "what-if-scenarios", "scamper"]
ideas_generated: []
context_file: "_bmad/bmm/data/project-context-template.md"
---

# ForkMonkey Brainstorming Session: Viral Growth Mechanics

**Date:** 2025-12-21  
**Facilitator:** Mary (Analyst Agent)  
**Participant:** Roei

---

## Session Overview

**Topic:** Viral Growth Mechanics for ForkMonkey  
**Goals:** Create irresistible forking triggers & exponential spread

### Context

ForkMonkey is a GitHub-based digital pet that:
- Evolves daily with AI (Claude/GPT-4o)
- Breeds through GitHub forking
- Competes on a rarity leaderboard
- Runs free on GitHub's infrastructure

**Current Challenge:** How to make the fork-and-share loop so compelling that growth becomes exponential.

---

## Technique Selection

**Approach:** AI-Recommended Techniques  
**Analysis Context:** Viral growth mechanics with focus on GitHub-native distribution

**Recommended Techniques:**

1. **Analogical Thinking:** Study viral success patterns from CryptoKitties, Pokémon, Tamagotchi
2. **Reversal Inversion:** Identify and remove barriers to forking/sharing
3. **What If Scenarios:** Remove constraints to find breakthrough ideas
4. **SCAMPER Method:** Systematically innovate on the fork mechanic

**AI Rationale:** This sequence moves from analysis → barrier removal → radical innovation → practical features, ensuring both breakthrough thinking and actionable outcomes.

---

## Phase 1: Analogical Thinking

*Studying viral success patterns from comparable products*

### Exploration Prompts

- "What made CryptoKitties go viral?"
- "How did Pokémon create collecting addiction?"
- "What made Tamagotchi a cultural phenomenon?"
- "How did Wordle achieve organic spread?"

### Ideas Generated

**From CryptoKitties Pattern:**
- Trait Extinction — Gen-locked traits that become impossible to get
- Breeding-Only Traits — Combinations only emerge through specific parent traits
- Time-Limited Traits — Seasonal/holiday traits create urgency

**From Pokémon Pattern:**
- Trait Inheritance Lottery — Fork to inherit rare traits you can't evolve
- Breeding Bonuses — "First 5 forks get +10% legendary chance"
- Lineage Achievements — Parent gets rewards when children succeed
- Ancestor Leaderboard — "Most Prolific Lineage" competition

**From Wordle Pattern:**
- Shareable Evolution Card — Visual grid showing today's evolution results
- Auto-generated share text with stats, rarity change, and CTA

**From Tamagotchi Pattern:**
- Evolution Prediction Game — Guess which trait mutates, earn bonus points
- Streak Rewards — 7/30 day streaks with guaranteed rarity upgrades
- Daily Breeding Windows — Time-limited fork bonuses

**Top 5 Priority Mechanics:**
1. 🥇 Shareable Evolution Card (Wordle-style visual)
2. 🥈 Fork Inheritance Boost (First 5 forks bonus)
3. 🥉 Lineage Achievements (Most descendants)
4. 4️⃣ Streak System (7/30 day rewards)
5. 5️⃣ Trait Extinction (Gen-locked traits)

---

## Phase 2: Reversal Inversion

*Flipping the problem: What STOPS people from forking/sharing?*

### Exploration Prompts

- "What would make someone NOT fork this?"
- "How could we make this WORSE for growth?"
- "What's the opposite of viral?"

### Barriers Identified

**Discovery Barriers:**
- "I don't know this exists" → Solution: Auto-announce forks
- "Looks like another GitHub project" → Solution: Stunning visual README

**Decision Barriers:**
- "What's in it for me?" → Solution: Show inherited traits upfront
- "I'll do it later" → Solution: Urgency messaging ("First 5 forks get boost!")

**Action Barriers:**
- "Where's the fork button?" → Solution: Giant CTA buttons
- Post-fork confusion → Solution: Auto-setup, welcome issue

**Retention Barriers:**
- "I forgot about it" → Solution: Daily notifications
- "Nothing's happening" → Solution: Dramatic evolution stories

**Sharing Barriers:**
- "I'd feel weird sharing" → Solution: Achievement unlocks for sharing
- "No easy way to share" → Solution: One-click shareable cards

---

## Implementation Session

### Features Implemented

| # | Feature | Status | Command |
|---|---------|--------|---------|
| 1 | 🎨 Shareable Evolution Card | ✅ Done | `python src/cli.py share-card` |
| 2 | 📢 Fork Notification in README | ✅ Done | Auto-updates via `update-readme` |
| 3 | ⚡ Urgency Messaging | ✅ Done | "First 5 forks get boost!" in README |
| 4 | 🏆 Lineage Counter | ✅ Done | Shows in `show` command |
| 5 | 📊 Rarity Percentile | ✅ Done | "Rarer than X% of monkeys!" |

### Code Changes Made

1. **`src/cli.py`** — Added `share-card` command with Wordle-style visual
2. **`src/cli.py`** — Enhanced `show` command with percentile and tier
3. **`src/cli.py`** — Enhanced `update-readme` with lineage stats and urgency
4. **`README.md`** — Added LINEAGE_STATS and BREEDING_BOOST sections

---

