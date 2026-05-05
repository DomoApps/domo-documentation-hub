---
name: openapi-sync-workflow
user-invocable: true
description: "work on the OpenAPI sync GitHub Action, debug sync-api-docs.yml, modify the detect/sync/PR Python scripts, change how YAMLs from internal-domo-apis are pulled into openapi/product, or update docs.json nav-generation integration"
---

Engineer skill for working on the **OpenAPI Sync** GitHub Action in this repo.

Before editing, read the pieces you're touching and understand the data flow end-to-end.

---

## What the action does

Scheduled workflow (every 6 hours, plus `workflow_dispatch` and `repository_dispatch: openapi-updated`) with two jobs:

### Job 1: `detect`
1. Auths to the source repo (`domoinc/internal-domo-apis`) via a GitHub App.
2. Clones source alongside this repo.
3. Runs `detect_yaml_changes.py`, which compares source vs. destination YAMLs by **SHA-256 content hash** and writes `changed_files.txt`.
4. Emits the file list as a JSON array output for the matrix job.

### Job 2: `sync-file` (matrix, one job per changed file)
For each changed YAML:
1. Re-auths to both repos.
2. Checks out this repo and clones source.
3. Copies the single YAML into `openapi/product/` (case-variant duplicates in the destination are removed first).
4. Runs `DomoApps/documentation-generator-action@main` with `process_changed_only: true` scoped to that one file, updating its entry in `docs.json`.
5. Runs `prune_stale_nav.py` to remove any OpenAPI nav entries in `docs.json` that point at YAMLs no longer on disk (case-renames, upstream deletes) — otherwise Mintlify preview deploys fail trying to resolve missing specs.
6. Opens a dedicated PR via `peter-evans/create-pull-request@v5` with branch `openapi-sync/<slug>` containing the YAML + nav edits + any cleanup.

### Job 3: `summary`
Always runs; writes a step summary.

---

## File map

| File | Role |
|---|---|
| `.github/workflows/sync-api-docs.yml` | The workflow. All orchestration + env config. |
| `.github/scripts/detect_yaml_changes.py` | Content-hash diff; writes `changed_files.txt`. |
| `.github/scripts/prune_stale_nav.py` | Strips OpenAPI nav entries from `docs.json` whose YAML is missing on disk. Case-sensitive check (dev repo on macOS / APFS gives false-negatives with `os.path.isfile`). |
| `.github/scripts/sync_to_destination.py` | Standalone copy helper. **Not called by the workflow** — retained for local/ad-hoc use. |
| `.github/scripts/create_individual_prs.py` | **Deprecated.** Predated the matrix flow; doesn't regenerate nav. Candidate for deletion. |
| `.github/scripts/README.md` | Script-level docs. |
| `openapi/product/` | Destination for synced YAMLs. |
| `docs.json` | Nav manifest; rewritten by the external action. |

---

## Important design choices / gotchas

1. **Content-hash detection.** `detect_yaml_changes.py` uses SHA-256, not mtime. Any "changes not detected" debugging should start by running the script locally against the two directories and inspecting its output.
2. **Matrix fan-out, not a single PR.** Each changed YAML gets its own PR. Pros: reviewable in isolation, can merge one without blocking others. Cons: concurrent PRs modifying `docs.json` can conflict. `max-parallel: 3` and `process_changed_only: true` minimize — but don't eliminate — conflict risk. When two PRs' nav edits overlap, the second merge needs a rebase (or re-trigger the workflow, which will re-detect and re-open).
3. **Branch naming.** `openapi-sync/<slug>` where `<slug>` is a lowercased, punctuation-normalized filename stem. Same file → same branch → existing PR is updated. Renaming the YAML will create a new branch/PR.
4. **Case-only renames** (e.g. `Foo.yaml` → `foo.yaml`) are flagged as modifications by the detector. The copy step deletes the old-cased destination file with `find -iname ... -delete` before `cp`ing the new casing in. The PR step's `add-paths` MUST include the full dest directory (not just the new file path) so that the deletion is staged alongside the addition — otherwise the PR ends up with both case-variants in the branch.
5. **External nav action pinned to `@main`.** `DomoApps/documentation-generator-action@main` can shift under us. If nav output changes unexpectedly, consider pinning to a SHA.
6. **Cross-repo auth needs the GitHub App installed on `domoinc/internal-domo-apis`.** Failures at "Generate Source Repo Token" mean the app was uninstalled or its permissions shifted.
7. **`create_individual_prs.py` is dead code.** Do not wire a new workflow to it — it skips the nav update and leaves `docs.json` inconsistent with the synced YAMLs. Either delete it or rewrite it to invoke the nav action per file (but the matrix job already does that natively, so deletion is preferred).

---

## Playbook: common tasks

### "Sync isn't picking up changes"
1. Manually trigger `workflow_dispatch` with `force_sync: true`.
2. Check the `detect` job's "Detect Changed YAML Files" step. Does it list the expected file under NEW/MODIFIED?
3. If still UNCHANGED: diff the files locally with `sha256sum` to confirm they really differ on disk. If they do but the workflow disagrees, check whether the source path (`SOURCE_YAML_PATH`) still points at the right directory in `internal-domo-apis`.

### "PR opened but docs.json didn't update"
Look at the matrix job's `Update API Navigation` step for that specific file. If it ran but produced no diff, the issue is inside `DomoApps/documentation-generator-action` — check its logs and confirm `openapi_base_path` matches where the YAML landed. If the nav step failed, the PR step still ran and may have opened a PR with the YAML only — close it and re-trigger.

### "Two PRs conflict on docs.json"
Expected when spec entries live in the same nav region. Merge one, then either rebase the other(s) onto `main` or re-trigger the workflow (which will regenerate both nav edits against the updated `docs.json`).

### "Want to change the source repo / path / schedule"
Everything lives in the `env:` block at the top of `sync-api-docs.yml`. Don't scatter new config elsewhere.

### "Add a post-sync step (linting, validation, Slack notification)"
Add it inside the `sync-file` matrix job (runs per file) or inside `summary` (runs once at the end). Gate matrix-internal steps carefully — a matrix-level `if:` on an output that only the `detect` job produces needs `needs.detect.outputs.*`, not `steps.*`.

---

## Working rules for this skill

- **Workflow edits:** preserve the `detect → sync-file (matrix) → summary` shape. If you flatten it back to a single job, you lose per-file PRs.
- **Python script edits:** scripts are standalone (no shared module). Keep them that way.
- **Test locally when possible:** `detect_yaml_changes.py` runs against any two local directories with no GitHub context. Exercise it before pushing workflow changes.
- **Don't touch `openapi/product/` contents by hand in the same PR as workflow changes** — it muddies review.
- **After any workflow change, suggest a `workflow_dispatch` dry-run** on a branch before merging, so the user sees a real run before trusting cron.
- **Don't revive `create_individual_prs.py`** — the matrix job in the workflow does everything it did, plus updates `docs.json`.
