# insta-fetcher

A small Python CLI that downloads media exposed by a public Instagram profile
through [Instaloader](https://instaloader.github.io/) and optionally organizes
dated files into `YYYY-MM-DD` folders.

## Install

```bash
git clone https://github.com/IvesLiu1026/insta-fetcher.git
cd insta-fetcher
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Use

```bash
insta-fetcher nasa
insta-fetcher nasa --profile-pic-only
insta-fetcher nasa --output ./downloads --no-organize
```

The command does not ask for or store Instagram credentials. Availability is
limited by what Instagram exposes publicly and by Instaloader's compatibility
with the platform.

## Responsible use

Only download content you are allowed to access and reuse. Follow Instagram's
terms, copyright rules, privacy expectations, and reasonable rate limits. This
project does not bypass private accounts or access controls.

## Development

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest
```

This repository publishes source code only. Generated downloads, build output,
and package artifacts are intentionally ignored.
