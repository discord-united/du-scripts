#!/usr/bin/env python3
"""
Fetch and print all metadata for a GitHub repository by its numeric ID.

Usage:
  # Pass the repo ID on the command line:
  python fetch_repo_by_id.py --id 480281047

  # Or omit --id to be prompted:
  python fetch_repo_by_id.py

Requires:
  pip install PyGithub python-dotenv

Optionally set GITHUB_TOKEN in your env or a .env file for higher rate limits:
  export GITHUB_TOKEN="your_token_here"
"""
import os
import sys
import json
import argparse

from dotenv import load_dotenv
from github import Github, Auth, GithubException

def main():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token == "ghp_example_token" or token == "":
        print("\n-----------------------------------------")
        print("No GitHub token could be found, aborting.")
        print("-----------------------------------------\n")
        sys.exit()

    p = argparse.ArgumentParser(description="Fetch GitHub repo metadata by ID")
    p.add_argument("--id", "-i", type=int, help="GitHub repository numeric ID")
    args = p.parse_args()

    if args.id:
        repo_id = args.id
    else:
        val = input("Enter GitHub repository ID: ").strip()
        if not val.isdigit():
            print("Error: ID must be a number.", file=sys.stderr)
            sys.exit(1)
        repo_id = int(val)


    auth = Auth.Token(token) if token else None
    gh = Github(auth=auth) if auth else Github()

    try:
        repo = gh.get_repo(repo_id)
    except GithubException as e:
        print(f"GitHub API error: {e.data.get('message', e)}", file=sys.stderr)
        sys.exit(1)

    # Print the full raw JSON
    print(json.dumps(repo.raw_data, indent=2))

    gh.close()

if __name__ == "__main__":
    main()
