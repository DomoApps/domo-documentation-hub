# DomoStats connector-to-docs schema sync

## Context

`s/article/360043433813.mdx` (DomoStats Connector) documents 115 reports and ~982 field
descriptions that must track the connector's Java source in `dev-org/domostats`. Today that
tracking is manual. The audit in PR #414 found 20 of 110 field tables materially wrong: missing
columns, stale enum values, reports absent entirely, and 31 feature-switch notes that were
misleading. That audit took days and will decay again within a release or two.

Two things now make automation worth building:

1. `Column` supports a 3-arg `Column(name, type, description)` constructor, and **272 of 1,062
   call sites already use it** across 29 files. The connector is becoming authoritative for
   descriptions, not just names and types. Bryce confirmed the description arg will be filled in
   going forward.
2. This repo already runs the exact pipeline shape needed: `.github/workflows/sync-api-docs.yml`
   does upstream-notify → App token → clone source → detect → regenerate → PR.

**Outcome:** a connector schema change produces a draft PR against `main` with the English field
tables already updated, new descriptions drafted, and everything a human must still decide listed
in the PR body. Nobody hand-diffs Java against MDX again.

## Decisions taken

| Decision | Choice |
| --- | --- |
| Manifest extraction | Gradle task in domostats, run on Jenkins |
| New columns with no source description | Claude drafts them in CI |
| Japanese mirror | English only; flag drifted JA sections on the PR |
| Removals | Report in the PR body, never delete automatically |

## The comparison contract

Java description strings are plain text that never renders. The docs keep Markdown presentation.
The two sides are **deliberately not byte-identical** and are compared on a normalized form:

```python
def normalize(s):
    s = s.replace('`', '')            # docs code-format enum values; the source can't
    s = re.sub(r'\s+', ' ', s).strip()
    return s.rstrip('.')              # docs terminate sentences; the source doesn't
```

The Role Grants section (`### Role Grants`, EN L1589) is the validated reference: all six rows
differ raw and match normalized. Any reconciler change must keep that section reporting clean.

**The single most important safety rule:** 790 of 1,062 columns still have no source description.
When the manifest description is empty, the existing doc description is authoritative and must be
left untouched. Only overwrite when the source has a description *and* the normalized forms differ.

## Part 1 — `dev-org/domostats`: emit the manifest

### Why this is not pure reflection

`Report` exposes no `getSchema()`. Schemas live as static fields on the Row/DataSet classes and are
passed into `SimpleReport.write(limit, schema, ...)` at fetch time
(`src/main/java/com/domo/connector/domostats/SimpleReport.java:52`). So a `Report` instance cannot
be asked for its schema without running it against the network. The extractor is therefore a hybrid:
reflection for values, source parse for structure.

### New files

- `src/tooling/java/com/domo/connector/domostats/tooling/SchemaManifestGenerator.java`
- `domostats-schema.json` (generated, committed)
- `build.gradle`: a `tooling` source set plus a `JavaExec` task `generateSchemaManifest` wired to
  the main runtime classpath

### What the generator does

**a. Schemas — reflection, exact.** Walk `build/classes/java/main`, load each class, collect every
`public static final List<Column>` field regardless of name. This handles all eight observed field
names (`schema`, `SCHEMA`, `columns`, `schemaAdv`, `inputSchema`, `outputSchema`, `metricsSchema`,
`metricsData`) with no special-casing, and picks up descriptions and `DataType` for free. Emit keyed
by declaring class FQN + field name.

**b. Report registry — source parse, constants resolved reflectively.** Parse
`discovery/ReportListCommand.java` for:

- `response.addOption("key", "Display Name")` and `response.addOption(XReport.NAME, XReport.DISPLAY_NAME)`
- gating context: the `switch (environment)`, `switch (customerName)`, and `CustomerFilter` blocks
- `requiresEnabled("feature-switch").forReports(key, label)` chains (L233-255), which give
  per-report feature-switch gating declaratively

Constant references resolve by reading the compile-time constants off the loaded classes (119
`NAME`/`DISPLAY_NAME` constants exist). Parse `ProcessRecords.java`'s 59-case switch for
key → Report class.

