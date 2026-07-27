# Documentation Hub CLI

A command-line tool for working with the Domo documentation site. No extra dependencies needed — it runs on Python 3's standard library.

## Quick Start

All commands are run from the **project root** (the folder that contains `docs.json`).

```bash
# See available commands
python scripts/docs_cli.py --help

# Export the full doc structure to CSV (uses all defaults)
python scripts/docs_cli.py export
```

This creates `scripts/reports/doc_structure.csv` with every page in the English docs.

## Commands

### `export`

Reads `docs.json` and every MDX file it references, then writes a CSV containing each page's tab, group path, file path, title, and URL.

```bash
# Basic usage — English docs, default output location
python scripts/docs_cli.py export

# Export Japanese docs
python scripts/docs_cli.py export --language jp

# Write the CSV somewhere else
python scripts/docs_cli.py export --output ~/Desktop/doc_pages.csv

# Use a different base URL for the generated links
python scripts/docs_cli.py export --base-url https://staging-docs.domo.com

# Combine options
python scripts/docs_cli.py export --language jp --output reports/jp_docs.csv --base-url https://staging-docs.domo.com

# Point at a different project root (if running from outside the repo)
python scripts/docs_cli.py export --project-dir /path/to/domo-documentation-hub
```

#### Options

| Option          | Default                             | What it does                                                                |
| --------------- | ----------------------------------- | --------------------------------------------------------------------------- |
| `--language`    | `en`                                | Language section to extract from `docs.json` (`en`, `jp`, `fr`, `de`, `es`) |
| `--base-url`    | `https://docs.domo.com`             | Base URL prepended to each file path to build the full page URL             |
| `--output`      | `scripts/reports/doc_structure.csv` | Where to write the CSV file                                                 |
| `--project-dir` | `.`                                 | Project root containing `docs.json` and the MDX files                       |

#### CSV Output

The CSV has five columns:

| Column      | Example                                                              |
| ----------- | -------------------------------------------------------------------- |
| `tab`       | `Knowledge Base`                                                     |
| `group`     | `Connect & Integrate > Connect Data to Domo > Cloud Data Warehouses` |
| `file_path` | `s/article/4412849158167`                                            |
| `title`     | `Cloud Amplifier Overview`                                           |
| `url`       | `https://docs.domo.com/s/article/4412849158167`                      |

- **group** uses `>` to show nesting. Pages that aren't inside a group have an empty group column.
- **title** is pulled from the MDX file's YAML frontmatter.

After the CSV is written, a summary prints to the terminal showing how many pages were exported, how many titles were found, and any warnings about missing files.
