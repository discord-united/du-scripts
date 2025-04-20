# `readme-generator.py`

## Overview

`readme-generator.py` is a tool to fetch metadata from a list of GitHub repositories and generate categorized YAML and Markdown files, split into **valid**, **abandoned**, and **archived** sets.

## 📋 Prerequisites

- Python 3.9+
- Install dependencies:
  ```bash
  pip install PyGithub PyYAML python-dotenv
  ```
- Create a `.env` file or set environment variable:
  ```bash
  GITHUB_TOKEN=your_personal_access_token
  ```
  A token avoids rate limits and grants repo access.
Ensure you have a `.env` file or environment variable:

---

## 🗂️ Project Layout

```
readme-generator/
├── data/             # Generated YAML files
│   ├── valid.yml
│   ├── inactive.yml
│   └── archived.yml
├── readme/           # Generated Markdown files
│   ├── VALID.md
│   ├── INACTIVE.md
│   ├── ARCHIVED.md
│   └── README.md     # Combined (if --readme)
└── readme-generator.py
```

---

## 🚀 Usage

### Fetch Data

```bash
python readme-generator.py fetch --txt repos.txt [options]
```

- `--txt, -t <file>`	: Path to a plain-text file with one GitHub URL per line.
- `--no-api`        	: Skip GitHub API calls (only URL parsing).
- `-v, --verbose`   	: Print progress and warnings to stderr.
- `--no-cat`        	: Skip categorization (all projects marked `Solutions`).
- `--readme`        	: Skip separate MD files; generate a combined `readme/README.md`.

Generates:
- `data/valid.yml`    
- `data/inactive.yml`
- `data/archived.yml`
- **Optionally** `readme/README.md` when `--readme` is set.

### Render Markdown

```bash
python readme-generator.py render [options]
```

- `--no-author`  	: Omit the **Author** column.
- `--no-star`    	: Omit the **Star** column.
- `--no-commit`  	: Omit the **Last-commit** column.
- `--no-lang`    	: Omit the **Top-language** column.
- `--no-license` 	: Omit the **License** column.
- `--no-desc`    	: Omit the **Description** column.
- `--readme`     	: Output a combined `readme/README.md` instead of separate files.

Reads existing YAML in `data/` and produces Markdown in `readme/`:
- `VALID.md`
- `INACTIVE.md`
- `ARCHIVED.md`
- Or combined `README.md` if `--readme`.

---

## 🛠️ Configuration

- **ARCHIVE_AFTER**: Time delta for classifying a repo as inactive (default: 365 days).
- **VALID_CATEGORIES** & **CATEGORY_KEYWORDS**: Define allowed category names and matching keywords. Fallback to `Solutions` if no match.