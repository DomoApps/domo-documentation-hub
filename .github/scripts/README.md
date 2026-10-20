# OpenAPI Sync Scripts

Helper scripts for `.github/workflows/sync-api-docs.yml`. That workflow runs when the api-registry pipeline (pipeline-shared-library `generateApiV4`) pushes published public API YAMLs to an `openapi-sync/<service>` branch. It regenerates the `docs.json` navigation, prunes stale entries, and opens a PR into `main`. Only `prune_stale_nav.py` is still used by it.

## Active scripts

### `detect_yaml_changes.py` (no longer used by the workflow)

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

### `sync_to_destination.py` (no longer used by the workflow)

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

1. The api-registry pipeline copies the published YAMLs into `openapi/product/` on a branch named `openapi-sync/<service>` (cut from `main`) and force-pushes it.
2. The push triggers the workflow (only when files under `openapi/product/` changed).
3. It finds YAMLs that differ from `main`, runs `DomoApps/documentation-generator-action@main` on them to update `docs.json`, then runs `prune_stale_nav.py`.
4. Nav changes are committed to the same branch, and a PR into `main` is opened if one isn't already open. Later pipeline runs for the same service update the existing PR.

## Requirements

- Python 3.7+
- GitHub App installed on this repo (`APP_ID`, `APP_PRIVATE_KEY` secrets).
