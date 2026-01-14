#!/usr/bin/env python3
"""
ForkMonkey Community Scanner

Scans all forks of the repository to aggregate monkey data.
Generates multiple static JSON files for the web app:
- web/community_data.json - All forks with SVGs and stats
- web/leaderboard.json - Rarity rankings
- web/family_tree.json - Fork genealogy
- web/network_stats.json - Aggregate statistics
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from github import Github, GithubException


def scan_community():
    """Main scanner function that generates all static data files."""
    print("🌍 Starting ForkMonkey Community Scan...")
    
    # Initialize GitHub
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("⚠️  No GITHUB_TOKEN found. API limits will be strict.")
    
    g = Github(token)
    
    # Determine repo to scan
    repo_name = os.getenv("GITHUB_REPOSITORY")
    if not repo_name:
        print("⚠️  GITHUB_REPOSITORY not set. Using default 'roeiba/forkMonkey'")
        repo_name = "roeiba/forkMonkey"
        
    try:
        repo = g.get_repo(repo_name)
        
        # If we are a fork, scan the parent's forks instead
        if repo.fork and repo.parent:
            print(f"🍴 Detected fork of {repo.parent.full_name}. Scanning parent's network...")
            target_repo = repo.parent
        else:
            target_repo = repo
            
        print(f"📡 Scanning forks of {target_repo.full_name}...")
        
        # Collect all repos to scan
        repos_to_scan = collect_repos(target_repo)
        print(f"🎯 Found {len(repos_to_scan)} potential habitats.")
        
        # Scan each repo and collect monkey data
        monkeys = []
        for repo_tuple in repos_to_scan:
            repo, degree = repo_tuple
            monkey = scan_repo(repo, target_repo.full_name, degree)
            if monkey:
                monkeys.append(monkey)
                degree_label = get_degree_label(degree)
                print(f"✅ Found monkey in {repo.full_name} ({degree_label})")
        
        # Print summary by degree
        degree_counts = {}
        for m in monkeys:
            d = m.get("degree", 0)
            degree_counts[d] = degree_counts.get(d, 0) + 1
        print(f"\n📊 Degree breakdown:")
        for d in sorted(degree_counts.keys()):
            print(f"   {get_degree_label(d)}: {degree_counts[d]} monkeys")
        
        print(f"\n✨ Scan complete! Discovered {len(monkeys)} monkeys.")
        
        # Generate all output files
        generate_community_data(target_repo.full_name, monkeys)
        generate_leaderboard(monkeys)
        generate_family_tree(target_repo.full_name, monkeys)
        generate_network_stats(monkeys)
        
        print("\n💾 All data files generated successfully!")
        
    except Exception as e:
        print(f"🔥 Critical error during scan: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


def collect_repos(target_repo, max_depth=3, max_total=200):
    """Collect all repos in the network (root + nested forks up to max_depth levels).
    
    Args:
        target_repo: The root repository to scan
        max_depth: Maximum depth to scan (1=direct forks, 2=forks of forks, 3=third level)
        max_total: Maximum total repos to collect
        
    Returns:
        List of tuples: (repo, degree) where degree is the distance from root (0=root, 1=1st degree, etc.)
    """
    repos = [(target_repo, 0)]  # (repo, degree)
    seen = {target_repo.full_name}
    queue = [(target_repo, 0)]  # BFS queue with (repo, current_depth)
    
    while queue and len(repos) < max_total:
        current_repo, current_depth = queue.pop(0)
        
        # Stop if we've reached max depth
        if current_depth >= max_depth:
            continue
        
        try:
            forks = current_repo.get_forks()
            # Get up to 50 forks per repo (1 page)
            try:
                page = forks.get_page(0)
                for fork in page:
                    if fork.full_name not in seen and len(repos) < max_total:
                        seen.add(fork.full_name)
                        fork_degree = current_depth + 1
                        repos.append((fork, fork_degree))
                        queue.append((fork, fork_degree))
                        
                        degree_label = get_degree_label(fork_degree)
                        print(f"  📍 Found {degree_label} fork: {fork.full_name}")
            except Exception:
                pass
        except Exception as e:
            print(f"⚠️ Error fetching forks of {current_repo.full_name}: {e}")
    
    return repos


def get_degree_label(degree):
    """Get human-readable label for fork degree."""
    labels = {
        0: "root",
        1: "1st degree",
        2: "2nd degree", 
        3: "3rd degree"
    }
    return labels.get(degree, f"{degree}th degree")


def scan_repo(repo, root_name, degree=0):
    """Scan a single repo for monkey data.
    
    Args:
        repo: GitHub repository object
        root_name: Full name of the root repository
        degree: Fork degree (0=root, 1=1st degree, 2=2nd degree, 3=3rd degree)
    """
    try:
        # Calculate age from creation
        now = datetime.now(timezone.utc)
        created = repo.created_at.replace(tzinfo=timezone.utc)
        age = (now - created).days
        
        monkey_data = {
            "owner": repo.owner.login,
            "repo": repo.name,
            "full_name": repo.full_name,
            "url": repo.html_url,
            "is_root": repo.full_name == root_name,
            "degree": degree,
            "degree_label": get_degree_label(degree),
            "parent": repo.parent.full_name if repo.fork and repo.parent else None,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "monkey_stats": None,
            "monkey_svg": None,
            "monkey_dna": None
        }
        
        # Fetch stats.json
        try:
            contents = repo.get_contents("monkey_data/stats.json")
            stats = json.loads(contents.decoded_content.decode())
            # Always calculate fresh age from repo creation date (fixes Issue #64)
            stats["age_days"] = age
            monkey_data["monkey_stats"] = stats
        except Exception:
            pass
        
        # Fetch monkey.svg
        try:
            contents = repo.get_contents("monkey_data/monkey.svg")
            svg = contents.decoded_content.decode()
            monkey_data["monkey_svg"] = svg
        except Exception:
            pass
        
        # Fetch dna.json for extra data
        try:
            contents = repo.get_contents("monkey_data/dna.json")
            dna = json.loads(contents.decoded_content.decode())
            monkey_data["monkey_dna"] = dna
        except Exception:
            pass
        
        # Only return if we found at least stats or SVG
        if monkey_data["monkey_stats"] or monkey_data["monkey_svg"]:
            # Ensure basic stats if missing
            if not monkey_data["monkey_stats"]:
                monkey_data["monkey_stats"] = {
                    "generation": 1,
                    "rarity_score": 0,
                    "age_days": age,
                    "mutation_count": 0
                }
            return monkey_data
        
        return None
        
    except Exception as e:
        print(f"❌ Error scanning {repo.full_name}: {e}")
        return None


def generate_community_data(source_repo, monkeys):
    """Generate community_data.json with all fork data."""
    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "source_repo": source_repo,
        "total_forks": len(monkeys),
        "forks": monkeys
    }
    
    output_file = Path("web/community_data.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"📊 Generated {output_file}")


def generate_leaderboard(monkeys):
    """Generate leaderboard.json with rarity rankings."""
    # Sort by rarity score (descending)
    sorted_monkeys = sorted(
        monkeys,
        key=lambda m: m.get("monkey_stats", {}).get("rarity_score", 0),
        reverse=True
    )
    
    rankings = []
    for rank, monkey in enumerate(sorted_monkeys, start=1):
        stats = monkey.get("monkey_stats", {})
        rankings.append({
            "rank": rank,
            "owner": monkey["owner"],
            "repo": monkey["repo"],
            "full_name": monkey["full_name"],
            "url": monkey["url"],
            "rarity_score": stats.get("rarity_score", 0),
            "generation": stats.get("generation", 1),
            "age_days": stats.get("age_days", 0),
            "mutation_count": stats.get("mutation_count", 0),
            "is_root": monkey["is_root"],
            "degree": monkey.get("degree", 0),
            "degree_label": monkey.get("degree_label", "root"),
            "monkey_svg": monkey.get("monkey_svg")
        })
    
    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_ranked": len(rankings),
        "rankings": rankings
    }
    
    output_file = Path("web/leaderboard.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"🏆 Generated {output_file}")


def generate_family_tree(root_name, monkeys):
    """Generate family_tree.json with fork genealogy."""
    # Build parent-children relationships
    nodes = {}
    
    for monkey in monkeys:
        full_name = monkey["full_name"]
        parent = monkey.get("parent")
        
        # Create node if not exists
        if full_name not in nodes:
            nodes[full_name] = {
                "id": full_name,
                "owner": monkey["owner"],
                "repo": monkey["repo"],
                "url": monkey["url"],
                "parent": parent,
                "children": [],
                "is_root": monkey["is_root"],
                "degree": monkey.get("degree", 0),
                "degree_label": monkey.get("degree_label", "root"),
                "rarity_score": monkey.get("monkey_stats", {}).get("rarity_score", 0),
                "generation": monkey.get("monkey_stats", {}).get("generation", 1),
                "monkey_svg": monkey.get("monkey_svg")
            }
        
        # Add as child to parent
        if parent and parent in nodes:
            if full_name not in nodes[parent]["children"]:
                nodes[parent]["children"].append(full_name)
    
    # Second pass: ensure all children are properly linked
    for monkey in monkeys:
        parent = monkey.get("parent")
        full_name = monkey["full_name"]
        if parent and parent in nodes:
            if full_name not in nodes[parent]["children"]:
                nodes[parent]["children"].append(full_name)
    
    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "root": root_name,
        "total_nodes": len(nodes),
        "nodes": list(nodes.values())
    }
    
    output_file = Path("web/family_tree.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"🌳 Generated {output_file}")


def generate_network_stats(monkeys):
    """Generate network_stats.json with aggregate statistics."""
    if not monkeys:
        data = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_monkeys": 0,
            "active_today": 0,
            "generations": {},
            "avg_rarity": 0,
            "rarest_trait": None,
            "most_common_trait": None,
            "trait_distribution": {}
        }
    else:
        # Count generations
        generation_counts = Counter()
        rarity_scores = []
        trait_counts = Counter()
        active_today = 0
        now = datetime.now(timezone.utc)
        
        for monkey in monkeys:
            stats = monkey.get("monkey_stats", {})
            dna = monkey.get("monkey_dna", {})
            
            # Generations
            gen = stats.get("generation", 1)
            generation_counts[str(gen)] += 1
            
            # Rarity
            rarity = stats.get("rarity_score", 0)
            rarity_scores.append(rarity)
            
            # Active today check
            updated = monkey.get("updated_at")
            if updated:
                try:
                    updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    if (now - updated_dt).days == 0:
                        active_today += 1
                except Exception:
                    pass
            
            # Collect traits
            traits = stats.get("traits", {})
            if not traits and dna:
                traits = dna.get("traits", {})
            
            for trait_name, trait_data in traits.items():
                if isinstance(trait_data, dict):
                    value = trait_data.get("value", "unknown")
                else:
                    value = trait_data
                trait_counts[f"{trait_name}:{value}"] += 1
        
        # Calculate stats
        avg_rarity = sum(rarity_scores) / len(rarity_scores) if rarity_scores else 0
        
        # Find rarest and most common traits
        rarest_trait = None
        most_common_trait = None
        
        if trait_counts:
            sorted_traits = trait_counts.most_common()
            most_common = sorted_traits[0]
            rarest = sorted_traits[-1]
            
            most_common_trait = {
                "trait": most_common[0].split(":")[0],
                "value": most_common[0].split(":")[1] if ":" in most_common[0] else most_common[0],
                "count": most_common[1]
            }
            
            rarest_trait = {
                "trait": rarest[0].split(":")[0],
                "value": rarest[0].split(":")[1] if ":" in rarest[0] else rarest[0],
                "count": rarest[1]
            }
        
        # Build trait distribution
        trait_distribution = {}
        for trait_key, count in trait_counts.items():
            parts = trait_key.split(":")
            trait_name = parts[0]
            trait_value = parts[1] if len(parts) > 1 else "unknown"
            
            if trait_name not in trait_distribution:
                trait_distribution[trait_name] = {}
            trait_distribution[trait_name][trait_value] = count
        
        data = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_monkeys": len(monkeys),
            "active_today": active_today,
            "generations": dict(generation_counts),
            "avg_rarity": round(avg_rarity, 2),
            "max_rarity": round(max(rarity_scores), 2) if rarity_scores else 0,
            "min_rarity": round(min(rarity_scores), 2) if rarity_scores else 0,
            "rarest_trait": rarest_trait,
            "most_common_trait": most_common_trait,
            "trait_distribution": trait_distribution
        }
    
    output_file = Path("web/network_stats.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"📈 Generated {output_file}")


if __name__ == "__main__":
    scan_community()
