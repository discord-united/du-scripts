#!/usr/bin/env python3
import argparse
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

import yaml
from dotenv import load_dotenv
from github import Github, Auth, GithubException

# 1 year cutoff
ARCHIVE_AFTER = timedelta(days=365)

# Allowed categories and keyword mapping
VALID_CATEGORIES = [
    "Website Templates",
    "Discovery Sites",
    "Platforms",
    "Solutions",
    "Dashboards",
    "Bot Templates",
    "Developer Tools",
    "Libraries",
    "Bots",
]
CATEGORY_KEYWORDS = {
    "Bots": ["bot", "discord"],
    "Dashboards": ["dashboard"],
    "Bot Templates": ["template"],
    "Developer Tools": ["cli", "tool", "sdk"],
    "Libraries": ["api", "wrapper", "library", "framework"],
    "Website Templates": ["website", "web", "landing", "template"],
    "Discovery Sites": ["discover", "directory", "listing"],
    "Platforms": ["platform", "service"],
    "Solutions": ["solution", "help", "support"],
}

CATEGORY_CHECK_ORDER = VALID_CATEGORIES.copy()


def parse_github_url(url: str) -> tuple[str, str]:
    p = urlparse(url.rstrip("/"))
    if p.netloc not in ("github.com", "www.github.com"):
        raise ValueError(f"Not a GitHub URL: {url}")
    owner, repo, *_ = p.path.strip("/").split("/")
    if not repo:
        raise ValueError(f"Invalid repo path: {url}")
    return owner, repo


def classify_category(name: str, desc: str) -> str:
    txt = (name + " " + desc).lower()
    for cat in CATEGORY_CHECK_ORDER:
        kws = CATEGORY_KEYWORDS.get(cat, [])
        if any(kw in txt for kw in kws):
            return cat
    return "Solutions"


def make_badges(owner: str, repo: str) -> dict:
    b = "https://img.shields.io/github"
    return {
        "star_count": f"{b}/stars/{owner}/{repo}?style=flat-square",
        "last_commit": f"{b}/last-commit/{owner}/{repo}?style=flat-square",
        "top_language": f"{b}/languages/top/{owner}/{repo}?style=flat-square",
        "license": f"{b}/license/{owner}/{repo}?style=flat-square",
    }


def fetch_all(urls: list[str], use_api: bool, verbose: bool):
    token = os.getenv("GITHUB_TOKEN", "").strip()
    gh = (Github(auth=Auth.Token(token)) if (use_api and token)
          else Github() if use_api else None)

    valid, inactive = [], []
    now = datetime.now(timezone.utc)

    for i, url in enumerate(urls, start=1):
        if verbose:
            print(f"[{i}/{len(urls)}] {url}", file=sys.stderr)
        try:
            owner, repo = parse_github_url(url)
            if use_api:
                r = gh.get_repo(f"{owner}/{repo}")
                pushed = r.pushed_at.replace(tzinfo=timezone.utc)
                archived_flag = r.archived
                meta = {
                    "name": r.name,
                    "id": r.id,
                    "author": r.owner.login,
                    "source": r.html_url,
                    "description": r.description or "",
                    "pushed_at": pushed.isoformat(),
                    "archived": archived_flag,
                    "badges": make_badges(owner, repo),
                }
                updated = pushed
            else:
                updated = now
                meta = {
                    "name": repo,
                    "author": owner,
                    "source": url,
                    "description": "",
                    "pushed_at": now.isoformat(),
                    "archived": False,
                    "badges": make_badges(owner, repo),
                }

            # classify + validate
            cat = classify_category(meta["name"], meta["description"])
            if cat not in VALID_CATEGORIES:
                if verbose:
                    print(f"  ⚠️  '{cat}' not in VALID_CATEGORIES, defaulting to 'Solutions'", file=sys.stderr)
                cat = "Solutions"
            meta["category"] = cat

            # split valid vs inactive
            if use_api and (now - updated) > ARCHIVE_AFTER:
                inactive.append(meta)
                if verbose: print("  → inactive", file=sys.stderr)
            else:
                valid.append(meta)
                if verbose: print("  → valid", file=sys.stderr)

        except GithubException as e:
            if verbose:
                print(f"  ⛔ skip {url}: {e.data.get('message', e)}", file=sys.stderr)
        except Exception as e:
            if verbose:
                print(f"  ⛔ skip {url}: {e}", file=sys.stderr)

    if gh:
        gh.close()

    archived_flagged = [r for r in valid + inactive if r.get("archived")]
    return valid, inactive, archived_flagged


