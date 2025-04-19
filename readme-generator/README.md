# `readme-generator.py`

## Overview

`readme-generator.py` is a tool to fetch metadata from a list of GitHub repositories and generate categorized YAML and Markdown files, split into **valid**, **abandoned**, and **archived** sets.

## Installation

```bash
pip install PyGithub PyYAML python-dotenv
```

Ensure you have a `.env` file or environment variable:

```bash
GITHUB_TOKEN=your_personal_token
```

## Usage

### Fetch step

Fetch repo data, classify, and write YAML under `./data/`.

```bash
# Reads repos.txt, uses GitHub API, verbose output
auth-discord-generator.py fetch --txt repos.txt -v
```

Flags:

- `--txt <file>`   : Plain list of GitHub URLs, one per line.
- `--no-api`      : Skip API, parse URLs only.
- `-v, --verbose` : Print progress and warnings to stderr.

Output:

- `data/valid.yml`
- `data/abandoned.yml`
- `data/archived.yml`

### Generate Markdown

Render categorized tables into `./readme/`.

```bash
awesome-discord-generator.py render [--no-star]
```

Flags:

- `--no-star` : Omit the star-count column in all tables.

Output:

- `readme/VALID.md`
- `readme/ABANDONED.md`
- `readme/ARCHIVED.md`