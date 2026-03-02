# Article Content Update Migration (HTML → MDX)

Bulk-updates article MDX files from a Salesforce Knowledge CSV export. Converts raw HTML article bodies to MDX format and writes them into existing files across all languages.

## CSV Source

`Knowledge Article Mod 1Aug2025 - 13Feb2026.csv` — 702 rows exported from Salesforce Knowledge. Key columns:

| Column | Purpose |
|---|---|
| `URLNAME` | Article identifier, maps to `{URLNAME}.mdx` filename |
| `LANGUAGE` | `en_US`, `ja`, `fr`, `de`, `es` (plus 1 `zh_CN` row, skipped) |
| `ARTICLE_BODY__C` | Raw HTML body content |
| `TITLE` | Article title — compared against existing frontmatter |
| `LASTMODIFIEDDATE` | ISO 8601 timestamp, used for dedup |

12 articles have duplicate rows (same URLNAME + LANGUAGE); the script keeps the most recent by `LASTMODIFIEDDATE`.

## What the Script Does

1. Reads and deduplicates the CSV (702 → 630 unique article/language pairs)
2. For each article, finds the existing MDX file by language directory:
   - `en_US` → `s/article/{URLNAME}.mdx`
   - `ja` → `ja/s/article/{URLNAME}.mdx`
   - `fr`, `de`, `es` → `{lang}/s/article/{URLNAME}.mdx`
3. Converts HTML → MDX:
   - `<div class="info-box note">` → `<Note>` component
   - `<div class="info-box important">` → `<Warning>` component
   - Force.com `<img>` URLs → local `/images/kb/{eid}-{feoid}-{refid}.{ext}` paths wrapped in `<Frame>`
   - `<span class="mt-font-courier-new">` / `<span class="nowiki">` → `` `code` ``
   - HTML tables → cleaned of Salesforce artifacts (`data-aura-rendered-by`, editorial classes)
   - Images inside tables get JSX-style dimensions (`style={{width: N, height: N}}`)
4. Preserves existing frontmatter, updates title only if CSV differs
5. Only updates existing files — never creates new MDX files

## Setup

```
pip install markdownify
```

## Usage

```
python scripts/articleUpdateMigration/update_articles.py [options]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--project-dir` | `.` | Project root directory |
| `--csv` | auto-detected | Path to CSV file |
| `--dry-run` | off | Preview without writing files |
| `--limit N` | 0 (all) | Process only the first N articles |
| `--skip-images` | off | Skip image copying (MDX paths still generated) |
| `--image-dir` | `scripts/articleUpdateMigration/images/` | Source dir for pre-downloaded images |
| `--image-ext` | `png` | Default image file extension |
| `--image-match` | `eid-feoid-refid` | Image matching strategy (see below) |
| `--manifest` | none | Path to manifest file (for `--image-match manifest`) |
| `--only-language` | all | Process single language, e.g. `en_US` |
| `--only-urlname` | all | Process single article (for testing) |
| `--verbose` | off | DEBUG-level log output |

### Image Matching Strategies

Images in the HTML reference `domo.file.force.com` URLs with `eid`, `feoid`, and `refid` query params. The script maps these to local files in `--image-dir` using one of three strategies:

- **`eid-feoid-refid`** (default): Source files named `{eid}-{feoid}-{refid}.{ext}`
- **`refid-only`**: Source files named `{refid}.{ext}`
- **`manifest`**: A JSON or CSV file maps Force.com URLs to local filenames

## Examples

```bash
# Dry-run on a single article
python scripts/articleUpdateMigration/update_articles.py --dry-run --only-urlname 360042932514

# First 5 articles, no image copying
python scripts/articleUpdateMigration/update_articles.py --limit 5 --skip-images

# English articles only
python scripts/articleUpdateMigration/update_articles.py --only-language en_US

# Full run
python scripts/articleUpdateMigration/update_articles.py
```

## Output

- **Console**: Progress counter (`[42/630] Processing 360042932514 (en_US)...`) and summary report
- **Log file**: `scripts/articleUpdateMigration/update_articles.log` — per-article detail including title changes, image mappings, and errors

### Stats from dry-run (full CSV)

```
CSV rows total:            702
CSV rows after dedup:      630
CSV rows skipped (empty):  26
CSV rows skipped (lang):   1    (zh_CN, no directory)
Articles updated:          488
Articles skipped (no file):142
Titles updated:            35
Images found:              5073
Errors:                    0
```
