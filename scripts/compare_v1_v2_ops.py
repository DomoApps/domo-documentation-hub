#!/usr/bin/env python3
"""
Compare v1 and v2 document operation definitions in openapi/framework/appdb.yaml.

For each matching v1/v2 pair, prints a structured diff so you can confirm
which differences are intentional (v2 additions) and which are accidental
gaps or inconsistencies.

Usage:
    python3 scripts/compare_v1_v2_ops.py
"""

import sys
import yaml
from pathlib import Path

SPEC_PATH = Path(__file__).parent.parent / "openapi/framework/appdb.yaml"

# Fields that are expected to differ and aren't worth flagging every time
SKIP_KEYS = {"x-excluded", "x-codeSamples"}

# v1 path → v2 path (operation pairs to compare)
PAIRS = [
    ("POST",   "/domo/datastores/v1/collections/{collectionName}/documents",
               "/domo/datastores/v2/collections/{collectionName}/documents"),
    ("GET",    "/domo/datastores/v1/collections/{collectionName}/documents",
               "/domo/datastores/v2/collections/{collectionName}/documents"),
    ("GET",    "/domo/datastores/v1/collections/{collectionName}/documents/{documentId}",
               "/domo/datastores/v2/collections/{collectionName}/documents/{documentId}"),
    ("PUT",    "/domo/datastores/v1/collections/{collectionName}/documents/{documentId}",
               "/domo/datastores/v2/collections/{collectionName}/documents/{documentId}"),
    ("DELETE", "/domo/datastores/v1/collections/{collectionName}/documents/{documentId}",
               "/domo/datastores/v2/collections/{collectionName}/documents/{documentId}"),
    ("POST",   "/domo/datastores/v1/collections/{collectionName}/documents/query",
               "/domo/datastores/v2/collections/{collectionName}/documents/query"),
    ("PUT",    "/domo/datastores/v1/collections/{collectionName}/documents/update",
               "/domo/datastores/v2/collections/{collectionName}/documents/update"),
    ("POST",   "/domo/datastores/v1/collections/{collectionName}/documents/bulk",
               "/domo/datastores/v2/collections/{collectionName}/documents/bulk"),
    ("PUT",    "/domo/datastores/v1/collections/{collectionName}/documents/bulk",
               "/domo/datastores/v2/collections/{collectionName}/documents/bulk"),
    ("DELETE", "/domo/datastores/v1/collections/{collectionName}/documents/bulk",
               "/domo/datastores/v2/collections/{collectionName}/documents/bulk"),
]


def deep_diff(a, b, path=""):
    """Yield (path, kind, v1_val, v2_val) tuples for every difference."""
    if type(a) != type(b):
        yield (path, "type_changed", type(a).__name__, type(b).__name__)
        yield (path, "value", a, b)
        return

    if isinstance(a, dict):
        all_keys = set(a) | set(b)
        for k in sorted(all_keys):
            if k in SKIP_KEYS:
                continue
            child = f"{path}.{k}" if path else k
            if k not in a:
                yield (child, "added_in_v2", None, b[k])
            elif k not in b:
                yield (child, "removed_in_v2", a[k], None)
            else:
                yield from deep_diff(a[k], b[k], child)

    elif isinstance(a, list):
        # For lists: compare element by element by index
        for i, (ea, eb) in enumerate(zip(a, b)):
            yield from deep_diff(ea, eb, f"{path}[{i}]")
        if len(a) > len(b):
            for i in range(len(b), len(a)):
                yield (f"{path}[{i}]", "removed_in_v2", a[i], None)
        elif len(b) > len(a):
            for i in range(len(a), len(b)):
                yield (f"{path}[{i}]", "added_in_v2", None, b[i])

    else:
        # Scalar — normalise v1/v2 strings before comparing so URL differences
        # in descriptions don't flood the output
        def normalise(v):
            if isinstance(v, str):
                return v.replace("/v1/", "/vN/").replace("/v2/", "/vN/") \
                         .replace("(v1)", "").replace("(v2)", "").strip()
            return v

        if normalise(a) != normalise(b):
            yield (path, "changed", a, b)


def fmt_val(v, indent=4):
    if v is None:
        return "(absent)"
    s = str(v)
    if "\n" in s or len(s) > 80:
        lines = s.splitlines()
        pad = " " * indent
        return "\n" + "\n".join(pad + l for l in lines)
    return repr(v)


def operation_label(method, path):
    # Extract the interesting part of the path
    tail = path.split("/documents", 1)[-1] or "/documents"
    return f"{method} .../documents{tail}"


def main():
    spec = yaml.safe_load(SPEC_PATH.read_text())
    paths = spec.get("paths", {})

    any_diff = False
    for method, v1_path, v2_path in PAIRS:
        m = method.lower()
        v1_op = paths.get(v1_path, {}).get(m)
        v2_op = paths.get(v2_path, {}).get(m)

        if v1_op is None:
            print(f"[MISSING] v1 {method} {v1_path}")
            continue
        if v2_op is None:
            print(f"[MISSING] v2 {method} {v2_path}")
            continue

        diffs = list(deep_diff(v1_op, v2_op))
        label = operation_label(method, v1_path)

        if not diffs:
            print(f"  OK  {label}")
        else:
            any_diff = True
            print(f"\n{'='*70}")
            print(f"DIFF  {label}")
            print(f"{'='*70}")
            for path, kind, old, new in diffs:
                if kind == "added_in_v2":
                    print(f"  + {path}")
                    print(f"      v2 value: {fmt_val(new)}")
                elif kind == "removed_in_v2":
                    print(f"  - {path}")
                    print(f"      v1 value: {fmt_val(old)}")
                elif kind in ("changed", "value"):
                    print(f"  ~ {path}")
                    print(f"      v1: {fmt_val(old)}")
                    print(f"      v2: {fmt_val(new)}")
                elif kind == "type_changed":
                    print(f"  ! {path}  (type: {old} → {new})")

    if not any_diff:
        print("\nNo meaningful differences found.")


if __name__ == "__main__":
    main()