**c. Bind report key to schema.** In order: a `SCHEMA` static on the Report class itself; then
convention (`XReport` → `XRow`, `XDataSet`); then emit `"schema": null, "unresolved": true`. The
docs side reports unresolved reports in the PR body rather than failing. Connector devs can make a
report resolve cleanly by adding one line — `public static final List<Column> SCHEMA = XRow.schema;`
— which is worth suggesting but is explicitly **not** a prerequisite.

### Manifest shape

```json
{
  "generatedFrom": "<git sha>",
  "reports": [
    {
      "key": "certifiedAttributesUsage",
      "displayName": "Certified Attributes Usage",
      "reportClass": "...CertifiedAttributesUsageReport",
      "schemaClass": "...CertifiedAttributesUsageRow",
      "gating": { "featureSwitch": "certified-attributes", "environments": null, "customers": null },
      "unresolved": false,
      "columns": [ { "name": "Object Type", "type": "STRING", "description": "" } ]
    }
  ]
}
```

### Transport

Jenkins runs `./gradlew generateSchemaManifest` on master and commits `domostats-schema.json` back
if it changed. Committing (rather than publishing to Nexus) means the docs hub only needs a `git
clone`, matching how `sync-api-docs.yml` reads YAMLs out of `source-repo/`, and it gives connector
reviewers a readable schema diff in their own PRs.

Optionally Jenkins also `curl`s a `repository_dispatch` of type `domostats-schema-updated` to the
docs hub for instant sync. Not required for v1 — cron covers it.

## Part 2 — `domo-documentation-hub`: reconcile and open the PR

### `.github/workflows/sync-domostats-schema.yml`

Modelled directly on `sync-api-docs.yml`:

- Triggers: nightly `schedule`, `workflow_dispatch` (with a `force` input), and
  `repository_dispatch: [domostats-schema-updated]`
- Two `actions/create-github-app-token@v1` blocks with `secrets.APP_ID` / `secrets.APP_PRIVATE_KEY`
  — source-scoped for the clone, dest-scoped for the PR. **The App must be installed on
  `domo-development/domostats`**; this is the one external prerequisite.
- `actions/checkout@v4` twice, source at `path: source-repo`
- `actions/setup-python@v5`, `python-version: "3.12"`, then `pip install anthropic` (the repo's
  first CI pip install; pin the version)
- Single job, no matrix. Unlike the OpenAPI sync there is exactly one target article, so
  fan-out and the `max-parallel: 3` docs.json conflict workaround are unnecessary.
- `peter-evans/create-pull-request@v5` with the **dest App token** (so `mint-preview.yml` fires —
  see the comment at `sync-video-library.yml:89`), `branch: domostats-sync/schema`,
  `delete-branch: true`, `draft: true`, `add-paths: s/article/360043433813.mdx`
- A stable branch name means a re-run updates the open PR instead of stacking duplicates.
- `$GITHUB_STEP_SUMMARY` block mirroring the existing `summary` job.

### `.github/scripts/reconcile_domostats.py`

CLI: `--manifest`, `--article`, `--ja-article`, `--report-json`, `--dry-run`, `--no-draft`.

Reuse from `.github/scripts/detect_yaml_changes.py`: the `GITHUB_OUTPUT` `<<EOF` heredoc writer
(L143-150) and the stdlib-only, argparse-with-string-`--force` style. Do **not** touch
`create_individual_prs.py` — it is deprecated.

**Parse.** The writable region is `## DataSet Fields` (EN L170) to EOF. Within it, each report is
`### <Display Name>`, an optional `<Note>`, and one `| Field | Description |` table.

**Apply automatically:**
- Column added → new row inserted at its schema-order position
- Column description changed → cell replaced, but only if the source description is non-empty and
  normalized forms differ
- Column reordered → rows reordered to match schema order
- Report added → new `###` section, its table, and a matching Details Pane row

**Report only, never apply:**
- Column or report removed
- Report present in the article but `unresolved` in the manifest
- Report gated by an environment or customer allowlist the parser could not fully evaluate
- Any structural anomaly listed below

**Structural invariants the rewriter must honor** (all verified present today):

