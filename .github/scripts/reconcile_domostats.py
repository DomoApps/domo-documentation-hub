#!/usr/bin/env python3
"""
Reconcile the DomoStats Connector KB article against the connector's schema manifest.

The manifest (`domostats-schema.json`) is generated in `domo-development/domostats` by
`./gradlew generateSchemaManifest` and committed there. This script compares it against
the `## DataSet Fields` section of `s/article/360043433813.mdx`, applies the changes that
are mechanically safe, and reports everything a human must still decide.

Applied automatically
    * a column the connector has and the article does not, inserted at its schema position
    * a column description the connector has and the article's differs from, once
      normalization has ruled out presentation-only differences
    * row order, when every article row maps to a manifest column
    * a report the connector has and the article does not, as a new section plus a
      Details Pane row (only when the report is generally available and its schema resolved)

Reported, never applied
    * a column or a report the article has and the connector does not
    * a report the manifest could not resolve to a schema
    * a report gated by an environment or customer allowlist
    * feature-switch notes: 41 callouts exist and their wording was hand-audited; new
      gating goes in the PR body as a suggestion, never into the article
    * anything structurally unusual (see SKIP_REASON_* below)

The comparison contract
    Java description strings are plain text that never renders; the docs keep Markdown
    presentation. The two sides are deliberately not byte-identical and are compared on a
    normalized form: backticks stripped, whitespace collapsed, one trailing period dropped.

    The single most important rule: when the manifest description is empty, the article's
    description is authoritative and is left untouched. Most columns still have no source
    description, so treating an empty source string as "clear the docs" would erase most
    of the article.

Usage
    python3 .github/scripts/reconcile_domostats.py \\
      --manifest source-repo/domostats-schema.json \\
      --article s/article/360043433813.mdx \\
      --ja-article ja/s/article/360043433813.mdx \\
      --report-json domostats-report.json \\
      --pr-body domostats-pr-body.md \\
      [--dry-run] [--draft-descriptions]

Exit codes
    0  reconciled (with or without changes)
    1  refused: a structural invariant the rewriter depends on does not hold
    2  bad input (missing file, unreadable manifest)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

# The article's field tables start here. Everything above it is prose the reconciler
# never touches, apart from the Details Pane report index.
FIELDS_HEADING = "## DataSet Fields"
DETAILS_PANE_HEADING = "### Details Pane"

# Sections whose display name starts with one of these are hand-ordered blocks. New
# members are appended to the block; the block itself is never sorted.
CURATED_PREFIXES = ("Domo Goals |", "PDP - ")

SKIP_REASON_NO_TABLE = "no field table in the article"
SKIP_REASON_BROKEN_HEADER = "table header row is empty (documented anomaly)"
SKIP_REASON_UNRESOLVED = "manifest could not resolve a schema for this report"
SKIP_REASON_RESTRICTED = "gated by an environment or customer allowlist"
SKIP_REASON_NOT_OPTED_IN = (
    "not in documentedReportKeys; a human opts a report in once it is announceable"
)

# Reasons whose wording would identify the report they belong to. Only used when the
# report name is being withheld, so the category still surfaces without the name.
REDACTED_REASONS = {
    "schema is built at run time from a remote schema endpoint": (
        "schema is built at run time"
    ),
}

# Column names or types that hint at an enum. Their drafted descriptions get a verify
# marker: enum members live in convertToString methods, not in the schema, so neither the
# manifest nor a model drafting from it can see the real value list.
ENUM_HINT_RE = re.compile(
    r"\b(type|status|state|level|kind|category|mode|frequency|unit|method|role)\b",
    re.IGNORECASE,
)
VERIFY_MARKER = "<!-- verify enum values -->"


# ---------------------------------------------------------------------------
# The comparison contract
# ---------------------------------------------------------------------------


def normalize(text: str) -> str:
    """Reduce a description to the form the two sides are allowed to agree on.

    The docs code-format enum values and terminate sentences; a Java string literal does
    neither. Comparing raw text would report every row in the article as changed.
    """
    text = text.replace("`", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip(".")


def normalize_field(name: str) -> str:
    """Field-name key that tolerates the casing and separator drift that already exists.

    `Task identifier` and `Task Identifier` are the same column; so are `Account_Id` and
    `Account Id`. Treating them as an add plus a remove would produce a duplicate row and
    a spurious removal report.
    """
    name = name.replace("\\_", "_").replace("&#124;", "|")
    name = re.sub(r"[\s_]+", " ", name).strip()
    return name.casefold()


def squash_field(name: str) -> str:
    """Separator-blind field key, used only as a fallback.

    `PageIds` and `Page Ids` are the same column. Matching on this key first would risk
    merging two genuinely distinct columns, so it is tried only for columns that found no
    match under `normalize_field`.
    """
    return re.sub(r"[^0-9a-z]+", "", normalize_field(name))


def normalize_report(name: str) -> str:
    """Report-name key for pairing a manifest report with an article section.

    Display names drift: the dropdown says "AI Readiness Report" where the article says
    "AI Readiness". Stripping a trailing "Report"/"DataSet" pairs them instead of
    reporting one as new and the other as removed.
    """
    name = unescape_pipes(name)
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"\s+(report|dataset|data set)$", "", name, flags=re.IGNORECASE)
    return name.casefold()


def unescape_pipes(text: str) -> str:
    return text.replace("&#124;", "|").replace("\\|", "|")


def escape_pipes(text: str) -> str:
    """Pipe escaping for a table cell. The Details Pane uses the HTML entity."""
    return text.replace("|", "&#124;")


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


@dataclass
class Table:
    """A pipe table in the article, as parsed cells plus enough context to rebuild it."""

    start: int  # index into the owning line list, inclusive
    end: int  # exclusive
    header: list[str]
    rows: list[list[str]]
    bold_header: bool
    broken_header: bool
    # When the header row is empty, the real header sits in the first data row. It is
    # carried here verbatim so rendering puts it back exactly as it was.
    pseudo_header: Optional[list[str]] = None

    def render(self) -> list[str]:
        cells = [self.header, ["---"] * len(self.header)]
        if self.pseudo_header is not None:
            cells.append(self.pseudo_header)
        cells.extend(self.rows)
        return ["| " + " | ".join(row) + " |" for row in cells]


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_separator(cells: Iterable[str]) -> bool:
    cells = list(cells)
    if not cells:
        return False
    return all(c and not (set(c) - set("-:")) and "-" in c for c in cells)


def find_table(lines: list[str], start: int, stop: int) -> Optional[Table]:
    """First pipe table in lines[start:stop], or None."""
    i = start
    while i < stop - 1:
        if lines[i].strip().startswith("|") and is_separator(split_row(lines[i + 1])):
            header = split_row(lines[i])
            j = i + 2
            rows = []
            while j < stop and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            broken = all(not c for c in header)
            pseudo = rows.pop(0) if broken and rows else None
            bold = any(c.startswith("**") for c in (pseudo or header))
            return Table(i, j, header, rows, bold, broken, pseudo)
        i += 1
    return None


def label(text: str, bold: bool) -> str:
    return f"**{text}**" if bold else text


# ---------------------------------------------------------------------------
# The article
# ---------------------------------------------------------------------------


@dataclass
class Section:
    """One `### <Display Name>` report section inside `## DataSet Fields`."""

    heading: str  # raw heading text, pipes as written
    name: str  # heading text with pipes unescaped
    start: int  # index of the `###` line
    end: int  # exclusive
    table: Optional[Table]

    @property
    def curated_prefix(self) -> Optional[str]:
        for prefix in CURATED_PREFIXES:
            if self.name.startswith(prefix):
                return prefix
        return None


@dataclass
class Article:
    path: Path
    lines: list[str]
    fields_start: int  # index of the `## DataSet Fields` line
    sections: list[Section]
    details_pane: Optional[Table]

    def text(self) -> str:
        return "\n".join(self.lines)


def find_fields_heading(lines: list[str]) -> int:
    """Locate the field-tables section without relying on its English wording.

    The localized mirrors translate the heading ("## DataSetフィールド"), so the drift
    check cannot match on the literal. The section is instead identified by shape: the
    last `##` heading that owns most of the file's `###` subsections.
    """
    tops = [i for i, line in enumerate(lines) if re.match(r"^##\s+\S", line)]
    if not tops:
        return -1
    subs = [i for i, line in enumerate(lines) if re.match(r"^###\s+\S", line)]
    best, best_count = -1, 0
    for pos, start in enumerate(tops):
        end = tops[pos + 1] if pos + 1 < len(tops) else len(lines)
        count = sum(1 for s in subs if start < s < end)
        if count > best_count:
            best, best_count = start, count
    return best if best_count >= 5 else -1


def parse_article(path: Path, require_english_heading: bool = True) -> Article:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    fields_start = next(
        (i for i, line in enumerate(lines) if line.strip() == FIELDS_HEADING), -1
    )
    if fields_start < 0 and not require_english_heading:
        fields_start = find_fields_heading(lines)
    if fields_start < 0:
        raise Refusal(
            f"{path}: no '{FIELDS_HEADING}' heading found"
            if require_english_heading
            else f"{path}: could not locate the field-tables section"
        )

    # Hard guard. scripts/pad_md_tables.py splits cells on a plain "|" with no escape
    # handling, so an escaped pipe inside a cell would split it and add a phantom column
    # to the whole table on the next padding run. Refuse rather than corrupt the article.
    writable = "\n".join(lines[fields_start:])
    if "\\|" in writable:
        raise Refusal(
            f"{path}: found an escaped pipe (\\|) inside '{FIELDS_HEADING}'. "
            "scripts/pad_md_tables.py cannot round-trip that; use &#124; instead."
        )

    heading_indices = [
        i
        for i in range(fields_start + 1, len(lines))
        if re.match(r"^###\s+\S", lines[i])
    ]
    sections = []
    for pos, i in enumerate(heading_indices):
        end = heading_indices[pos + 1] if pos + 1 < len(heading_indices) else len(lines)
        # A `##` heading after the fields section would end it; there is none today, but
        # stop at one rather than swallowing unrelated content into the last section.
        for j in range(i + 1, end):
            if re.match(r"^##\s+\S", lines[j]):
                end = j
                break
        heading = lines[i][3:].strip()
        sections.append(
            Section(
                heading=heading,
                name=unescape_pipes(heading),
                start=i,
                end=end,
                table=find_table(lines, i + 1, end),
            )
        )

    pane_start = next(
        (i for i, line in enumerate(lines) if line.strip() == DETAILS_PANE_HEADING), -1
    )
    details_pane = None
    if 0 <= pane_start < fields_start:
        details_pane = find_table(lines, pane_start + 1, fields_start)

    return Article(path, lines, fields_start, sections, details_pane)


class Refusal(Exception):
    """A structural invariant the rewriter depends on does not hold."""


# ---------------------------------------------------------------------------
# The manifest
# ---------------------------------------------------------------------------


@dataclass
class ManifestColumn:
    name: str
    type: str
    description: str


@dataclass
class ManifestReport:
    key: str
    display_name: str
    aliases: list[str]
    report_class: Optional[str]
    schema_class: Optional[str]
    gating: dict
    unresolved: bool
    unresolved_reason: Optional[str]
    internal: bool
    columns: Optional[list[ManifestColumn]]

    @property
    def names(self) -> list[str]:
        return [self.display_name, *self.aliases]

    @property
    def feature_switch(self) -> Optional[str]:
        return self.gating.get("featureSwitch")

    @property
    def restricted(self) -> bool:
        """Availability depends on something that cannot be decided statically.

        The manifest records only the *kind* of restriction, never the customer
        identifiers or internal environment names behind it, because this repository is
        public and the PR body is world-readable. The kind is all the reconciler needs:
        it answers "may I touch this table automatically, or must a human look?"
        """
        return bool(self.gating.get("restricted") or self.gating.get("restrictionKinds"))

    @property
    def restriction_kinds(self) -> list:
        return list(self.gating.get("restrictionKinds") or [])

    @property
    def generally_available(self) -> bool:
        return not self.restricted and not self.internal


def load_manifest(path: Path) -> list[ManifestReport]:
    data = json.loads(path.read_text(encoding="utf-8"))
    reports = []
    for raw in data.get("reports", []):
        columns = raw.get("columns")
        reports.append(
            ManifestReport(
                key=raw["key"],
                display_name=raw["displayName"],
                aliases=list(raw.get("aliases") or []),
                report_class=raw.get("reportClass"),
                schema_class=raw.get("schemaClass"),
                gating=raw.get("gating") or {},
                unresolved=bool(raw.get("unresolved")),
                unresolved_reason=raw.get("unresolvedReason"),
                internal=bool(raw.get("internal")),
                columns=(
                    None
                    if columns is None
                    else [
                        ManifestColumn(c["name"], c.get("type", ""), c.get("description") or "")
                        for c in columns
                    ]
                ),
            )
        )
    return reports, data


# ---------------------------------------------------------------------------
# The reconciliation report
# ---------------------------------------------------------------------------


@dataclass
class Report:
    """Everything the run decided, split by whether it was applied or not."""

    applied_columns_added: list[dict] = field(default_factory=list)
    applied_descriptions: list[dict] = field(default_factory=list)
    applied_reordered: list[dict] = field(default_factory=list)
    applied_reports_added: list[dict] = field(default_factory=list)

    columns_removed: list[dict] = field(default_factory=list)
    duplicate_columns: list[dict] = field(default_factory=list)
    reports_removed: list[dict] = field(default_factory=list)
    reports_unresolved: list[dict] = field(default_factory=list)
    reports_restricted: list[dict] = field(default_factory=list)
    reports_undocumented: list[dict] = field(default_factory=list)
    name_drift: list[dict] = field(default_factory=list)
    gating_suggestions: list[dict] = field(default_factory=list)
    verify_enums: list[dict] = field(default_factory=list)
    drafted_descriptions: list[dict] = field(default_factory=list)
    sections_skipped: list[dict] = field(default_factory=list)
    pane_drift: list[dict] = field(default_factory=list)
    ja_drift: list[dict] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def applied_count(self) -> int:
        return (
            len(self.applied_columns_added)
            + len([d for d in self.applied_descriptions if d.get("applied")])
            + len(self.applied_reordered)
            + len(self.applied_reports_added)
        )

    @property
    def review_count(self) -> int:
        return (
            len([d for d in self.applied_descriptions if not d.get("applied")])
            + len(self.columns_removed)
            + len(self.duplicate_columns)
            + len(self.reports_removed)
            + len(self.reports_unresolved)
            + len(self.reports_restricted)
            + len(self.reports_undocumented)
            + len(self.name_drift)
            + len(self.gating_suggestions)
            + len(self.verify_enums)
            + len(self.pane_drift)
            + len(self.ja_drift)
        )

    def to_json(self) -> dict:
        return {
            "applied": {
                "columnsAdded": self.applied_columns_added,
                "descriptionsUpdated": self.applied_descriptions,
                "sectionsReordered": self.applied_reordered,
                "reportsAdded": self.applied_reports_added,
            },
            "review": {
                "columnsRemoved": self.columns_removed,
                "duplicateConnectorColumns": self.duplicate_columns,
                "reportsRemoved": self.reports_removed,
                "reportsUnresolved": self.reports_unresolved,
                "reportsRestricted": self.reports_restricted,
                "reportsUndocumented": self.reports_undocumented,
                "nameDrift": self.name_drift,
                "gatingSuggestions": self.gating_suggestions,
                "verifyEnumValues": self.verify_enums,
                "detailsPaneDrift": self.pane_drift,
                "japaneseDrift": self.ja_drift,
            },
            "draftedDescriptions": self.drafted_descriptions,
            "sectionsSkipped": self.sections_skipped,
            "notes": self.notes,
            "counts": {
                "applied": self.applied_count,
                "needsReview": self.review_count,
            },
        }


# ---------------------------------------------------------------------------
# Reconciling one section
# ---------------------------------------------------------------------------


@dataclass
class Pairing:
    """How a manifest report lines up with an article section."""

    report: ManifestReport
    section: Optional[Section]
    exact: bool


def pair_reports(
    reports: list[ManifestReport], sections: list[Section]
) -> tuple[list[Pairing], list[Section]]:
    """Match manifest reports to article sections, exact names first.

    Returns the pairings and the sections nothing claimed.
    """
    by_exact = {}
    by_normal = {}
    for section in sections:
        by_exact.setdefault(section.name, section)
        by_normal.setdefault(normalize_report(section.name), section)

    claimed: set[int] = set()
    pairings = []
    # Exact names win outright, so a normalized collision can never steal a section from
    # the report that names it precisely.
    for report in reports:
        section = next((by_exact.get(n) for n in report.names if by_exact.get(n)), None)
        if section is not None and section.start not in claimed:
            claimed.add(section.start)
            pairings.append(Pairing(report, section, True))
        else:
            pairings.append(Pairing(report, None, False))

    for pairing in pairings:
        if pairing.section is not None:
            continue
        for name in pairing.report.names:
            section = by_normal.get(normalize_report(name))
            if section is not None and section.start not in claimed:
                claimed.add(section.start)
                pairing.section = section
                break

    orphans = [s for s in sections if s.start not in claimed]
    return pairings, orphans


def reconcile_section(
    pairing: Pairing,
    report: Report,
    descriptions_mode: str,
    excluded_columns: set[str],
) -> Optional[Table]:
    """Compute the new table for one section, or None to leave it alone."""
    manifest = pairing.report
    section = pairing.section
    assert section is not None

    if manifest.unresolved or manifest.columns is None:
        report.sections_skipped.append(
            {
                "section": section.name,
                "reason": SKIP_REASON_UNRESOLVED,
                "detail": manifest.unresolved_reason,
            }
        )
        report.reports_unresolved.append(
            {
                "report": manifest.display_name,
                "key": manifest.key,
                "reason": manifest.unresolved_reason,
            }
        )
        return None

    if manifest.restricted:
        report.sections_skipped.append(
            {
                "section": section.name,
                "reason": SKIP_REASON_RESTRICTED,
                "restrictionKinds": manifest.restriction_kinds,
            }
        )
        report.reports_restricted.append(
            {
                "report": manifest.display_name,
                "key": manifest.key,
                "restrictionKinds": manifest.restriction_kinds,
            }
        )
        return None

    table = section.table
    if table is None:
        report.sections_skipped.append(
            {"section": section.name, "reason": SKIP_REASON_NO_TABLE}
        )
        return None
    if table.broken_header:
        report.sections_skipped.append(
            {"section": section.name, "reason": SKIP_REASON_BROKEN_HEADER}
        )
        return None
    if len(table.header) != 2:
        report.sections_skipped.append(
            {
                "section": section.name,
                "reason": f"table has {len(table.header)} columns, expected 2",
            }
        )
        return None

    # ---- pair up rows -------------------------------------------------
    article_rows = [(row[0], row[1] if len(row) > 1 else "") for row in table.rows]
    row_by_key: dict[str, int] = {}
    row_by_squash: dict[str, int] = {}
    for index, (name, _) in enumerate(article_rows):
        row_by_key.setdefault(normalize_field(name), index)
        row_by_squash.setdefault(squash_field(name), index)

    # A schema that lists the same column twice is a connector bug, not two columns.
    # JupyterWorkspaceUsageDataSet declares "Dataflow Id" twice today. Adding a second
    # row for it would put a duplicate into the article, so report and drop it.
    columns: list[ManifestColumn] = []
    seen_columns: set[str] = set()
    for column in manifest.columns:
        key = normalize_field(column.name)
        if key in seen_columns:
            report.duplicate_columns.append(
                {
                    "report": section.name,
                    "field": column.name,
                    "schemaClass": manifest.schema_class,
                }
            )
            continue
        seen_columns.add(key)
        columns.append(column)

    matched_row_indices: set[int] = set()
    # manifest index -> article row index, or None when the column is new
    mapping: list[Optional[int]] = [None] * len(columns)
    # Exact-ish keys first so a separator-blind fallback can never steal a row from the
    # column that names it the same way.
    for lookup in (row_by_key, row_by_squash):
        key_of = normalize_field if lookup is row_by_key else squash_field
        for position, column in enumerate(columns):
            if mapping[position] is not None:
                continue
            index = lookup.get(key_of(column.name))
            if index is not None and index not in matched_row_indices:
                matched_row_indices.add(index)
                mapping[position] = index

    # ---- report what will not be applied ------------------------------
    for index, (name, _) in enumerate(article_rows):
        if index in matched_row_indices:
            continue
        if normalize_field(name) in excluded_columns:
            # Platform-added metadata columns such as _BATCH_ID_ are not part of any
            # connector schema, so their absence from the manifest is not drift.
            continue
        report.columns_removed.append(
            {"report": section.name, "field": name, "action": "left in place"}
        )

    for position, column in enumerate(columns):
        index = mapping[position]
        if index is None:
            continue
        article_name = article_rows[index][0]
        if article_name != column.name and normalize_field(article_name) == normalize_field(
            column.name
        ):
            report.name_drift.append(
                {
                    "report": section.name,
                    "article": article_name,
                    "connector": column.name,
                }
            )

    # ---- build the new row list --------------------------------------
    new_rows: list[list[str]] = []
    additions: list[dict] = []
    updates: list[dict] = []

    reorderable = len(matched_row_indices) == len(article_rows)

    if reorderable:
        # Every article row maps to a manifest column, so schema order is unambiguous.
        for position, column in enumerate(columns):
            index = mapping[position]
            if index is None:
                new_rows.append(
                    _new_row(column, table.bold_header, section.name, additions, report)
                )
            else:
                name, description = article_rows[index]
                new_rows.append(
                    [name, _resolve_description(
                        column, description, descriptions_mode, section.name, updates
                    )]
                )
        if [r[0] for r in new_rows if r[0] in {n for n, _ in article_rows}] != [
            n for n, _ in article_rows
        ]:
            report.applied_reordered.append(
                {"report": section.name, "order": [c.name for c in columns]}
            )
    else:
        # Extra article rows have no schema position, so leave the existing order alone
        # and insert each new column after the row its schema predecessor maps to.
        new_rows = [[name, description] for name, description in article_rows]
        insertions: list[tuple[int, list[str]]] = []
        for position, column in enumerate(columns):
            index = mapping[position]
            if index is not None:
                name, description = article_rows[index]
                new_rows[index] = [
                    name,
                    _resolve_description(
                        column, description, descriptions_mode, section.name, updates
                    ),
                ]
                continue
            anchor = next(
                (mapping[p] for p in range(position - 1, -1, -1) if mapping[p] is not None),
                None,
            )
            at = len(new_rows) if anchor is None else anchor + 1
            insertions.append(
                (at, _new_row(column, table.bold_header, section.name, additions, report))
            )
        for offset, (at, row) in enumerate(sorted(insertions, key=lambda p: p[0])):
            new_rows.insert(at + offset, row)

    report.applied_columns_added.extend(additions)
    report.applied_descriptions.extend(updates)

    if new_rows == [[name, description] for name, description in article_rows]:
        return None

    return Table(
        start=table.start,
        end=table.end,
        header=table.header,
        rows=new_rows,
        bold_header=table.bold_header,
        broken_header=False,
    )


def _new_row(
    column: ManifestColumn,
    bold: bool,
    section_name: str,
    additions: list[dict],
    report: Report,
) -> list[str]:
    """A row for a column the article does not have yet."""
    description = column.description.strip()
    drafted = not description
    if drafted:
        description = "TODO: describe this field."
    else:
        description = style_new_description(description)

    # The marker only goes on descriptions nobody wrote. When the connector author supplied
    # the text, they could see the enum; a model drafting from a column name cannot.
    if drafted and _looks_like_enum(column):
        description = f"{description} {VERIFY_MARKER}"
        report.verify_enums.append(
            {"report": section_name, "field": column.name, "type": column.type}
        )

    additions.append(
        {
            "report": section_name,
            "field": column.name,
            "type": column.type,
            "description": description,
            "needsDraft": drafted,
        }
    )
    return [escape_pipes(column.name), escape_pipes(description)]


CODE_SPAN_RE = re.compile(r"`([^`]+)`")

# The article is written to a style guide; the connector string is not. Anything written
# into the article goes through this first.
DASH_REPLACEMENTS = {"–": "-", "—": "-", "−": "-"}

# Domo product terms the article always capitalizes and Java descriptions often do not.
# Only the all-lowercase form is rewritten, so a column named "Dataset Context" is safe.
HOUSE_TERMS = (
    (re.compile(r"\bdatasets\b"), "DataSets"),
    (re.compile(r"\bdataset\b"), "DataSet"),
    (re.compile(r"\bdataflows\b"), "DataFlows"),
    (re.compile(r"\bdataflow\b"), "DataFlow"),
)

# Below this ratio of normalized lengths, a source description is treated as a summary of
# the article's rather than a correction to it.
SHRINK_RATIO = 0.6


# Values the article always code-formats. A new row has no existing cell to copy
# presentation from, so these are the two patterns worth recognising on their own:
# SCREAMING_SNAKE enum members, and the boolean/null literals.
ENUM_TOKEN_RE = re.compile(r"(?<![`\w])([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+|[A-Z]{3,})(?![`\w])")
LITERAL_TOKEN_RE = re.compile(r"(?<![`\w])(true|false|null|NULL)(?![`\w])")

# Upper-case words that are acronyms in prose, not enum members. Without this an
# uppercase-token rule code-formats "API" and "SQL" in the middle of a sentence.
ACRONYMS = frozenset(
    """
    AI API APIS AWS CPU CSV DNS ETL GCP GPU HTML HTTP HTTPS IDP IP JSON KPI KPIS LDAP
    MFA OAUTH OKR OKRS PDF PDP SAML SDK SFTP SLA SQL SSO TODO UI URI URL URLS UTC UUID UX
    XML YAML
    """.split()
)


def style_new_description(source: str) -> str:
    """Apply house style to a connector description from scratch.

    Used directly when a column is added (there is no article cell to copy presentation
    from) and as the first step of `restyle` when one is replaced.
    """
    text = source.strip()
    for dash, replacement in DASH_REPLACEMENTS.items():
        text = text.replace(dash, replacement)
    for pattern, replacement in HOUSE_TERMS:
        text = pattern.sub(replacement, text)
    text = ENUM_TOKEN_RE.sub(
        lambda m: m.group(1) if m.group(1) in ACRONYMS else f"`{m.group(1)}`", text
    )
    text = LITERAL_TOKEN_RE.sub(r"`\1`", text)
    if not text.endswith((".", "!", "?", ":")):
        text += "."
    return text


def restyle(source: str, existing: str) -> str:
    """Take the connector's wording and put it back into house style.

    The comparison contract says the two sides differ in presentation, not substance. That
    cuts both ways: when the connector's substance wins, the article's presentation still
    applies. Code-formatted values stay code-formatted, sentences stay terminated, and no
    en or em dash makes it into the file.
    """
    text = style_new_description(source)

    # Re-apply backticks to any value the article code-formatted, first occurrence only,
    # on a word boundary, and never inside an existing code span. A value the connector
    # put in straight quotes gets the quotes swapped for backticks rather than nested.
    for token in dict.fromkeys(CODE_SPAN_RE.findall(existing)):
        token = token.strip()
        if not token or f"`{token}`" in text:
            continue
        quoted = re.compile(rf'"{re.escape(token)}"')
        text, replaced = quoted.subn(f"`{token}`", text, count=1)
        if replaced:
            continue
        bare = re.compile(rf"(?<![`\w]){re.escape(token)}(?![`\w])")
        text = bare.sub(f"`{token}`", text, count=1)

    if not text.endswith((".", "!", "?", ":")):
        text += "."
    return text


def description_regression(source: str, existing: str) -> Optional[str]:
    """Why replacing `existing` with `source` would lose information, or None.

    The connector's descriptions are not all better than the article's: the article was
    hand-audited and several of its cells enumerate enum members or add caveats that the
    Java string does not carry. Replacing those would quietly undo that work, so they are
    reported for a human instead of applied.
    """
    haystack = normalize(source).casefold()
    dropped = [
        token
        for token in dict.fromkeys(CODE_SPAN_RE.findall(existing))
        if token.strip() and token.strip().casefold() not in haystack
    ]
    if dropped:
        return "the article documents values the connector string does not: " + ", ".join(
            f"`{t}`" for t in dropped[:6]
        )
    if len(normalize(existing)) and len(haystack) < SHRINK_RATIO * len(
        normalize(existing)
    ):
        return "the connector string is much shorter than the article's description"
    return None


def _resolve_description(
    column: ManifestColumn,
    existing: str,
    mode: str,
    section_name: str,
    updates: list[dict],
) -> str:
    """Decide the description cell for a column present on both sides.

    The single most important safety rule lives here: when the connector has no
    description, the article's is authoritative and is left untouched.
    """
    source = column.description.strip()
    if not source:
        return existing

    # Substance decides, and casing is presentation: the article writes "DataSet" where
    # Java writes "dataset". Comparing case-sensitively would rewrite cells that already
    # carry the connector's wording, on every run.
    def same(a: str, b: str) -> bool:
        return normalize(a).casefold() == normalize(b).casefold()

    if same(source, existing):
        return existing

    replacement = restyle(source, existing)
    # Restyling can land back on the article's own wording (dashes, house terms, backticks
    # are all reversible presentation). That is not a change.
    if same(replacement, existing):
        return existing
    record = {
        "report": section_name,
        "field": column.name,
        "from": existing,
        "to": replacement,
        "applied": False,
        "reason": None,
    }

    if mode == "report-only":
        record["reason"] = "--descriptions report-only"
        updates.append(record)
        return existing

    if mode == "safe":
        regression = description_regression(source, existing)
        if regression is not None:
            record["reason"] = regression
            updates.append(record)
            return existing

    record["applied"] = True
    updates.append(record)
    return escape_pipes(replacement)


def _looks_like_enum(column: ManifestColumn) -> bool:
    if not ENUM_HINT_RE.search(column.name):
        return False
    # A numeric or temporal column named "Type" is an id or a timestamp, not an enum.
    return column.type in ("", "STRING")


# ---------------------------------------------------------------------------
# Adding a section for a report the article does not document
# ---------------------------------------------------------------------------


def _undocumented(
    manifest: ManifestReport, reason: str, redact: bool, **extra
) -> dict:
    """One "the connector has this, the article does not" record.

    With `redact` on (the default, because this repository is public) the report's name
    and key are withheld. Naming an undocumented report in a public PR body discloses that
    it exists, which for an unreleased feature is exactly the disclosure the opt-in policy
    is there to prevent. The count still surfaces, so the gap is visible without the leak.
    """
    if redact:
        # The unresolved reasons name the Java class they were derived from, which is as
        # identifying as the report name itself. Collapse them to the category.
        reason = REDACTED_REASONS.get(reason, reason)
        if reason.startswith("no static List<Column>"):
            reason = SKIP_REASON_UNRESOLVED
    record = {"reason": reason, "action": "not added", "withheld": redact, **extra}
    if not redact:
        record["report"] = manifest.display_name
        record["key"] = manifest.key
    return record


def render_section(manifest: ManifestReport, report: Report) -> list[str]:
    """The MDX for a brand-new report section: heading, table, nothing else.

    Deliberately no `<Note>`. Feature-switch note wording was hand-audited; when this
    report is gated the PR body carries the suggestion instead.
    """
    lines = [f"### {escape_pipes(manifest.display_name)}", ""]
    header = ["Field", "Description"]
    rows = []
    additions: list[dict] = []
    for column in manifest.columns or []:
        rows.append(_new_row(column, False, manifest.display_name, additions, report))
    table = Table(0, 0, header, rows, False, False)
    lines.extend(table.render())
    lines.append("")

    if manifest.feature_switch:
        report.gating_suggestions.append(
            {
                "report": manifest.display_name,
                "featureSwitch": manifest.feature_switch,
                "suggestion": (
                    "This report is gated by the "
                    f"`{manifest.feature_switch}` feature switch. Add a feature-switch "
                    "Note only if the switch does not default on."
                ),
            }
        )
    return lines


def insertion_index(sections: list[Section], name: str) -> int:
    """Where a new `### <name>` section belongs, honouring the curated blocks.

    `Domo Goals | *` and `PDP - *` are hand-ordered: a new member is appended to its
    block. Everything else is alphabetical, and the search steps over a curated block
    rather than landing inside it.
    """
    prefix = next((p for p in CURATED_PREFIXES if name.startswith(p)), None)
    if prefix is not None:
        members = [s for s in sections if s.name.startswith(prefix)]
        if members:
            return members[-1].end
        # No block yet: fall through and place it alphabetically.

    key = name.casefold()
    for section in sections:
        if section.curated_prefix is not None:
            # Never split a curated block. Compare against the block as a whole.
            if key < section.curated_prefix.casefold():
                return section.start
            continue
        if key < section.name.casefold():
            return section.start
    return sections[-1].end if sections else -1


def pane_row(manifest: ManifestReport, bold: bool) -> list[str]:
    return [
        escape_pipes(manifest.display_name),
        f"TODO: describe the {manifest.display_name} report.",
    ]


# ---------------------------------------------------------------------------
# Applying everything to the article
# ---------------------------------------------------------------------------


def reconcile(
    article: Article,
    reports: list[ManifestReport],
    config: dict,
    descriptions_mode: str,
    redact: bool = True,
) -> tuple[list[str], Report]:
    """Returns the new article lines and the reconciliation report."""
    result = Report()
    excluded = set(config.get("excludedReportKeys") or [])
    excluded_sections = set(config.get("excludedSections") or [])
    excluded_columns = {
        normalize_field(name) for name in (config.get("excludedColumns") or [])
    }
    documented_keys = set(config.get("documentedReportKeys") or [])
    opt_in = config.get("newReportPolicy", "opt-in") != "auto"

    documented = [r for r in reports if r.key not in excluded]
    pairings, orphans = pair_reports(documented, article.sections)

    for pairing in pairings:
        if pairing.section is not None and not pairing.exact:
            result.name_drift.append(
                {
                    "report": pairing.report.display_name,
                    "article": pairing.section.name,
                    "connector": pairing.report.display_name,
                    "note": "heading text differs; the heading is left as written",
                }
            )

    # A section with no manifest report at all: the report may have been removed from the
    # connector, or renamed beyond what normalization pairs up. Never delete either way.
    for section in orphans:
        if section.name in excluded_sections:
            continue
        result.reports_removed.append(
            {"section": section.name, "action": "left in place"}
        )

    # ---- rewrite the tables of paired sections ------------------------
    # Collect edits first, then apply back to front so earlier line indices stay valid.
    edits: list[tuple[int, int, list[str]]] = []
    for pairing in pairings:
        if pairing.section is None:
            continue
        table = reconcile_section(
            pairing, result, descriptions_mode, excluded_columns
        )
        if table is not None:
            edits.append((table.start, table.end, table.render()))

    # ---- new sections -------------------------------------------------
    #
    # A report the connector has and the article does not is not merely a docs gap: it is
    # a report that exists in the connector but has not shipped to customers yet. Domo cuts
    # a branch roughly six weeks before feature release, so auto-proposing a section the
    # night a report merges to master would announce an unreleased feature in a public
    # draft PR. Hence opt-in: a human adds the key to `documentedReportKeys` once the report
    # is announceable, and only then does a section appear. Set `newReportPolicy` to
    # "auto" to restore the eager behaviour (appropriate only if this repo goes private).
    new_sections: list[tuple[int, str, list[str]]] = []
    for pairing in pairings:
        if pairing.section is not None:
            continue
        manifest = pairing.report

        def not_added(reason: str, **extra) -> None:
            result.reports_undocumented.append(
                _undocumented(manifest, reason, redact, **extra)
            )

        if manifest.unresolved or manifest.columns is None:
            not_added(manifest.unresolved_reason or SKIP_REASON_UNRESOLVED)
            continue
        if not manifest.generally_available:
            not_added(
                SKIP_REASON_RESTRICTED, restrictionKinds=manifest.restriction_kinds
            )
            continue
        if opt_in and manifest.key not in documented_keys:
            not_added(SKIP_REASON_NOT_OPTED_IN)
            continue
        at = insertion_index(article.sections, manifest.display_name)
        if at < 0:
            continue
        new_sections.append((at, manifest.display_name, render_section(manifest, result)))
        result.applied_reports_added.append(
            {
                "report": manifest.display_name,
                "key": manifest.key,
                "columns": len(manifest.columns),
            }
        )

    # ---- Details Pane index -------------------------------------------
    pane_additions: list[list[str]] = []
    if article.details_pane is not None:
        pane = article.details_pane
        existing = {normalize_report(unescape_pipes(row[0])) for row in pane.rows}
        section_names = {normalize_report(s.name) for s in article.sections}
        for added in result.applied_reports_added:
            if normalize_report(added["report"]) not in existing:
                manifest = next(r for r in documented if r.display_name == added["report"])
                pane_additions.append(pane_row(manifest, pane.bold_header))
        for row in pane.rows:
            if normalize_report(unescape_pipes(row[0])) not in section_names:
                result.pane_drift.append(
                    {
                        "paneRow": unescape_pipes(row[0]),
                        "issue": "listed in the Details Pane with no matching field section",
                    }
                )
        for section in article.sections:
            if normalize_report(section.name) not in existing:
                result.pane_drift.append(
                    {
                        "section": section.name,
                        "issue": "has a field section but no Details Pane row",
                    }
                )
    else:
        result.notes.append(
            "Details Pane table not found; report-index rows were not reconciled."
        )

    # ---- splice ------------------------------------------------------
    lines = list(article.lines)

    if pane_additions and article.details_pane is not None:
        pane = article.details_pane
        rows = list(pane.rows)
        for row in pane_additions:
            key = normalize_report(unescape_pipes(row[0]))
            at = next(
                (
                    i
                    for i, existing_row in enumerate(rows)
                    if key < normalize_report(unescape_pipes(existing_row[0]))
                ),
                len(rows),
            )
            rows.insert(at, row)
        replacement = Table(
            pane.start, pane.end, pane.header, rows, pane.bold_header, False
        )
        edits.append((pane.start, pane.end, replacement.render()))

    # Several new sections can land at the same insertion point. Group them and lay them
    # out alphabetically inside the group, or the reverse-order splice below would emit
    # them backwards.
    grouped: dict[int, list[tuple[str, list[str]]]] = {}
    for at, name, block in new_sections:
        grouped.setdefault(at, []).append((name, block))
    for at, members in grouped.items():
        block: list[str] = []
        for _, member_block in sorted(members, key=lambda m: m[0].casefold()):
            block.extend(member_block)
        edits.append((at, at, block))

    for start, end, block in sorted(edits, key=lambda e: e[0], reverse=True):
        lines[start:end] = block

    return lines, result


# ---------------------------------------------------------------------------
# Japanese drift
# ---------------------------------------------------------------------------


def check_japanese(en: Article, ja_path: Path, result: Report) -> None:
    """Compare section and row counts against English and name the drifted sections.

    Localization cannot be byte-compared, so this only reports. The Japanese article is
    never edited here; run the `localize` skill after the English is approved.
    """
    if not ja_path.is_file():
        result.notes.append(f"{ja_path} not found; Japanese drift not checked.")
        return
    try:
        ja = parse_article(ja_path, require_english_heading=False)
    except Refusal as exc:
        result.notes.append(f"Japanese article not parsed: {exc}")
        return

    def rows_of(section: Section) -> int:
        return len(section.table.rows) if section.table else 0

    # Report section headings are untranslated in the mirrors (the DataSet name is the
    # heading), so pair on the heading. Position pairing would misreport every section
    # after the first English insertion, which is exactly when this check runs.
    ja_by_name = {normalize_report(s.name): s for s in ja.sections}
    matched = sum(1 for s in en.sections if normalize_report(s.name) in ja_by_name)

    if en.sections and matched < len(en.sections) / 2:
        # A locale that does translate its headings. Fall back to position pairing and
        # say so, rather than reporting every section as missing.
        result.notes.append(
            f"{ja_path}: headings do not match English, so drift was compared by "
            "position rather than by section name."
        )
        for index, section in enumerate(en.sections):
            if index >= len(ja.sections):
                result.ja_drift.append(
                    {"section": section.name, "issue": "no localized section at this position"}
                )
                continue
            if rows_of(section) != rows_of(ja.sections[index]):
                result.ja_drift.append(
                    {
                        "section": section.name,
                        "japaneseSection": ja.sections[index].name,
                        "issue": "row count differs",
                        "english": rows_of(section),
                        "japanese": rows_of(ja.sections[index]),
                    }
                )
        return

    for section in en.sections:
        ja_section = ja_by_name.get(normalize_report(section.name))
        if ja_section is None:
            result.ja_drift.append(
                {"section": section.name, "issue": "missing from the Japanese mirror"}
            )
            continue
        if rows_of(section) != rows_of(ja_section):
            result.ja_drift.append(
                {
                    "section": section.name,
                    "japaneseSection": ja_section.name,
                    "issue": "row count differs",
                    "english": rows_of(section),
                    "japanese": rows_of(ja_section),
                }
            )

    en_names = {normalize_report(s.name) for s in en.sections}
    for ja_section in ja.sections:
        if normalize_report(ja_section.name) not in en_names:
            result.ja_drift.append(
                {
                    "section": ja_section.name,
                    "issue": "in the Japanese mirror but not in English",
                }
            )


# ---------------------------------------------------------------------------
# Description drafting
# ---------------------------------------------------------------------------


def _anthropic_client(api_key: str):
    """Constructed through a module-level indirection so tests can stub it out."""
    from anthropic import Anthropic

    return Anthropic(api_key=api_key)


def draft_descriptions(
    lines: list[str],
    result: Report,
    model: str,
    article_path: Path,
    api_key: Optional[str] = None,
) -> list[str]:
    """Fill in the TODO descriptions for columns the connector gave no description for.

    One Anthropic call per column, given the column name, its DataType, the report it
    belongs to, and the neighbouring rows for tone. Constrained hard: one sentence,
    matching voice, no invented enum values. Anything enum-shaped keeps its verify marker,
    because enum members live in `convertToString` methods that the model cannot see.

    A failure here is never fatal: the placeholder stays and the reason goes in the report.
    """
    pending = [a for a in result.applied_columns_added if a.get("needsDraft")]
    if not pending:
        return lines

    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        result.notes.append(
            f"{len(pending)} new columns need a description but ANTHROPIC_API_KEY is not "
            "set; they were left as TODO."
        )
        return lines

    try:
        client = _anthropic_client(api_key)
    except ImportError:
        result.notes.append(
            "anthropic SDK not installed; new column descriptions were left as TODO."
        )
        return lines

    text = "\n".join(lines)

    for item in pending:
        neighbours = _neighbour_rows(lines, item["report"])
        prompt = (
            "You are writing one field description for a Domo knowledge base reference "
            "table. The table documents the columns of a DomoStats connector report.\n\n"
            f"Report: {item['report']}\n"
            f"Column name: {item['field']}\n"
            f"Column data type: {item['type'] or 'unknown'}\n\n"
            "Neighbouring rows from the same table, for voice and length:\n"
            f"{neighbours}\n\n"
            "Write exactly one sentence describing what this column contains. Rules:\n"
            "- Match the voice, tense and length of the neighbouring rows.\n"
            "- Start with 'The' or 'Indicates whether' where that fits the neighbours.\n"
            "- End with a single period.\n"
            "- Do not invent enum values, example values, or units.\n"
            "- Do not mention Java, the connector, or the schema.\n"
            "- Do not use an em dash.\n"
            "- Output only the sentence."
        )
        try:
            response = client.messages.create(
                model=model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            drafted = response.content[0].text.strip().strip('"').strip()
        except Exception as exc:  # noqa: BLE001 - reported, never fatal
            result.notes.append(
                f"description draft failed for {item['report']} / {item['field']}: "
                f"{type(exc).__name__}"
            )
            continue
        if not drafted:
            continue
        if not drafted.endswith((".", "!", "?")):
            drafted += "."

        placeholder = "TODO: describe this field."
        marker = f" {VERIFY_MARKER}" if VERIFY_MARKER in _cell_for(text, item) else ""
        old_cell = escape_pipes(placeholder + marker)
        new_cell = escape_pipes(drafted + marker)
        text = _replace_cell(text, item["field"], old_cell, new_cell)
        item["description"] = drafted + marker
        item["needsDraft"] = False
        result.drafted_descriptions.append(
            {"report": item["report"], "field": item["field"], "description": drafted}
        )

    return text.split("\n")


def _neighbour_rows(lines: list[str], section_name: str, limit: int = 6) -> str:
    heading = f"### {escape_pipes(section_name)}"
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        return "(none)"
    rows = []
    for line in lines[start : start + 200]:
        if line.strip().startswith("|") and not is_separator(split_row(line)):
            cells = split_row(line)
            if len(cells) >= 2 and "TODO: describe this field." not in cells[1]:
                rows.append(f"{cells[0]}: {cells[1]}")
        if len(rows) >= limit + 1:
            break
    return "\n".join(rows[1 : limit + 1]) or "(none)"


def _cell_for(text: str, item: dict) -> str:
    for line in text.split("\n"):
        cells = split_row(line) if line.strip().startswith("|") else []
        if cells and cells[0] == escape_pipes(item["field"]):
            return cells[1] if len(cells) > 1 else ""
    return ""


def _replace_cell(text: str, field_name: str, old_cell: str, new_cell: str) -> str:
    out = []
    replaced = False
    for line in text.split("\n"):
        if not replaced and line.strip().startswith("|"):
            cells = split_row(line)
            if (
                len(cells) >= 2
                and cells[0] == escape_pipes(field_name)
                and cells[1] == old_cell
            ):
                cells[1] = new_cell
                out.append("| " + " | ".join(cells) + " |")
                replaced = True
                continue
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# PR body
# ---------------------------------------------------------------------------


def render_pr_body(result: Report, manifest_meta: dict, article_path: Path) -> str:
    sha = manifest_meta.get("generatedFrom") or "unknown"
    stats = manifest_meta.get("stats") or {}
    out: list[str] = []
    out.append("## DomoStats schema sync")
    out.append("")
    out.append(
        f"Reconciled `{article_path}` against the connector schema manifest generated "
        f"from `domostats@{sha[:12] if sha != 'unknown' else sha}`."
    )
    out.append("")
    out.append(
        f"- Reports in manifest: **{stats.get('reports', '?')}** "
        f"({stats.get('unresolvedReports', '?')} with no resolvable schema)"
    )
    out.append(f"- Changes applied: **{result.applied_count}**")
    out.append(f"- Items needing a human: **{result.review_count}**")
    out.append("")

    def block(title: str, items: list, render_item) -> None:
        if not items:
            return
        out.append(f"### {title} ({len(items)})")
        out.append("")
        for item in items:
            out.append(f"- {render_item(item)}")
        out.append("")

    out.append("---")
    out.append("")
    out.append("## Applied")
    out.append("")
    if not result.applied_count:
        out.append("Nothing to apply. The article already matches the connector.")
        out.append("")

    block(
        "Reports added",
        result.applied_reports_added,
        lambda i: f"**{i['report']}** (`{i['key']}`), {i['columns']} columns",
    )
    block(
        "Columns added",
        result.applied_columns_added,
        lambda i: (
            f"**{i['report']}** / `{i['field']}` ({i['type'] or 'unknown type'})"
            + (" - description still `TODO`" if i.get("needsDraft") else "")
        ),
    )
    block(
        "Descriptions updated from the connector",
        [i for i in result.applied_descriptions if i.get("applied")],
        lambda i: (
            f"**{i['report']}** / `{i['field']}`\n"
            f"  - was: {i['from']}\n"
            f"  - now: {i['to']}"
        ),
    )
    block(
        "Rows reordered to schema order",
        result.applied_reordered,
        lambda i: f"**{i['report']}**",
    )
    block(
        "Descriptions drafted for new columns",
        result.drafted_descriptions,
        lambda i: f"**{i['report']}** / `{i['field']}`: {i['description']}",
    )

    out.append("---")
    out.append("")
    out.append("## Needs a human")
    out.append("")
    if not result.review_count:
        out.append("Nothing outstanding.")
        out.append("")

    block(
        "Verify enum values",
        result.verify_enums,
        lambda i: (
            f"[ ] **{i['report']}** / `{i['field']}`: enum members live in the report's "
            "`convertToString` method, not in the schema. Confirm the value list."
        ),
    )
    block(
        "Descriptions the connector changed but the article kept",
        [i for i in result.applied_descriptions if not i.get("applied")],
        lambda i: (
            f"[ ] **{i['report']}** / `{i['field']}` - not applied because {i['reason']}\n"
            f"  - article: {i['from']}\n"
            f"  - connector: {i['to']}"
        ),
    )
    block(
        "Columns the article has and the connector does not",
        result.columns_removed,
        lambda i: (
            f"[ ] **{i['report']}** / `{i['field']}` - left in place. Remove it only if "
            "the column really is gone."
        ),
    )
    block(
        "Columns the connector declares twice",
        result.duplicate_columns,
        lambda i: (
            f"[ ] **{i['report']}** / `{i['field']}` is declared twice in "
            f"`{(i['schemaClass'] or '').split('.')[-1]}`. Only the first was used. This "
            "is a connector bug worth filing."
        ),
    )
    block(
        "Sections with no matching connector report",
        result.reports_removed,
        lambda i: f"[ ] **{i['section']}** - left in place. Removed upstream, or renamed?",
    )
    withheld = [i for i in result.reports_undocumented if i.get("withheld")]
    if withheld:
        out.append(f"### Connector reports the article does not document ({len(withheld)})")
        out.append("")
        out.append(
            "Their names are withheld: this repository is public, and a report can exist "
            "in the connector weeks before its feature ships. Look them up in "
            "`domostats-schema.json` in the connector repo, then add the ones that are "
            "announceable to `documentedReportKeys` in "
            "`.github/domostats-sync-config.json` to have sections generated for them."
        )
        out.append("")
        for reason, count in sorted(Counter(i["reason"] for i in withheld).items()):
            out.append(f"- [ ] {count} x {reason}")
        out.append("")
    block(
        "Connector reports the article does not document",
        [i for i in result.reports_undocumented if not i.get("withheld")],
        lambda i: (
            f"[ ] **{i['report']}** (`{i['key']}`) - not added: {i['reason']}. "
            "Add the report key to `documentedReportKeys` in "
            "`.github/domostats-sync-config.json` to have a section generated for it."
        ),
    )
    block(
        "Reports with no resolvable schema",
        result.reports_unresolved,
        lambda i: (
            f"[ ] **{i['report']}** (`{i['key']}`): {i['reason']}. A connector dev can fix "
            "this with one line on the Report class: "
            "`public static final List<Column> SCHEMA = XRow.schema;`"
        ),
    )
    if result.reports_restricted:
        out.append(f"### Reports gated by environment or customer ({len(result.reports_restricted)})")
        out.append("")
        out.append(
            "Their tables are left untouched. The manifest records the kind of restriction "
            "only; the allowlist itself never leaves the connector repo."
        )
        out.append("")
        for item in result.reports_restricted:
            kinds = ", ".join(item["restrictionKinds"]) or "unknown"
            out.append(f"- [ ] **{item['report']}** (`{item['key']}`): {kinds}")
        out.append("")
    block(
        "Feature-switch gating (suggestion only)",
        result.gating_suggestions,
        lambda i: f"[ ] **{i['report']}**: {i['suggestion']}",
    )
    block(
        "Name drift",
        result.name_drift,
        lambda i: (
            f"[ ] **{i.get('report', '')}**: article says `{i['article']}`, connector says "
            f"`{i['connector']}`. Headings and field names are never rewritten."
        ),
    )
    block(
        "Details Pane index drift",
        result.pane_drift,
        lambda i: f"[ ] {i.get('section') or i.get('paneRow')}: {i['issue']}",
    )
    block(
        "Japanese sections to re-localize",
        result.ja_drift,
        lambda i: (
            f"[ ] {i.get('section', i.get('issue'))}: {i['issue']}"
            + (
                f" (en={i['english']}, ja={i['japanese']})"
                if "english" in i
                else ""
            )
        ),
    )

    if result.sections_skipped:
        out.append("---")
        out.append("")
        out.append(f"<details><summary>Sections skipped ({len(result.sections_skipped)})"
                   "</summary>")
        out.append("")
        for item in result.sections_skipped:
            detail = f" - {item['detail']}" if item.get("detail") else ""
            out.append(f"- **{item['section']}**: {item['reason']}{detail}")
        out.append("")
        out.append("</details>")
        out.append("")

    if result.notes:
        out.append("---")
        out.append("")
        out.append("### Run notes")
        out.append("")
        for note in result.notes:
            out.append(f"- {note}")
        out.append("")

    out.append("---")
    out.append("")
    out.append(
        "Japanese is not edited by this workflow. After the English is approved, run the "
        "`localize` skill on the sections listed above."
    )
    out.append("")
    out.append("*Opened automatically by `.github/workflows/sync-domostats-schema.yml`.*")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def write_github_output(has_changes: bool, summary: str) -> None:
    """Emit workflow outputs using the heredoc form detect_yaml_changes.py uses."""
    output_file = os.environ.get("GITHUB_OUTPUT", "/dev/stdout")
    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"has_changes={'true' if has_changes else 'false'}\n")
        handle.write(f"summary<<EOF\n{summary}\nEOF\n")


def pad_tables(path: Path) -> None:
    """Run the repo's table padder so the rewritten tables match house formatting."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    try:
        import pad_md_tables  # type: ignore
    except ImportError:
        print("warning: scripts/pad_md_tables.py not importable; tables left unpadded")
        return
    original = path.read_text(encoding="utf-8")
    updated = pad_md_tables.process(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Path to domostats-schema.json")
    parser.add_argument(
        "--article", default="s/article/360043433813.mdx", help="English article"
    )
    parser.add_argument(
        "--ja-article",
        default="ja/s/article/360043433813.mdx",
        help="Japanese mirror, checked for drift and never edited",
    )
    parser.add_argument(
        "--config",
        default=".github/domostats-sync-config.json",
        help="Optional sync config (excludedReportKeys, excludedSections)",
    )
    parser.add_argument("--report-json", help="Write the machine-readable report here")
    parser.add_argument("--pr-body", help="Write the rendered PR body here")
    parser.add_argument(
        "--dry-run", action="store_true", help="Compute everything, write no article"
    )
    parser.add_argument(
        "--descriptions",
        choices=("safe", "source-wins", "report-only"),
        default="safe",
        help=(
            "safe (default): a non-empty connector description replaces the article's, "
            "restyled to house style, unless doing so would drop values the article "
            "documents or shorten it substantially. "
            "source-wins: always replace. "
            "report-only: never replace, just list the differences."
        ),
    )
    parser.add_argument(
        "--no-redact",
        dest="redact",
        action="store_false",
        help=(
            "Name undocumented reports in the PR body and report JSON. Only safe when the "
            "output stays private; this repository is public, so redaction is the default."
        ),
    )
    parser.add_argument(
        "--draft-descriptions",
        action="store_true",
        help="Ask Claude to draft descriptions for new columns the connector left blank",
    )
    parser.add_argument("--model", default="claude-sonnet-5", help="Drafting model")
    parser.add_argument(
        "--force",
        default="false",
        help="Reserved for workflow parity with detect_yaml_changes.py",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    article_path = Path(args.article)
    for path in (manifest_path, article_path):
        if not path.is_file():
            sys.stderr.write(f"ERROR: {path} not found\n")
            return 2

    config = {}
    config_path = Path(args.config)
    if config_path.is_file():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    try:
        reports, manifest_meta = load_manifest(manifest_path)
    except (json.JSONDecodeError, KeyError) as exc:
        sys.stderr.write(f"ERROR: could not read {manifest_path}: {exc}\n")
        return 2

    try:
        article = parse_article(article_path)
    except Refusal as exc:
        sys.stderr.write(f"REFUSED: {exc}\n")
        return 1

    lines, result = reconcile(
        article, reports, config, args.descriptions, redact=args.redact
    )
    check_japanese(article, Path(args.ja_article), result)

    if args.draft_descriptions:
        lines = draft_descriptions(lines, result, args.model, article_path)

    changed = lines != article.lines
    if changed and not args.dry_run:
        article_path.write_text("\n".join(lines), encoding="utf-8")
        pad_tables(article_path)

    summary = _summary(result, changed, args.dry_run)
    print(summary)

    if args.report_json:
        Path(args.report_json).write_text(
            json.dumps(result.to_json(), indent=2) + "\n", encoding="utf-8"
        )
    if args.pr_body:
        Path(args.pr_body).write_text(
            render_pr_body(result, manifest_meta, article_path) + "\n", encoding="utf-8"
        )
    if os.environ.get("GITHUB_OUTPUT"):
        write_github_output(changed, summary)

    return 0


def _summary(result: Report, changed: bool, dry_run: bool) -> str:
    verb = "would change" if dry_run else "changed"
    lines = [
        f"DomoStats reconcile: {result.applied_count} change(s) applied "
        f"({verb} the article: {changed}), {result.review_count} item(s) need a human.",
        f"  reports added:        {len(result.applied_reports_added)}",
        f"  columns added:        {len(result.applied_columns_added)}",
        f"  descriptions synced:  {len([d for d in result.applied_descriptions if d.get('applied')])}",
        f"  descriptions to review:{len([d for d in result.applied_descriptions if not d.get('applied')])}",
        f"  sections reordered:   {len(result.applied_reordered)}",
        f"  columns to review:    {len(result.columns_removed)}",
        f"  duplicate columns:    {len(result.duplicate_columns)}",
        f"  sections to review:   {len(result.reports_removed)}",
        f"  unresolved reports:   {len(result.reports_unresolved)}",
        f"  restricted reports:   {len(result.reports_restricted)}",
        f"  undocumented reports: {len(result.reports_undocumented)}",
        f"  sections skipped:     {len(result.sections_skipped)}",
        f"  JA drift items:       {len(result.ja_drift)}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
