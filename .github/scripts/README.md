# CI Sync Scripts

Helper scripts used by the sync workflows in `.github/workflows/`:

- **OpenAPI sync** (`sync-api-docs.yml`) pulls OpenAPI YAMLs from `domoinc/internal-domo-apis` into `openapi/product/` and updates `docs.json` navigation. See `detect_yaml_changes.py`, `prune_stale_nav.py`, `sync_to_destination.py`.
- **DomoStats schema sync** (`sync-domostats-schema.yml`) reconciles the DomoStats Connector KB article against the connector's generated schema manifest. See `reconcile_domostats.py`.

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
- Comparison is by content hash, not mtime. `actions/checkout` resets mtimes on both clones, which makes mtime comparison unreliable.
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

Standalone helper that copies YAMLs from a list into a destination directory, removing any case-variant duplicates. **Not invoked by `sync-api-docs.yml` directly** (the workflow inlines a single-file copy in its matrix job), but kept for local testing and ad-hoc syncs.

```bash
python sync_to_destination.py \
  --source source-repo/api-docs/public \
  --destination openapi/product \
  --changed-list changed_files.txt
```

---

### `reconcile_domostats.py`

Reconciles `s/article/360043433813.mdx` (DomoStats Connector) against `domostats-schema.json`, the manifest generated in `domo-development/domostats` by `./gradlew generateSchemaManifest` and committed there by Jenkins.

```bash
python3 .github/scripts/reconcile_domostats.py \
  --manifest source-repo/domostats-schema.json \
  --article s/article/360043433813.mdx \
  --ja-article ja/s/article/360043433813.mdx \
  --config .github/domostats-sync-config.json \
  --report-json domostats-report.json \
  --pr-body domostats-pr-body.md \
  --dry-run
```

**Arguments:**

| Flag | Meaning |
| --- | --- |
| `--manifest` | Path to `domostats-schema.json` (required) |
| `--article` | English article. Default `s/article/360043433813.mdx` |
| `--ja-article` | Japanese mirror. Checked for drift, **never edited** |
| `--config` | Sync config (`excludedReportKeys`, `excludedSections`). Default `.github/domostats-sync-config.json` |
| `--report-json` | Write the machine-readable reconciliation report here |
| `--pr-body` | Write the rendered PR body markdown here |
| `--dry-run` | Compute everything, write no article |
| `--descriptions` | `safe` (default), `source-wins`, or `report-only` (see below) |
| `--no-redact` | Name undocumented reports in the output. Only safe when the output stays private |
| `--draft-descriptions` | Ask Claude to draft descriptions for new columns the connector left blank. Needs `ANTHROPIC_API_KEY` |
| `--model` | Drafting model. Default `claude-sonnet-5` |

**Exit codes:** `0` reconciled, `1` refused (a structural invariant does not hold), `2` bad input.

#### The comparison contract

Java description strings are plain text that never renders; the article keeps Markdown presentation. The two sides are **deliberately not byte-identical** and are compared on a normalized form: backticks stripped, whitespace collapsed, trailing periods dropped, casing ignored.

The single most important safety rule: **when the manifest description is empty, the article's description is authoritative and is left untouched.** Most columns still have no source description, so treating an empty source string as "clear the docs" would erase most of the article.

`--descriptions` picks what happens when both sides have a description and they differ:

- `safe` (default) replaces the article's with the connector's, restyled to house style, **unless** doing so would drop values the article code-formats or shorten the cell substantially. Those are reported instead. This exists because the article was hand-audited in PR #414 and several of its cells enumerate enum members the Java string does not carry.
- `source-wins` always replaces.
- `report-only` never replaces; every difference goes in the PR body.

#### This repository is public, the connector repository is not

Two behaviours exist because of that asymmetry, and neither should be relaxed while this repo is public.

**Gating is recorded as a kind, never as a value.** `ReportListCommand` gates reports on named Domo customers (`stravello`, `fidelity`, the `mmmm-*` CIDs) and on internal environment names (`demo1`, `gastage1`, `prod2`). The generator records only `restrictionKinds: ["customer-allowlist"]` and friends, so the allowlist contents never leave the connector repo. The reconciler only ever needs to know whether a human has to look, which the kind answers.

**A new report is opt-in.** Domo cuts a release branch about six weeks before customers see a feature, so a report can sit in the connector long before it ships. Auto-proposing a section would announce it in a public draft PR the night it merges to the connector's master. Under the default `newReportPolicy: "opt-in"`, a section is generated only once its key is in `documentedReportKeys`, and until then the report's name is withheld from the PR body and the report JSON: only a count and a category surface. Column-level changes to reports the article already documents flow automatically, because those reports are already public.

