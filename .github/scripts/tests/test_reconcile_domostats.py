#!/usr/bin/env python3
"""
Tests for .github/scripts/reconcile_domostats.py.

Run from the repo root:

    python3 -m unittest discover -s .github/scripts/tests -v

Stdlib only, no pytest, no network. The fixtures under `fixtures/` are real slices of
`s/article/360043433813.mdx` and of `domostats-schema.json`, chosen to cover every
structural anomaly the reconciler has to survive:

    Accounts                          plain header, plain table
    Activity Log                      bold header, escaped underscores in field names
    Beast Modes used in Beast Modes   prose before the table
    Certified Content                 prose after the table
    Domo Goals | Goals                curated block, Note plus prose, literal pipe
    Domo Goals | Goal Owners          curated block member
    PDP - Column Policies             curated block
    PDP - Row Policies                curated block
    People                            bold header plus prose
    Role Grants                       the synthetic-change target
    Roles                             plain
    Task Center                       empty header row (documented anomaly)
    Upgrade Path Conversions          no table at all (schema built at run time)
    Usage Metrics                     feature-switch Note

`article-baseline.mdx` is converged: reconciling it against `manifest-baseline.json`
must produce no diff at all. Any churn there is a parser bug, not a real change.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
REPO = SCRIPTS.parent.parent
FIXTURES = HERE / "fixtures"

sys.path.insert(0, str(SCRIPTS))

import reconcile_domostats as rd  # noqa: E402

BASELINE = FIXTURES / "article-baseline.mdx"
MANIFEST = FIXTURES / "manifest-baseline.json"
ROLEGRANTS_MANIFEST = FIXTURES / "manifest-rolegrants.json"
ROLEGRANTS_BEFORE = FIXTURES / "article-rolegrants-before.mdx"


def run(article: Path, manifest: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "reconcile_domostats.py"),
            "--manifest",
            str(manifest),
            "--article",
            str(article),
            "--ja-article",
            str(article.parent / "does-not-exist.mdx"),
            "--config",
            str(article.parent / "does-not-exist.json"),
            *extra,
        ],
        capture_output=True,
        text=True,
        cwd=REPO,
        check=False,
    )


def sections(text: str) -> dict[str, str]:
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if re.match(r"^###\s+\S", line)]
    out = {}
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        out[lines[start][3:].strip()] = "\n".join(lines[start:end]).rstrip()
    return out


# ---------------------------------------------------------------------------
# 1. Normalization: the comparison contract
# ---------------------------------------------------------------------------


class TestNormalization(unittest.TestCase):
    def test_backticks_whitespace_and_terminal_period_are_presentation(self):
        docs = "The grant's category as a raw enum value, for example `USERS_GROUPS`."
        source = "The grant's category as a raw enum value, for example USERS_GROUPS"
        self.assertNotEqual(docs, source)
        self.assertEqual(rd.normalize(docs), rd.normalize(source))

    def test_role_grants_rows_differ_raw_and_match_normalized(self):
        """The validated reference case: all six rows differ raw, match normalized."""
        manifest = json.loads(ROLEGRANTS_MANIFEST.read_text(encoding="utf-8"))
        report = next(
            r for r in manifest["reports"] if r["displayName"] == "Role Grants"
        )
        article = sections(BASELINE.read_text(encoding="utf-8"))["Role Grants"]
        cells = {
            row[0]: row[1]
            for row in (
                rd.split_row(line)
                for line in article.split("\n")
                if line.startswith("|")
            )
            if len(row) > 1
        }
        self.assertEqual(len(report["columns"]), 6)
        for column in report["columns"]:
            docs = cells[column["name"]]
            source = column["description"]
            self.assertNotEqual(docs, source, column["name"])
            self.assertEqual(rd.normalize(docs), rd.normalize(source), column["name"])

    def test_trailing_periods_are_dropped_but_internal_ones_are_kept(self):
        self.assertEqual(rd.normalize("Ends here."), "Ends here")
        self.assertEqual(rd.normalize("Two sentences. And a second."), "Two sentences. And a second")

    def test_field_keys_tolerate_case_and_separator_drift(self):
        self.assertEqual(
            rd.normalize_field("Task identifier"), rd.normalize_field("Task Identifier")
        )
        self.assertEqual(rd.normalize_field("Account_Id"), rd.normalize_field("Account Id"))
        self.assertEqual(
            rd.normalize_field("\\_BATCH_ID\\_"), rd.normalize_field("_BATCH_ID_")
        )
        # Separator-blind matching is a fallback key, deliberately distinct.
        self.assertNotEqual(
            rd.normalize_field("PageIds"), rd.normalize_field("Page Ids")
        )
        self.assertEqual(rd.squash_field("PageIds"), rd.squash_field("Page Ids"))

    def test_report_keys_tolerate_a_trailing_report_suffix(self):
        self.assertEqual(
            rd.normalize_report("AI Readiness Report"), rd.normalize_report("AI Readiness")
        )
        self.assertEqual(
            rd.normalize_report("Domo Goals &#124; Goals"),
            rd.normalize_report("Domo Goals | Goals"),
        )


# ---------------------------------------------------------------------------
# 2. The safety rule: an empty source description never overwrites the docs
# ---------------------------------------------------------------------------


class TestEmptySourceDescription(unittest.TestCase):
    def test_empty_source_leaves_the_article_untouched(self):
        column = rd.ManifestColumn("Role ID", "INTEGER", "")
        updates: list[dict] = []
        kept = rd._resolve_description(
            column, "Unique identifier of the role.", "safe", "Role Grants", updates
        )
        self.assertEqual(kept, "Unique identifier of the role.")
        self.assertEqual(updates, [])

    def test_whitespace_only_source_counts_as_empty(self):
        column = rd.ManifestColumn("Role ID", "INTEGER", "   \n  ")
        updates: list[dict] = []
        kept = rd._resolve_description(column, "Docs wording.", "safe", "R", updates)
        self.assertEqual(kept, "Docs wording.")
        self.assertEqual(updates, [])

    def test_most_baseline_columns_have_no_source_description(self):
        """Guards the premise: if this ever inverts, revisit the safety rule."""
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        total = sum(len(r["columns"] or []) for r in manifest["reports"])
        described = sum(
            1
            for r in manifest["reports"]
            for c in (r["columns"] or [])
            if c["description"]
        )
        self.assertGreater(total, 0)
        self.assertLess(described, total)


# ---------------------------------------------------------------------------
# 3. Description replacement: house style in, regressions out
# ---------------------------------------------------------------------------


class TestDescriptions(unittest.TestCase):
    def test_restyle_keeps_code_formatting_the_article_had(self):
        existing = "The status. Values: `OPEN`, `CLOSED`."
        source = "The status of the goal. Values: OPEN, CLOSED, EXPIRED"
        styled = rd.restyle(source, existing)
        self.assertIn("`OPEN`", styled)
        self.assertIn("`CLOSED`", styled)
        self.assertTrue(styled.endswith("."))

    def test_restyle_swaps_quotes_for_backticks_rather_than_nesting(self):
        styled = rd.restyle('Indicates whether it is "Yes" or "No"', "Options: `Yes` or `No`")
        self.assertIn("`Yes`", styled)
        self.assertNotIn('"`Yes`"', styled)

    def test_restyle_removes_en_and_em_dashes(self):
        styled = rd.restyle("An integer (0–100)", "An integer.")
        self.assertNotIn("–", styled)
        self.assertIn("0-100", styled)

    def test_restyle_applies_domo_product_capitalization(self):
        styled = rd.restyle("The id of the dataset that powers the dataflow", "x.")
        self.assertIn("DataSet", styled)
        self.assertIn("DataFlow", styled)

    def test_regression_detected_when_the_source_drops_documented_values(self):
        existing = (
            "Displays the status. Values: `COMPLETED`, `FAILED`, `IN_PROGRESS`, "
            "`CANCELLED`, `NOT_STARTED`."
        )
        source = "Displays the status of the workflow execution"
        self.assertIsNotNone(rd.description_regression(source, existing))

    def test_regression_detected_when_the_source_is_much_shorter(self):
        existing = (
            "A timestamp for the last time this user logged in. Login is measured by any "
            "regular, SSO, or mobile login."
        )
        self.assertIsNotNone(rd.description_regression("Last login", existing))

    def test_no_regression_when_the_source_keeps_every_value(self):
        existing = "The type. Values: `USER`, `GROUP`."
        source = "Whether the entity is a USER or a GROUP"
        self.assertIsNone(rd.description_regression(source, existing))

    def test_safe_mode_reports_a_regression_instead_of_applying_it(self):
        column = rd.ManifestColumn(
            "Workflow Status", "STRING", "Displays the status of the workflow execution"
        )
        existing = "Displays the status. Values: `COMPLETED`, `FAILED`, `IN_PROGRESS`."
        updates: list[dict] = []
        kept = rd._resolve_description(column, existing, "safe", "Workflows", updates)
        self.assertEqual(kept, existing)
        self.assertEqual(len(updates), 1)
        self.assertFalse(updates[0]["applied"])
        self.assertIn("documents values", updates[0]["reason"])

    def test_source_wins_mode_applies_the_same_regression(self):
        column = rd.ManifestColumn(
            "Workflow Status", "STRING", "Displays the status of the workflow execution"
        )
        existing = "Displays the status. Values: `COMPLETED`, `FAILED`, `IN_PROGRESS`."
        updates: list[dict] = []
        kept = rd._resolve_description(
            column, existing, "source-wins", "Workflows", updates
        )
        self.assertNotEqual(kept, existing)
        self.assertTrue(updates[0]["applied"])

    def test_report_only_mode_never_applies(self):
        column = rd.ManifestColumn("F", "STRING", "A completely different description")
        updates: list[dict] = []
        kept = rd._resolve_description(column, "Old.", "report-only", "R", updates)
        self.assertEqual(kept, "Old.")
        self.assertFalse(updates[0]["applied"])

    def test_new_row_styling_code_formats_enums_but_not_acronyms(self):
        styled = rd.style_new_description(
            "The category as a raw enum value, for example USERS_GROUPS, exposed in the API"
        )
        self.assertIn("`USERS_GROUPS`", styled)
        self.assertIn(" API", styled)
        self.assertNotIn("`API`", styled)

    def test_new_row_styling_code_formats_boolean_literals(self):
        styled = rd.style_new_description("Whether it is admin level, as true or false")
        self.assertIn("`true`", styled)
        self.assertIn("`false`", styled)


# ---------------------------------------------------------------------------
# 4. Golden no-op
# ---------------------------------------------------------------------------


class TestGoldenNoOp(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        shutil.copy(BASELINE, self.article)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_converged_article_produces_zero_diff(self):
        result = run(self.article, MANIFEST)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.article.read_text(encoding="utf-8"),
            BASELINE.read_text(encoding="utf-8"),
            "reconciling a converged article changed it; that is a parser bug",
        )

    def test_dry_run_never_writes(self):
        before = self.article.read_text(encoding="utf-8")
        result = run(self.article, ROLEGRANTS_MANIFEST, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.article.read_text(encoding="utf-8"), before)

    def test_second_run_is_a_no_op(self):
        shutil.copy(ROLEGRANTS_BEFORE, self.article)
        self.assertEqual(run(self.article, ROLEGRANTS_MANIFEST).returncode, 0)
        after_first = self.article.read_text(encoding="utf-8")
        self.assertEqual(run(self.article, ROLEGRANTS_MANIFEST).returncode, 0)
        self.assertEqual(self.article.read_text(encoding="utf-8"), after_first)


# ---------------------------------------------------------------------------
# 5. Synthetic change: the Role Grants columns from DOMO-492939
# ---------------------------------------------------------------------------


class TestSyntheticChange(unittest.TestCase):
    """The connector branch adds Grant ID, Category and Admin Level with descriptions.

    PR #414 contains the hand-written correct answer, which is what
    `article-baseline.mdx` carries, so the whole file is the assertion.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        shutil.copy(ROLEGRANTS_BEFORE, self.article)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_reproduces_the_hand_written_answer_exactly(self):
        result = run(self.article, ROLEGRANTS_MANIFEST, "--report-json", str(self.tmp / "r.json"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.article.read_text(encoding="utf-8"),
            BASELINE.read_text(encoding="utf-8"),
        )

    def test_exactly_three_columns_were_added_and_nothing_else(self):
        report_path = self.tmp / "r.json"
        run(self.article, ROLEGRANTS_MANIFEST, "--report-json", str(report_path))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        added = report["applied"]["columnsAdded"]
        self.assertEqual(
            [a["field"] for a in added], ["Grant ID", "Category", "Admin Level"]
        )
        self.assertTrue(all(a["report"] == "Role Grants" for a in added))
        self.assertEqual(report["applied"]["reportsAdded"], [])
        self.assertEqual(report["applied"]["sectionsReordered"], [])
        self.assertEqual(
            [d for d in report["applied"]["descriptionsUpdated"] if d["applied"]], []
        )

    def test_no_verify_marker_on_connector_written_descriptions(self):
        run(self.article, ROLEGRANTS_MANIFEST)
        text = self.article.read_text(encoding="utf-8")
        self.assertNotIn(rd.VERIFY_MARKER, text)


# ---------------------------------------------------------------------------
# 6. Anomaly suite
# ---------------------------------------------------------------------------


class TestAnomalies(unittest.TestCase):
    """Every section the rewriter must leave byte-identical, whatever else it does."""

    UNTOUCHABLE = (
        "Task Center",
        "Upgrade Path Conversions",
        "Beast Modes used in Beast Modes",
        "Certified Content",
        "Domo Goals | Goals",
    )

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        shutil.copy(ROLEGRANTS_BEFORE, self.article)
        self.before = sections(self.article.read_text(encoding="utf-8"))
        run(self.article, ROLEGRANTS_MANIFEST)
        self.after = sections(self.article.read_text(encoding="utf-8"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_anomalous_and_prose_sections_are_byte_identical(self):
        for name in self.UNTOUCHABLE:
            with self.subTest(section=name):
                self.assertEqual(self.before[name], self.after[name])

    def test_task_center_broken_header_survives(self):
        task_center = self.after["Task Center"]
        # An empty header row followed by the separator, with the real header as data.
        self.assertRegex(task_center, r"\n\|\s+\|\s+\|\n")
        self.assertIn("| **Field**", task_center)

    def test_upgrade_path_conversions_gains_no_table(self):
        self.assertNotIn("|", self.after["Upgrade Path Conversions"])

    def test_bold_header_style_is_preserved_per_section(self):
        for name, body in self.before.items():
            with self.subTest(section=name):
                self.assertEqual(
                    "| **Field**" in body, "| **Field**" in self.after[name]
                )

    def test_callouts_are_never_added_removed_or_reworded(self):
        before = ROLEGRANTS_BEFORE.read_text(encoding="utf-8")
        after = self.article.read_text(encoding="utf-8")
        self.assertEqual(before.count("<Note>"), after.count("<Note>"))
        self.assertEqual(
            re.findall(r"<Note>.*?</Note>", before, re.S),
            re.findall(r"<Note>.*?</Note>", after, re.S),
        )

    def test_html_pipe_entities_are_preserved(self):
        self.assertEqual(
            ROLEGRANTS_BEFORE.read_text(encoding="utf-8").count("&#124;"),
            self.article.read_text(encoding="utf-8").count("&#124;"),
        )


# ---------------------------------------------------------------------------
# 7. Structural parity and the hard guard
# ---------------------------------------------------------------------------


class TestStructure(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_heading_count_is_stable_when_no_report_is_added(self):
        shutil.copy(ROLEGRANTS_BEFORE, self.article)
        before = self.article.read_text(encoding="utf-8")
        run(self.article, ROLEGRANTS_MANIFEST)
        after = self.article.read_text(encoding="utf-8")
        count = lambda text: len(re.findall(r"^#{2,4} ", text, re.M))  # noqa: E731
        self.assertEqual(count(before), count(after))

    def test_tables_come_out_padded(self):
        """pad_md_tables must report no change on a second invocation."""
        sys.path.insert(0, str(REPO / "scripts"))
        import pad_md_tables  # noqa: PLC0415

        shutil.copy(ROLEGRANTS_BEFORE, self.article)
        run(self.article, ROLEGRANTS_MANIFEST)
        text = self.article.read_text(encoding="utf-8")
        self.assertEqual(pad_md_tables.process(text), text)

    def test_escaped_pipe_in_the_writable_region_is_refused(self):
        text = BASELINE.read_text(encoding="utf-8")
        text = text.replace("| Role ID  ", "| Role \\| ID  ", 1).replace(
            "| Role ID ", "| Role \\| ID ", 1
        )
        self.article.write_text(text, encoding="utf-8")
        result = run(self.article, MANIFEST)
        self.assertEqual(result.returncode, 1)
        self.assertIn("escaped pipe", result.stderr)

    def test_missing_dataset_fields_heading_is_refused(self):
        self.article.write_text(
            '---\ntitle: "x"\n---\n\n## Intro\n\nNo field tables here.\n', encoding="utf-8"
        )
        result = run(self.article, MANIFEST)
        self.assertEqual(result.returncode, 1)
        self.assertIn("DataSet Fields", result.stderr)

    def test_missing_manifest_is_bad_input(self):
        shutil.copy(BASELINE, self.article)
        result = run(self.article, self.tmp / "nope.json")
        self.assertEqual(result.returncode, 2)


# ---------------------------------------------------------------------------
# 8. Curated section ordering
# ---------------------------------------------------------------------------


class TestInsertionOrder(unittest.TestCase):
    def _sections(self, names: list[str]) -> list[rd.Section]:
        return [
            rd.Section(heading=n, name=n, start=i * 10, end=i * 10 + 10, table=None)
            for i, n in enumerate(names)
        ]

    def test_alphabetical_placement_outside_a_curated_block(self):
        order = self._sections(["Accounts", "Buzz", "Cards"])
        self.assertEqual(rd.insertion_index(order, "Alerts"), 10)

    def test_new_domo_goals_member_is_appended_to_its_block(self):
        order = self._sections(
            [
                "Accounts",
                "Domo Goals | Goals",
                "Domo Goals | Goal Owners",
                "Email Logs",
            ]
        )
        # After the last member of the block, not alphabetically inside it.
        self.assertEqual(rd.insertion_index(order, "Domo Goals | Goal Teams"), 30)

    def test_new_pdp_member_is_appended_to_its_block(self):
        order = self._sections(
            ["Mobile Activity", "PDP - Column Policies", "PDP - Row Policies", "People"]
        )
        self.assertEqual(rd.insertion_index(order, "PDP - Column Policy Rules"), 30)

    def test_a_curated_block_is_never_split(self):
        order = self._sections(
            ["Mobile Activity", "PDP - Column Policies", "PDP - Row Policies", "Roles"]
        )
        # "Pages (Deprecated)" sorts before "PDP - ", so it lands ahead of the block.
        self.assertEqual(rd.insertion_index(order, "Pages (Deprecated)"), 10)
        # "Publish" sorts after it, so it lands past the whole block.
        self.assertEqual(rd.insertion_index(order, "Publish"), 30)


# ---------------------------------------------------------------------------
# 9. Reports the reconciler must not act on
# ---------------------------------------------------------------------------


class TestReportOnly(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        self.report_path = self.tmp / "r.json"
        shutil.copy(BASELINE, self.article)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _report(self, manifest: Path, *extra: str) -> dict:
        run(self.article, manifest, "--report-json", str(self.report_path), *extra)
        return json.loads(self.report_path.read_text(encoding="utf-8"))

    def _with_config(self, manifest: Path, config: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "reconcile_domostats.py"),
                "--manifest", str(manifest),
                "--article", str(self.article),
                "--ja-article", str(self.tmp / "nope.mdx"),
                "--config", str(config),
                "--report-json", str(self.report_path),
            ],
            capture_output=True, text=True, cwd=REPO, check=True,
        )

    def test_a_column_only_the_article_has_is_reported_not_deleted(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for report in manifest["reports"]:
            if report["displayName"] == "Roles":
                report["columns"] = report["columns"][:2]
        trimmed = self.tmp / "trimmed.json"
        trimmed.write_text(json.dumps(manifest), encoding="utf-8")

        result = self._report(trimmed)
        removed = [
            r for r in result["review"]["columnsRemoved"] if r["report"] == "Roles"
        ]
        self.assertEqual(
            [r["field"] for r in removed],
            ["Description", "Created Date", "Last Updated Date"],
        )
        self.assertIn("| Last Updated Date", self.article.read_text(encoding="utf-8"))

    def test_a_section_with_no_manifest_report_is_reported_not_deleted(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["reports"] = [
            r for r in manifest["reports"] if r["displayName"] != "Roles"
        ]
        trimmed = self.tmp / "trimmed.json"
        trimmed.write_text(json.dumps(manifest), encoding="utf-8")

        result = self._report(trimmed)
        self.assertIn(
            "Roles", [r["section"] for r in result["review"]["reportsRemoved"]]
        )
        self.assertIn("### Roles", self.article.read_text(encoding="utf-8"))

    def test_an_unresolved_report_is_reported_and_its_table_untouched(self):
        result = self._report(MANIFEST)
        unresolved = [r["report"] for r in result["review"]["reportsUnresolved"]]
        self.assertIn("Upgrade Path Conversions", unresolved)
        self.assertEqual(
            BASELINE.read_text(encoding="utf-8"),
            self.article.read_text(encoding="utf-8"),
        )

    def test_a_restricted_report_is_skipped(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for report in manifest["reports"]:
            if report["displayName"] == "Roles":
                report["gating"]["restricted"] = True
                report["gating"]["restrictionKinds"] = ["environment-allowlist"]
                report["gating"]["featureSwitch"] = None
                report["columns"] = report["columns"][:1]
        restricted = self.tmp / "restricted.json"
        restricted.write_text(json.dumps(manifest), encoding="utf-8")

        result = self._report(restricted)
        entry = next(
            r for r in result["review"]["reportsRestricted"] if r["report"] == "Roles"
        )
        self.assertEqual(entry["restrictionKinds"], ["environment-allowlist"])
        self.assertIn("| Last Updated Date", self.article.read_text(encoding="utf-8"))

    def test_no_customer_or_environment_identifier_reaches_the_report(self):
        """The manifest records restriction kinds only; nothing names who is allowlisted."""
        blob = json.dumps(json.loads(MANIFEST.read_text(encoding="utf-8")))
        for term in ("stravello", "fidelity", "loreal", "wellpoint", "concentrix",
                     "moneydesktop", "mmmm-", "demo1", "gastage1", "prod2"):
            self.assertNotIn(term, blob.lower(), f"{term} leaked into the manifest fixture")
        for report in json.loads(blob)["reports"]:
            self.assertNotIn("customers", report["gating"])
            self.assertNotIn("environments", report["gating"])
            self.assertNotIn("unevaluated", report["gating"])

    def test_an_excluded_report_key_is_neither_added_nor_reported(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        extra = json.loads(json.dumps(manifest["reports"][0]))
        extra.update(
            {
                "key": "brandNewReport",
                "displayName": "Brand New Report",
                "aliases": [],
                "unresolved": False,
            }
        )
        manifest["reports"].append(extra)
        extended = self.tmp / "extended.json"
        extended.write_text(json.dumps(manifest), encoding="utf-8")
        config = self.tmp / "config.json"
        config.write_text(json.dumps({"excludedReportKeys": ["brandNewReport"]}))

        opted_in = self.tmp / "opted-in.json"
        opted_in.write_text(json.dumps({"documentedReportKeys": ["brandNewReport"]}))
        self._with_config(extended, opted_in)
        with_report = json.loads(self.report_path.read_text(encoding="utf-8"))
        self.assertIn(
            "Brand New Report",
            [r["report"] for r in with_report["applied"]["reportsAdded"]],
        )

        shutil.copy(BASELINE, self.article)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "reconcile_domostats.py"),
                "--manifest",
                str(extended),
                "--article",
                str(self.article),
                "--ja-article",
                str(self.tmp / "nope.mdx"),
                "--config",
                str(config),
                "--report-json",
                str(self.report_path),
            ],
            capture_output=True,
            text=True,
            cwd=REPO,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        excluded_report = json.loads(self.report_path.read_text(encoding="utf-8"))
        self.assertEqual(excluded_report["applied"]["reportsAdded"], [])
        self.assertEqual(excluded_report["review"]["reportsUndocumented"], [])
        self.assertEqual(
            BASELINE.read_text(encoding="utf-8"),
            self.article.read_text(encoding="utf-8"),
        )

    def test_an_excluded_column_is_not_reported_as_missing(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for report in manifest["reports"]:
            if report["displayName"] == "Roles":
                report["columns"] = report["columns"][:2]
        trimmed = self.tmp / "trimmed.json"
        trimmed.write_text(json.dumps(manifest), encoding="utf-8")
        config = self.tmp / "config.json"
        config.write_text(
            json.dumps({"excludedColumns": ["created date", "LAST_UPDATED_DATE"]})
        )

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "reconcile_domostats.py"),
                "--manifest",
                str(trimmed),
                "--article",
                str(self.article),
                "--ja-article",
                str(self.tmp / "nope.mdx"),
                "--config",
                str(config),
                "--report-json",
                str(self.report_path),
            ],
            capture_output=True,
            text=True,
            cwd=REPO,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(self.report_path.read_text(encoding="utf-8"))
        removed = [
            r["field"] for r in report["review"]["columnsRemoved"] if r["report"] == "Roles"
        ]
        # Matching is case- and separator-insensitive, so only "Description" is left.
        self.assertEqual(removed, ["Description"])
        self.assertIn("| Last Updated Date", self.article.read_text(encoding="utf-8"))

    def test_a_duplicated_connector_column_is_reported_not_duplicated(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for report in manifest["reports"]:
            if report["displayName"] == "Roles":
                report["columns"].append(dict(report["columns"][0]))
        duped = self.tmp / "duped.json"
        duped.write_text(json.dumps(manifest), encoding="utf-8")

        result = self._report(duped)
        self.assertEqual(
            [d["field"] for d in result["review"]["duplicateConnectorColumns"]], ["ID"]
        )
        self.assertEqual(
            self.article.read_text(encoding="utf-8").count("| ID  "),
            BASELINE.read_text(encoding="utf-8").count("| ID  "),
        )


# ---------------------------------------------------------------------------
# 10. Adding a report
# ---------------------------------------------------------------------------


class TestNewReport(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        self.report_path = self.tmp / "r.json"
        shutil.copy(BASELINE, self.article)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["reports"].append(
            {
                "key": "widgets",
                "displayName": "Widgets",
                "aliases": [],
                "reportClass": "com.domo.connector.domostats.widgets.WidgetsReport",
                "schemaClass": "com.domo.connector.domostats.widgets.WidgetsRow",
                "schemaField": "schema",
                "schemaBoundBy": "setSchema-reference",
                "internal": False,
                "gating": {
                    "featureSwitch": "widgets-v1",
                    "featureSwitches": ["widgets-v1"],
                    "environments": [],
                    "customers": [],
                    "unevaluated": [],
                    "unconditional": False,
                },
                "unresolved": False,
                "unresolvedReason": None,
                "columns": [
                    {"name": "Widget ID", "type": "STRING", "description": "The widget id"},
                    {"name": "Widget Type", "type": "STRING", "description": ""},
                ],
            }
        )
        self.manifest = self.tmp / "with-widgets.json"
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        # A new report is only written into a public article once a human opts it in.
        self.config = self.tmp / "config.json"
        self.config.write_text(json.dumps({"documentedReportKeys": ["widgets"]}))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, *extra: str, config: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "reconcile_domostats.py"),
                "--manifest", str(self.manifest),
                "--article", str(self.article),
                "--ja-article", str(self.tmp / "nope.mdx"),
                "--config", str(config or self.config),
                "--report-json", str(self.report_path),
                *extra,
            ],
            capture_output=True, text=True, cwd=REPO, check=False,
        )

    def test_section_table_and_details_pane_row_are_all_added(self):
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.article.read_text(encoding="utf-8")
        self.assertIn("### Widgets", text)
        self.assertIn("| Widget ID", text)
        # Details Pane row, above the field sections.
        pane = text.split(rd.FIELDS_HEADING)[0]
        self.assertIn("| Widgets", pane)

    def test_a_blank_source_description_becomes_a_todo_with_a_verify_marker(self):
        self._run()
        text = self.article.read_text(encoding="utf-8")
        self.assertRegex(text, r"\| Widget Type\s+\| TODO: describe this field\.")
        self.assertIn(rd.VERIFY_MARKER, text)
        report = json.loads(self.report_path.read_text(encoding="utf-8"))
        self.assertIn(
            "Widget Type", [v["field"] for v in report["review"]["verifyEnumValues"]]
        )

    def test_no_callout_is_generated_for_the_new_section(self):
        before = BASELINE.read_text(encoding="utf-8").count("<Note>")
        self._run()
        self.assertEqual(self.article.read_text(encoding="utf-8").count("<Note>"), before)
        report = json.loads(self.report_path.read_text(encoding="utf-8"))
        self.assertIn(
            "widgets-v1",
            [g["featureSwitch"] for g in report["review"]["gatingSuggestions"]],
        )

    def test_a_pr_body_is_rendered(self):
        body_path = self.tmp / "body.md"
        self._run("--pr-body", str(body_path))
        body = body_path.read_text(encoding="utf-8")
        self.assertIn("## DomoStats schema sync", body)
        self.assertIn("Widgets", body)
        self.assertIn("Needs a human", body)
        self.assertNotIn("—", body)


class TestNewReportPolicy(unittest.TestCase):
    """A report the connector has and the article does not may be unreleased.

    This repository is public, so a section is only generated once a human opts the report
    in, and until then its name is withheld from the PR body and the report JSON.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        self.report_path = self.tmp / "r.json"
        shutil.copy(BASELINE, self.article)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        template = json.loads(json.dumps(manifest["reports"][0]))
        template.update(
            {
                "key": "unreleasedThing",
                "displayName": "Unreleased Thing",
                "aliases": [],
                "unresolved": False,
                "gating": {
                    "featureSwitch": "unreleased-thing",
                    "featureSwitches": ["unreleased-thing"],
                    "restricted": False,
                    "restrictionKinds": [],
                    "unconditional": False,
                },
            }
        )
        manifest["reports"].append(template)
        self.manifest = self.tmp / "manifest.json"
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, config: dict, *extra: str) -> dict:
        config_path = self.tmp / "config.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        body = self.tmp / "body.md"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "reconcile_domostats.py"),
                "--manifest", str(self.manifest),
                "--article", str(self.article),
                "--ja-article", str(self.tmp / "nope.mdx"),
                "--config", str(config_path),
                "--report-json", str(self.report_path),
                "--pr-body", str(body),
                *extra,
            ],
            capture_output=True, text=True, cwd=REPO, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.body = body.read_text(encoding="utf-8")
        return json.loads(self.report_path.read_text(encoding="utf-8"))

    def test_default_policy_adds_nothing_and_withholds_the_name(self):
        report = self._run({})
        self.assertEqual(report["applied"]["reportsAdded"], [])
        self.assertNotIn("### Unreleased Thing", self.article.read_text(encoding="utf-8"))

        undocumented = report["review"]["reportsUndocumented"]
        self.assertTrue(undocumented)
        self.assertTrue(all(u["withheld"] for u in undocumented))
        self.assertTrue(all("report" not in u for u in undocumented))
        self.assertTrue(all("key" not in u for u in undocumented))

    def test_the_withheld_name_never_reaches_the_pr_body(self):
        self._run({})
        self.assertNotIn("Unreleased Thing", self.body)
        self.assertNotIn("unreleasedThing", self.body)
        self.assertIn("names are withheld", self.body)

    def test_opting_a_report_in_generates_its_section(self):
        report = self._run({"documentedReportKeys": ["unreleasedThing"]})
        self.assertEqual(
            [r["report"] for r in report["applied"]["reportsAdded"]], ["Unreleased Thing"]
        )
        self.assertIn("### Unreleased Thing", self.article.read_text(encoding="utf-8"))

    def test_auto_policy_restores_eager_behaviour(self):
        report = self._run({"newReportPolicy": "auto"})
        self.assertIn(
            "Unreleased Thing", [r["report"] for r in report["applied"]["reportsAdded"]]
        )

    def test_no_redact_names_the_report_for_private_use(self):
        report = self._run({}, "--no-redact")
        undocumented = report["review"]["reportsUndocumented"]
        self.assertIn("Unreleased Thing", [u["report"] for u in undocumented])
        self.assertFalse(any(u["withheld"] for u in undocumented))
        self.assertIn("Unreleased Thing", self.body)


# ---------------------------------------------------------------------------
# 11. Japanese drift
# ---------------------------------------------------------------------------


class TestJapaneseDrift(unittest.TestCase):
    """The mirror is reported on and never edited, and its headings are translated."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.article = self.tmp / "article.mdx"
        self.ja = self.tmp / "ja.mdx"
        self.report_path = self.tmp / "r.json"
        shutil.copy(BASELINE, self.article)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _localize(self, text: str) -> str:
        """Stand in for the real mirror.

        `ja/s/article/360043433813.mdx` translates the `##` headings, the table header
        cells and the descriptions, but leaves the report `###` headings and the field
        names in English, because those are literal DataSet and column names.
        """
        return (
            text.replace(rd.FIELDS_HEADING, "## DataSetフィールド")
            .replace("### Details Pane", "### ［詳細］ペイン")
            .replace("| Field ", "| フィールド ")
            .replace("| **Field** ", "| **フィールド** ")
        )

    def _run(self) -> dict:
        subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "reconcile_domostats.py"),
                "--manifest",
                str(MANIFEST),
                "--article",
                str(self.article),
                "--ja-article",
                str(self.ja),
                "--config",
                str(self.tmp / "nope.json"),
                "--report-json",
                str(self.report_path),
            ],
            capture_output=True,
            text=True,
            cwd=REPO,
            check=True,
        )
        return json.loads(self.report_path.read_text(encoding="utf-8"))

    def test_a_translated_fields_heading_is_still_found(self):
        self.ja.write_text(
            self._localize(BASELINE.read_text(encoding="utf-8")), encoding="utf-8"
        )
        result = self._run()
        self.assertEqual(result["notes"], [])
        self.assertEqual(result["review"]["japaneseDrift"], [])

    def test_a_row_count_difference_is_reported(self):
        lines = self._localize(BASELINE.read_text(encoding="utf-8")).split("\n")
        start = next(i for i, line in enumerate(lines) if line.strip() == "### Accounts")
        stop = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("### "))
        rows = [i for i in range(start, stop) if lines[i].startswith("|")]
        drop = set(rows[-2:])
        self.ja.write_text(
            "\n".join(l for i, l in enumerate(lines) if i not in drop), encoding="utf-8"
        )
        drift = self._run()["review"]["japaneseDrift"]
        self.assertEqual(
            drift,
            [
                {
                    "section": "Accounts",
                    "japaneseSection": "Accounts",
                    "issue": "row count differs",
                    "english": 13,
                    "japanese": 11,
                }
            ],
        )

    def test_a_section_missing_from_the_mirror_is_named(self):
        lines = self._localize(BASELINE.read_text(encoding="utf-8")).split("\n")
        start = next(i for i, line in enumerate(lines) if line.strip() == "### Roles")
        stop = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("### "))
        self.ja.write_text("\n".join(lines[:start] + lines[stop:]), encoding="utf-8")
        drift = self._run()["review"]["japaneseDrift"]
        self.assertIn(
            {"section": "Roles", "issue": "missing from the Japanese mirror"}, drift
        )

    def test_pairing_falls_back_to_position_when_headings_are_translated(self):
        text = self._localize(BASELINE.read_text(encoding="utf-8"))
        text = re.sub(r"^### (?!\[)", "### 翻訳済み ", text, flags=re.M)
        self.ja.write_text(text, encoding="utf-8")
        result = self._run()
        self.assertTrue(any("by position" in note for note in result["notes"]))
        # Same structure, only the headings changed, so nothing should be reported.
        self.assertEqual(result["review"]["japaneseDrift"], [])

    def test_the_japanese_file_is_never_written(self):
        localized = self._localize(BASELINE.read_text(encoding="utf-8"))
        self.ja.write_text(localized, encoding="utf-8")
        self._run()
        self.assertEqual(self.ja.read_text(encoding="utf-8"), localized)

    def test_a_missing_mirror_is_a_note_not_a_failure(self):
        result = self._run()
        self.assertTrue(any("not found" in note for note in result["notes"]))
        self.assertEqual(result["review"]["japaneseDrift"], [])