def write_yaml(path: str, entries: list[dict]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"repositories": entries}, f, sort_keys=False)


def render_md(
        path: str,
        entries: list[dict],
        include_archived_col: bool = False,
        include_star_col: bool = True,
):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    grouped = defaultdict(list)
    for r in entries:
        grouped[r["category"]].append(r)

    headers = ["Project Name"]
    if include_star_col:
        headers.append("⭐")
    headers.extend(["⏱️", "🖥️", "📄"])
    if include_archived_col:
        headers.append("🏷️ Archived")
    headers.append("Description")

    sep = ["-" * len(h) for h in headers]
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(sep) + " |"

    lines = []
    for cat in sorted(grouped):
        repos = sorted(grouped[cat], key=lambda r: r["name"].lower())
        lines.append(f"## {cat}\n")
        lines.append(header_line)
        lines.append(sep_line)
        for r in repos:
            b = r["badges"]
            row = [f"[{r['name']}]({r['source']})"]
            if include_star_col:
                row.append(f"![Star]({b['star_count']})")
            row.extend([
                f"![Commit]({b['last_commit']})",
                f"![Lang]({b['top_language']})",
                f"![License]({b['license']})",
            ])
            if include_archived_col:
                row.append("✅" if r.get("archived") else "")
            row.append(r["description"])
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def load_txt(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def load_yml(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("repositories", [])


def main():
    load_dotenv()

    if os.getenv("GITHUB_TOKEN") == "ghp_example_token" or os.getenv("GITHUB_TOKEN") == "":
        print("\n-----------------------------------------")
        print("No GitHub token could be found, aborting.")
        print("-----------------------------------------\n")
        sys.exit()
    p = argparse.ArgumentParser(prog="readme-generator.py")
    sub = p.add_subparsers(dest="cmd")

    f = sub.add_parser("fetch", help="fetch & split into valid.yml/inactive.yml/archived.yml")
    f.add_argument("--txt", "-t", required=True, help="raw URLs file")
    f.add_argument("--no-api", action="store_true")
    f.add_argument("-v", "--verbose", action="store_true")

    m = sub.add_parser("render", help="Render VALID.md, INACTIVE.md & ARCHIVED.md from YAML")
    m.add_argument("--no-star", action="store_true", help="Omit star column")

    args = p.parse_args(sys.argv[1:] or ["fetch", "--txt", "repos.txt"])

    if args.cmd in (None, "fetch"):
        urls = load_txt(args.txt)
        valid, inactive, archived_flagged = fetch_all(urls, not args.no_api, args.verbose)
        write_yaml("data/valid.yml", valid)
        write_yaml("data/inactive.yml", inactive)
        write_yaml("data/archived.yml", archived_flagged)
        if args.cmd == "fetch":
            return

    # render
    valid = load_yml("data/valid.yml")
    inactive = load_yml("data/inactive.yml")
    archived = load_yml("data/archived.yml")

    render_md(
        "readme/VALID.md", valid,
        include_archived_col=False,
        include_star_col=not getattr(args, "no_star", False),
    )
    render_md(
        "readme/INACTIVE.md", inactive,
        include_archived_col=True,
        include_star_col=not getattr(args, "no_star", False),
    )
    render_md(
        "readme/ARCHIVED.md", archived,
        include_archived_col=True,
        include_star_col=not getattr(args, "no_star", False),
    )


if __name__ == "__main__":
    main()
