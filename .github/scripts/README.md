# OpenAPI Sync Scripts

Helper scripts used by `.github/workflows/sync-api-docs.yml` to sync OpenAPI YAML files from the source repo (`domoinc/internal-domo-apis`) into this repo (`openapi/product/`) and update `docs.json` navigation.

## Active scripts

### `detect_yaml_changes.py`

Detects which YAML files in the source repo differ from the destination via **SHA-256 content hashing**. Writes `changed_files.txt` (one source path per line) and the GitHub Actions outputs `changed_files` and `summary`.

```bash
python detect_yaml_changes.py \
  --source source-repo/api-docs/public \
  --dest openapi/product \
  --force false
```

**Arguments:**
- `--source`: Path to source repo YAML directory
- `--dest`: Path to destination YAML directory
- `--force`: `true` to force sync all files

**Notes:**
- Comparison is by content hash, not mtime — `actions/checkout` resets mtimes on both clones, making mtime comparison unreliable.
- Case-only filename renames are treated as modifications so the destination filename gets normalized.
- Always exits 0. The caller decides whether to act on the results via `changed_files.txt`.

---

### `prune_stale_nav.py`

Walks `docs.json` and removes OpenAPI page entries (`"openapi/product/<file>.yaml METHOD /path"`) whose referenced YAML does not exist on disk. Fixes the case where Mintlify preview deploys fail after a YAML is deleted upstream or case-renamed (e.g., `Filesets.yaml` → `filesets.yaml`) but the old nav entry lingers.

```bash
# Preview what would be pruned (exits 1 if any found):
python prune_stale_nav.py --check --docs-json ./docs.json --repo-root .

# Actually prune:
python prune_stale_nav.py --docs-json ./docs.json --repo-root .
```

**Why the explicit case-sensitive check?** Dev repos on macOS APFS are case-insensitive, so `os.path.isfile("Filesets.yaml")` returns True even when only `filesets.yaml` exists. CI and Mintlify preview both run on case-sensitive Linux where the reference is stale. The script checks `os.listdir()` membership directly to match Linux behavior.

Wired into `sync-api-docs.yml` after the nav-regen step so every sync PR also cleans up dangling entries.

---

### `sync_to_destination.py`

Standalone helper that copies YAMLs from a list into a destination directory, removing any case-variant duplicates. **Not invoked by `sync-api-docs.yml` directly** — the workflow inlines a single-file copy in its matrix job — but kept for local testing / ad-hoc syncs.

```bash
python sync_to_destination.py \
  --source source-repo/api-docs/public \
  --destination openapi/product \
  --changed-list changed_files.txt
```

---

## Deprecated

### `create_individual_prs.py`

**Do not use.** This predated the matrix-based workflow in `sync-api-docs.yml`. It produces one PR per YAML but never invokes the nav-generation action, so PRs it creates leave `docs.json` stale. The matrix job in `sync-api-docs.yml` replaces it. Candidate for deletion — left in place only to avoid surprise during this transition.

---

## Workflow

See `.github/workflows/sync-api-docs.yml`. High-level flow:

1. `detect` job finds changed YAMLs and emits them as a JSON array.
2. `sync-file` matrix job fans out: one parallel-capped job per changed file.
3. Each matrix job: copies the YAML into `openapi/product/`, runs `DomoApps/documentation-generator-action@main` against that single file, opens a PR containing just that YAML and its `docs.json` nav update.

## Requirements

- Python 3.7+
- GitHub App installed on both source and destination repos (`APP_ID`, `APP_PRIVATE_KEY` secrets).