# ---------------------------------------------------------------------------
# 12. Description drafting
# ---------------------------------------------------------------------------


class _FakeMessages:
    def __init__(self, text: str):
        self.text = text
        self.prompts: list[str] = []

    def create(self, **kwargs):
        self.prompts.append(kwargs["messages"][0]["content"])

        class Block:
            def __init__(self, text):
                self.text = text

        class Response:
            def __init__(self, text):
                self.content = [Block(text)]

        return Response(self.text)


class _FakeClient:
    def __init__(self, text: str):
        self.messages = _FakeMessages(text)


class TestDrafting(unittest.TestCase):
    """The drafting call is stubbed; what is under test is the cell substitution."""

    def setUp(self):
        self.lines = [
            "### Roles",
            "",
            "| Field     | Description                                            |",
            "| --------- | ------------------------------------------------------ |",
            "| ID        | The unique identifier of the role.                     |",
            "| Name      | The name of the role.                                  |",
            "| Role Kind | TODO: describe this field. <!-- verify enum values --> |",
            "",
        ]
        self.report = rd.Report()
        self.report.applied_columns_added.append(
            {
                "report": "Roles",
                "field": "Role Kind",
                "type": "STRING",
                "description": "TODO: describe this field. <!-- verify enum values -->",
                "needsDraft": True,
            }
        )
        self.fake = _FakeClient("The classification of the role")
        self._real_client = rd._anthropic_client
        rd._anthropic_client = lambda api_key: self.fake

    def tearDown(self):
        rd._anthropic_client = self._real_client

    def test_the_placeholder_is_replaced_and_the_marker_kept(self):
        out = rd.draft_descriptions(
            self.lines, self.report, "test-model", Path("article.mdx"), api_key="k"
        )
        text = "\n".join(out)
        self.assertIn("The classification of the role.", text)
        self.assertNotIn("TODO: describe this field.", text)
        self.assertIn(rd.VERIFY_MARKER, text)
        self.assertEqual(
            self.report.drafted_descriptions,
            [
                {
                    "report": "Roles",
                    "field": "Role Kind",
                    "description": "The classification of the role.",
                }
            ],
        )
        self.assertFalse(self.report.applied_columns_added[0]["needsDraft"])

    def test_the_prompt_carries_the_neighbouring_rows_for_voice(self):
        rd.draft_descriptions(
            self.lines, self.report, "test-model", Path("article.mdx"), api_key="k"
        )
        prompt = self.fake.messages.prompts[0]
        self.assertIn("Role Kind", prompt)
        self.assertIn("The name of the role.", prompt)
        self.assertIn("Do not invent enum values", prompt)
        self.assertIn("Do not use an em dash", prompt)

    def test_no_key_leaves_the_placeholder_and_records_a_note(self):
        out = rd.draft_descriptions(
            self.lines, self.report, "test-model", Path("article.mdx"), api_key=None
        )
        self.assertEqual(out, self.lines)
        self.assertTrue(any("ANTHROPIC_API_KEY" in n for n in self.report.notes))
        self.assertEqual(self.fake.messages.prompts, [])

    def test_a_failed_call_leaves_the_placeholder_and_records_a_note(self):
        class Boom:
            class messages:  # noqa: N801
                prompts: list[str] = []

                @staticmethod
                def create(**kwargs):
                    raise RuntimeError("upstream is down")

        rd._anthropic_client = lambda api_key: Boom()
        out = rd.draft_descriptions(
            self.lines, self.report, "test-model", Path("article.mdx"), api_key="k"
        )
        self.assertEqual(out, self.lines)
        self.assertTrue(any("draft failed" in n for n in self.report.notes))


