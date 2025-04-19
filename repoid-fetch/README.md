# `fetch-id.py`

## Overview

`fetch-id.py` retrieves the full JSON metadata of a GitHub repository by its numeric ID, using the PyGithub library.

## Installation

```bash
pip install PyGithub python-dotenv
```

Set your token:

```bash
GITHUB_TOKEN=your_personal_token
```

## Usage

### Command-line ID

Fetch by passing `--id`:

```bash
python fetch-id.py --id 879513837
```

### Interactive prompt

If no `--id` is given, you are prompted:

```bash
python fetch-id.py
Enter GitHub repository ID: 879513837
```

## Output

Prints prettified JSON of the repository’s metadata to `stdout`.

Flags:

- `--id, -i <number>` : Numeric GitHub repo ID.