| Invariant | Detail |
| --- | --- |
| Section order is curated, not sorted | `Domo Goals \| *` and `PDP - *` are hand-ordered blocks. Never `sorted()`. Insert new sections alphabetically outside those blocks; append inside them. |
| Two indexes per report | The Details Pane table (EN L28-144) and the `###` section. The pane escapes pipes as `&#124;`; the heading uses a literal `\|`. |
| Prose-bearing sections | `Beast Modes used in Beast Modes`, `Certified Content`, `Domo Goals \| Goals`, `People` carry prose before or after the table. Rewrite the table only. |
| `Upgrade Path Conversions` has no table | Schema is built at run time. Skip it. |
| `Task Center` has a broken header | Empty header row, with `\| **Field** \| **Description** \|` as the first data row. Detect and skip, do not crash or "fix". |
| Header style varies | 99 tables plain, 14 bolded. Preserve per-section. |
| Two inline `<Note>` cells | Details Pane rows for `DataFlows History` and `Workflows`. |
| Notes are never generated | 41 callouts exist. Feature-switch note wording was hand-audited in PR #414 (31 removed because the switch defaults on). The reconciler must not add, remove, or reword them; new gating goes in the PR body as a suggestion. |

**Hard guard:** `scripts/pad_md_tables.py` does a plain `split("|")` with no escape handling, so an
escaped `\|` in a cell splits it and adds a phantom column to the whole table. Abort with a clear
error if the article contains `\|` inside the writable region. (None today.)

### Description drafting

For each new column with no source description, one Anthropic call with the column name, `DataType`,
the report's Java class, and the neighboring rows for tone. Constrain hard: one sentence, match
surrounding voice, no invented enum values.

Any column whose name or type suggests an enum gets its drafted description plus an inline
`<!-- verify enum values -->` marker and a line in the PR body checklist. This is the known weak
spot: enum lists live in `convertToString` methods, not in the schema, and the model cannot see them.

Needs a new `ANTHROPIC_API_KEY` repo secret. `scripts/add_excerpts.py` is the in-repo reference for
the client usage pattern.

### Final steps

Run `python3 scripts/pad_md_tables.py s/article/360043433813.mdx`. It is idempotent and correctly
uses East-Asian display width, so it is safe on `ja/` too.

For Japanese: compare section and row counts against the English file and post a PR comment naming
the drifted sections, to be run through the `localize` skill after the English is approved. Do not
edit `ja/`.

### PR body

Generated from the reconciler's report JSON: applied changes, TODO/verify checklist, removals
awaiting a human, unresolved reports, and JA sections needing localization.

## Verification

1. **Normalization unit tests.** Cover the Role Grants six-row case: raw-different,
   normalized-equal. Include a case where the source description is empty and assert the doc
   description survives untouched.
2. **Golden no-op.** Generate the manifest from domostats master, run the reconciler against the
   current article with `--dry-run`, and confirm the ~90 already-correct tables produce **zero**
   diff. Any churn here is a parser bug, not a real change.
3. **Synthetic change.** Run against the `users/bryce-cindrich/DOMO-492939-role-grants-columns`
   branch, which adds Grant ID, Category, and Admin Level with descriptions. Expected: exactly
   those three rows appended in schema order with no other edit. PR #414 already contains the
   hand-written correct answer to diff against.
4. **Anomaly suite.** Assert the reconciler leaves `Task Center`, `Upgrade Path Conversions`, the
   four prose-bearing sections, and the 14 bold-header tables byte-identical.
5. **Structural parity.** After any run: `grep -cE '^#{2,4} '` = 122 and `grep -cE '^\|'` on both
   locales, plus `python3 scripts/pad_md_tables.py` reporting `no change` on a second invocation.
6. **End to end.** `workflow_dispatch` with `force`, confirm the draft PR opens, `mint-preview.yml`
   fires on it (proving the App token is wired correctly), and the preview renders the tables.

## Build order

1. Gradle task + manifest, committed to domostats. Useful alone as a diffable per-release schema
   record, before any docs automation exists.
2. `reconcile_domostats.py` with `--dry-run`, validated against tests 1-4 locally.
3. The workflow, on `workflow_dispatch` only, opening draft PRs.
4. Claude description drafting.
5. Enable cron, and add the Jenkins `repository_dispatch` curl if instant sync is wanted.

## Open prerequisites

- GitHub App installed on `domo-development/domostats` (blocks the clone; also check SAML/SSO
  authorization).
- `ANTHROPIC_API_KEY` secret added to `DomoApps/domo-documentation-hub`.
- Connector team sign-off on the Gradle task and on Jenkins committing a generated file to master.