# ---------------------------------------------------------------------------
# 13. Table parsing
# ---------------------------------------------------------------------------


class TestTableParsing(unittest.TestCase):
    def test_plain_table(self):
        lines = ["| Field | Description |", "| --- | --- |", "| A | one |", "| B | two |"]
        table = rd.find_table(lines, 0, len(lines))
        self.assertIsNotNone(table)
        self.assertFalse(table.bold_header)
        self.assertFalse(table.broken_header)
        self.assertEqual(table.rows, [["A", "one"], ["B", "two"]])

    def test_bold_header_is_detected(self):
        lines = ["| **Field** | **Description** |", "| --- | --- |", "| A | one |"]
        table = rd.find_table(lines, 0, len(lines))
        self.assertTrue(table.bold_header)

    def test_empty_header_row_is_flagged_and_round_trips(self):
        lines = [
            "|  |  |",
            "| --- | --- |",
            "| **Field** | **Description** |",
            "| A | one |",
        ]
        table = rd.find_table(lines, 0, len(lines))
        self.assertTrue(table.broken_header)
        self.assertEqual(table.pseudo_header, ["**Field**", "**Description**"])
        self.assertEqual(table.rows, [["A", "one"]])
        self.assertEqual(
            table.render(),
            ["|  |  |", "| --- | --- |", "| **Field** | **Description** |", "| A | one |"],
        )

    def test_no_table_returns_none(self):
        self.assertIsNone(rd.find_table(["Just prose.", ""], 0, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
