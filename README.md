# DU-Scripts

This repository (`du-scripts`) contains a collection of utility scripts maintained by Discord United for automating documentation and repository lookup tasks. It currently includes two main tools:

- **readme-generator**: Fetches metadata from a list of GitHub repositories and generates categorized YAML and Markdown files.  
- **repoid-fetch**: Retrieves full JSON metadata for a GitHub repository by its numeric ID.

---

## 📦 Repository Structure

```
du-scripts/
├── readme-generator/     # Tool to generate YAML & Markdown from GitHub URLs
│   ├── readme-generator.py
│   └── ...
├── repoid-fetch/         # Tool to fetch repo JSON by ID
│   ├── repoid-fetch.py
│   └── ...
└── README.md             # You are here
```

---

## 🔧 Installation

Both tools share similar dependencies. From the root of this repo, install via:

```bash
pip install PyGithub PyYAML python-dotenv
```

Create a `.env` file in this directory (or set environment variables) with your GitHub personal access token:

```bash
GITHUB_TOKEN=your_personal_token_here
```

This token grants higher API rate limits and access to private repos if needed.

---

## 🚀 Usage

### 1. readme-generator

The **readme-generator** tool automates fetching metadata from multiple GitHub repositories and produces:

- **YAML** files under `data/`: `valid.yml`, `inactive.yml`, `archived.yml`  
- **Markdown** tables under `readme/`: `VALID.md`, `INACTIVE.md`, `ARCHIVED.md`

#### Fetch Step

```bash
cd readme-generator
python readme-generator.py fetch --txt path/to/repos.txt [-v] [--no-api]
```

- `--txt <file>`   : File with one GitHub repo URL per line.  
- `-v, --verbose` : Show progress and warnings.  
- `--no-api`      : Skip GitHub API calls; parse URLs only.

#### Render Step

```bash
python readme-generator.py render [--no-star]
```

- `--no-star` : Omit the ⭐ star-count column from Markdown tables.

### 2. repoid-fetch

The **repoid-fetch** tool retrieves all repository metadata for a given numeric GitHub repo ID.

#### Command‑Line Mode

```bash
cd repoid-fetch
python fetch-id.py --id 480281047
```

#### Interactive Mode

```bash
python fetch-id.py
# Then enter the repo ID at the prompt
```

---

## 📝 License

This collection of scripts is released under the MIT License. See [LICENSE](LICENSE) for details.

---

*Created and maintained by Discord United.*