Consequences for the workflow: the report JSON is **not** uploaded as an artifact (artifacts on a public repo are world-readable), and `--no-redact` must never be passed in CI.

#### What it applies vs. reports

Applied automatically: a column the connector has and the article does not (inserted at its schema position); a changed description (subject to `--descriptions`); row order when every article row maps to a manifest column; a whole new report section plus its Details Pane row, when the report is generally available and its schema resolved.

Reported and never applied: removals of any kind, reports with no resolvable schema, restricted reports, name drift, duplicated connector columns, Details Pane index drift, and Japanese sections whose row counts no longer match English. Callouts are never added, removed, or reworded: their wording was hand-audited, so new gating goes in the PR body as a suggestion.

Connector class names do appear in the PR body, but only for reports the article already documents, so they never disclose an unreleased feature.

#### Structural invariants it honors

- Section order is curated, not sorted. `Domo Goals | *` and `PDP - *` are hand-ordered blocks; new members are appended to the block and the search never lands inside one.
- Every report appears twice: as a Details Pane row (pipes escaped `&#124;`) and as a `###` section.
- Prose-bearing sections (`Beast Modes used in Beast Modes`, `Certified Content`, `Domo Goals | Goals`, `People`) keep their prose; only the table is rewritten.
- `Upgrade Path Conversions` has no table (its schema is built at run time) and is skipped.
- `Task Center` has an empty header row with `| **Field** | **Description** |` as its first data row. It is detected and skipped, never "fixed".
- Header style varies per section (99 plain, 14 bolded) and is preserved.

**Hard guard:** `scripts/pad_md_tables.py` splits cells on a plain `|` with no escape handling, so an escaped `\|` inside a cell would gain a phantom column on the next padding run. The reconciler refuses with exit 1 if it finds one inside `## DataSet Fields`. Use `&#124;` instead.

#### Tests

```bash
python3 -m unittest discover -s .github/scripts/tests -t .github/scripts/tests
```

Stdlib-only, no network. Fixtures under `tests/fixtures/` are real slices of the article and the manifest chosen to cover every anomaly above. `article-baseline.mdx` is converged: reconciling it against `manifest-baseline.json` must produce **zero** diff, so any churn there is a parser bug rather than a real change. The synthetic-change test reconstructs PR #414's hand-written Role Grants table byte-for-byte from the `DOMO-492939` connector branch's schema.

---

## Deprecated

### `create_individual_prs.py`

**Do not use.** This predated the matrix-based workflow in `sync-api-docs.yml`. It produces one PR per YAML but never invokes the nav-generation action, so PRs it creates leave `docs.json` stale. The matrix job in `sync-api-docs.yml` replaces it. Candidate for deletion; left in place only to avoid surprise during this transition.

---

## Workflows

### `sync-api-docs.yml`

1. `detect` job finds changed YAMLs and emits them as a JSON array.
2. `sync-file` matrix job fans out: one parallel-capped job per changed file.
3. Each matrix job: copies the YAML into `openapi/product/`, runs `DomoApps/documentation-generator-action@main` against that single file, opens a PR containing just that YAML and its `docs.json` nav update.

### `sync-domostats-schema.yml`

Triggered by a `domostats-schema-updated` repository dispatch from Jenkins, nightly on a schedule, or manually.

1. Mint a source-scoped and a dest-scoped App token, clone `domo-development/domostats`, and read `domostats-schema.json` out of it.
2. Run the reconciler test suite, then `reconcile_domostats.py` against `s/article/360043433813.mdx`.
3. Open a **draft** PR on the stable branch `domostats-sync/schema`, with the reconciler's report rendered as the PR body. A re-run updates the same PR instead of stacking duplicates. Nothing else is published: no artifacts, and the step summary carries counts only.

The PR is opened with the dest App token rather than `GITHUB_TOKEN` so that `mint-preview.yml` fires on it. See the comment at `sync-video-library.yml:89`.

Japanese is never edited here. The workflow reports which `ja/` sections drifted; run the `localize` skill on them after the English is approved.

## Requirements

- Python 3.7+ (the DomoStats reconciler needs 3.9+ for builtin generic annotations).
- GitHub App installed on both source and destination repos (`APP_ID`, `APP_PRIVATE_KEY` secrets).
- For the DomoStats sync, the App must additionally be installed on `domo-development/domostats` (check SAML/SSO authorization), and `ANTHROPIC_API_KEY` must be set for description drafting. Without the key the workflow still runs and leaves new descriptions as `TODO`.
