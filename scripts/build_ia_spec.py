#!/usr/bin/env python3
"""
Phase 2: Build the Information Architecture spec.

Reads catalog-classified.json and assigns every article to one of the
11 new content pillars (plus Release Notes and Archive).

Outputs:
  scripts/output/ia-spec.json    — full pillar → group → article tree
  scripts/output/ia-mapping.json — flat {filename: {pillar, group, sub_group}} lookup

Usage:
    python3 scripts/build_ia_spec.py
"""

import json
import re
from collections import defaultdict

CATALOG = "scripts/output/catalog-classified.json"

# ---------------------------------------------------------------------------
# Pillar assignment rules
# Each rule: (pillar, sub_group, match_fn(entry)) — first match wins
# ---------------------------------------------------------------------------

def nav_contains(entry, *fragments):
    ng = (entry.get("nav_group") or "").lower()
    return any(f.lower() in ng for f in fragments)

def title_contains(entry, *fragments):
    t = (entry.get("title") or "").lower()
    return any(f.lower() in t for f in fragments)

def excerpt_contains(entry, *fragments):
    ex = (entry.get("excerpt") or "").lower()
    return any(f.lower() in ex for f in fragments)

# ---------------------------------------------------------------------------
# Specific article overrides (filename → (pillar, group, sub_group))
# ---------------------------------------------------------------------------
OVERRIDES = {
    # Getting Started
    "Getting-Started-for-Data-Consumers.mdx":  ("Getting Started", "By Role", None),
    "Getting-Started-for-Data-Engineers.mdx":  ("Getting Started", "By Role", None),
    "000005874.mdx":  ("Getting Started", "Key Resources", None),  # Introduction to Domo
    "000005878.mdx":  ("Getting Started", "Key Resources", None),  # First 5 Things to Do
    "360043442453.mdx": ("Getting Started", "Key Resources", None),  # Domo Platform Tour
    "360042922874.mdx": ("Getting Started", "Key Resources", None),  # Getting Help
    "360042922914.mdx": ("Getting Started", "Key Resources", None),  # Standard Domo Support
    "Domo-Video-Library.mdx": ("Getting Started", "Key Resources", None),
    "000005875.mdx": ("Getting Started", "Key Resources", None),   # Domo Glossary (if exists)
    "360043427453.mdx": ("Getting Started", "Key Resources", None), # Domo Glossary
    "000005900.mdx": ("Getting Started", "Key Resources", None),   # Quick reference
    "000005879.mdx": ("Getting Started", "Key Resources", None),
    "360043427193.mdx": ("Getting Started", "Key Resources", None),  # System Requirements
    "000005283.mdx": ("Archive", "Legacy Products", None),  # PopChart — retire
    # Domo Free
    "360043428793.mdx": ("Getting Started", "Domo Free", None),

    # Sandbox → Administer & Govern
    "Create-and-Use-Data-Models.mdx": ("Prepare & Transform Data", "Data Models", None),

    # DomoStats → AI & Data Science
    "360042934594.mdx": ("AI & Data Science", "DomoStats", None),
    "360043433813.mdx": ("AI & Data Science", "DomoStats", None),
    "360043439273.mdx": ("AI & Data Science", "DomoStats", None),
    "360043439293.mdx": ("AI & Data Science", "DomoStats", None),
    "360043439313.mdx": ("AI & Data Science", "DomoStats", None),
    "DomoStats-Overview.mdx": ("AI & Data Science", "DomoStats", None),
    "000005946.mdx": ("AI & Data Science", "DomoStats", None),  # DataSet Fields (DomoStats reference)
    # Goals → Administer & Govern
    "4577172785559.mdx": ("Administer & Govern", "Goals", None),
    "4577793742615.mdx": ("Administer & Govern", "Goals", None),
    "4578049721495.mdx": ("Administer & Govern", "Goals", None),
    "4578278680855.mdx": ("Administer & Govern", "Goals", None),
    "4663374299031.mdx": ("Administer & Govern", "Goals", None),
    # Projects & Tasks → Share & Collaborate
    "360042925914.mdx": ("Share & Collaborate", "Projects & Tasks", None),
    "360042925934.mdx": ("Share & Collaborate", "Projects & Tasks", None),
    "360043430473.mdx": ("Share & Collaborate", "Projects & Tasks", None),
    "360043430493.mdx": ("Share & Collaborate", "Projects & Tasks", None),

    # Access Tokens (Beta, orphaned) → Administer & Govern
    "Access-Tokens.mdx": ("Administer & Govern", "Security & Access", None),
    # FileSets (orphaned) → AI & Data Science
    "000005849.mdx": ("AI & Data Science", "Unstructured Data", None),
    # Slideshows → Share & Collaborate > Publications
    "360042933014.mdx": ("Share & Collaborate", "Publications", None),  # Slideshow Publications Page Layout
    "360043437793.mdx": ("Share & Collaborate", "Publications", None),  # Sharing Content Using Slideshows
    # Worksheets → Analyze & Visualize > Cards
    "Use-Worksheets.mdx": ("Analyze & Visualize", "Cards", None),
    # Goals tutorial
    "4578278680855.mdx": ("Administer & Govern", "Goals", None),

    # ---------------------------------------------------------------------------
    # D9 resolution (2026-07-14): DataSet Management split
    # Governance/lifecycle articles → Manage Data
    # Pipeline/transformation articles stay in Prepare & Transform Data (no override needed)
    # ---------------------------------------------------------------------------

    # Manage Data > Data Center
    "360047553253.mdx": ("Manage Data", "Data Center", None),       # Data Center Layout
    "360043430413.mdx": ("Manage Data", "Data Center", None),       # Using the Data Warehouse to Manage Data
    "360051558694.mdx": ("Manage Data", "Data Center", None),       # Understanding the Connector Options Menu Items

    # Manage Data > DataSet Lifecycle
    "360042926054.mdx": ("Manage Data", "DataSet Lifecycle", None), # Manage Connector/Adapter Accounts
    "360042926074.mdx": ("Manage Data", "DataSet Lifecycle", None), # Change the Owner of a DataSet
    "360042926114.mdx": ("Manage Data", "DataSet Lifecycle", None), # Setting the Expected Update Frequency for a DataSet
    "360042926134.mdx": ("Manage Data", "DataSet Lifecycle", None), # Exporting DataSets
    "360042926154.mdx": ("Manage Data", "DataSet Lifecycle", None), # Best Practices for Managing DataSets
    "360042926194.mdx": ("Manage Data", "DataSet Lifecycle", None), # Deleting DataSets
    "360042926214.mdx": ("Manage Data", "DataSet Lifecycle", None), # Executing DataSets
    "360042926234.mdx": ("Manage Data", "DataSet Lifecycle", None), # Viewing the Impact of Changes to DataSets
    "360042935314.mdx": ("Manage Data", "DataSet Lifecycle", None), # Best Practices for Designing and Structuring Your Domo Instance
    "360042935354.mdx": ("Manage Data", "DataSet Lifecycle", None), # Best Practices for Sharing Content in Domo
    "360043430653.mdx": ("Manage Data", "DataSet Lifecycle", None), # Connecting Cards to a Different DataSet
    "360043430713.mdx": ("Manage Data", "DataSet Lifecycle", None), # Share a DataSet
    "360043435533.mdx": ("Manage Data", "DataSet Lifecycle", None), # Public DataSet Connectors
    "360046074774.mdx": ("Manage Data", "DataSet Lifecycle", None), # Manage DataSet Views
    "360056727214.mdx": ("Manage Data", "DataSet Lifecycle", None), # Non-queryable DataSets
    "4405337525783.mdx": ("Manage Data", "DataSet Lifecycle", None),# Data Fundamentals: Understanding Relational Data...
    "4434784751767.mdx": ("Manage Data", "DataSet Lifecycle", None),# Optimizing Data Performance

    # PDP → Administer & Govern (data-access governance feature)
    "360042934614.mdx": ("Administer & Govern", "Governance", None),# Personalized Data Permissions (PDP)

    # Developer tools → Develop & Integrate
    "360043437693.mdx": ("Develop & Integrate", "APIs & SDKs", None),# Domo ODBC Data Driver
    "360043437733.mdx": ("Develop & Integrate", "APIs & SDKs", None),# Domo CLI (Command Line Interface) Tool

    # Cloud integration migration guide → Connect & Bring In Data
    "000005675.mdx": ("Connect & Bring In Data", "Cloud Data Warehouses", None), # Migrate from Federated to Cloud Integrations

    # Visualization articles → Analyze & Visualize
    "4402058407191.mdx": ("Analyze & Visualize", "Analyzer", None), # Analyzer and DataSet Views Integration
    "360043428693.mdx": ("Analyze & Visualize", "Analyzer", None),  # Understanding Chart Data
}

# ---------------------------------------------------------------------------
# Pillar/group assignment logic
# ---------------------------------------------------------------------------

def assign_pillar(entry: dict) -> tuple[str, str, str | None]:
    """Return (pillar, group, sub_group) for an article."""
    fn = entry["filename"]

    # 1. Hard overrides
    if fn in OVERRIDES:
        return OVERRIDES[fn]

    dtype = entry.get("type", "howto")
    nav = (entry.get("nav_group") or "").lower()
    title = (entry.get("title") or "").lower()
    excerpt = (entry.get("excerpt") or "").lower()

    # 2. Release notes
    if dtype == "release-notes" or "release notes" in nav:
        if "archived" in nav or "archive" in nav:
            return ("Release Notes", "Archived Release Notes", None)
        return ("Release Notes", "Current Release Notes", None)

    # 3. Retire candidates → Archive
    if dtype == "retire-candidate":
        if "workbench 4" in nav or "workbench 4" in title:
            return ("Archive", "Legacy Workbench", None)
        if "legacy" in title or "deprecated" in title or "legacy" in nav:
            return ("Archive", "Deprecated Features", None)
        return ("Archive", "Legacy Content", None)

    # 4. Developer Portal articles
    if "developer portal" in nav or "domo sdk" in nav or "developer topics" in nav:
        return ("Develop & Integrate", "APIs & SDKs", None)

    # 5. Getting Started section
    if "getting started" in nav and "connect" not in nav:
        return ("Getting Started", "Getting Started", None)

    # 6. Connect & Bring In Data
    if "connect & integrate" in nav or "connect" in nav and "integrate" in nav:
        # Cloud data warehouses
        if "cloud data warehouse" in nav:
            dw = _extract_dw_name(nav)
            return ("Connect & Bring In Data", "Cloud Data Warehouses", dw)
        # Workbench
        if "workbench" in nav or "workbench" in title:
            if "workbench 5.1" in title or "workbench 5.1" in nav:
                return ("Connect & Bring In Data", "Workbench", "Workbench 5.1 (Legacy)")
            if "workbench 4" in title or "workbench 4" in nav:
                return ("Archive", "Legacy Workbench", None)
            return ("Connect & Bring In Data", "Workbench", None)
        # Writeback
        if "writeback" in title or "writeback" in nav:
            return ("Connect & Bring In Data", "Writeback Connectors", None)
        # File / JSON connectors
        if "file and json" in nav:
            return ("Connect & Bring In Data", "Connector Library", "Files & APIs")
        # Data provider A-Z
        if "data provider" in nav:
            letter_group = _extract_letter_group(nav)
            return ("Connect & Bring In Data", "Connector Library", letter_group)
        # General connector info
        if "general connector" in nav:
            return ("Connect & Bring In Data", "How Connectors Work", None)
        # Unstructured Data
        if "unstructured" in nav:
            return ("AI & Data Science", "Unstructured Data", None)
        return ("Connect & Bring In Data", "Connector Library", None)

    # 7. Analyze & Visualize — check BEFORE Transform & Manage because
    #    "Card and Dashboard Management" contains "manage"
    if "visualize & interact" in nav or ("visualize" in nav and "interact" in nav):
        if "beast mode" in nav or "beast mode" in title:
            return ("Analyze & Visualize", "Beast Mode", None)
        if "chart" in nav or "chart" in title:
            return ("Analyze & Visualize", "Chart Types", None)
        if "dashboard" in title or "dashboard" in nav or "page filter" in title:
            return ("Analyze & Visualize", "Dashboards & Pages", None)
        if "card" in title or "card" in nav:
            return ("Analyze & Visualize", "Cards", None)
        if "analyzer" in nav or "analyzer" in title:
            return ("Analyze & Visualize", "Analyzer", None)
        return ("Analyze & Visualize", "Analyzer", None)

    # 7b. Prepare & Transform Data (must come after Analyze & Visualize check)
    if "transform & manage" in nav or ("transform" in nav and "manage" in nav and "visualize" not in nav):
        if "magic etl" in nav or "magic etl" in title:
            if "legacy magic etl" in nav or "old magic etl" in title:
                return ("Archive", "Legacy Magic ETL", None)
            return ("Prepare & Transform Data", "Magic ETL", None)
        if "dataflow" in nav or "dataflow" in title or "data flow" in title:
            return ("Prepare & Transform Data", "DataFlows", None)
        if "dataset" in nav or "dataset" in title:
            return ("Prepare & Transform Data", "DataSet Management", None)
        if "workbench" in nav or "workbench" in title:
            return ("Connect & Bring In Data", "Workbench", None)
        if "dashboard" in title or "card" in title or "page" in title:
            return ("Analyze & Visualize", "Dashboards & Pages", None)
        return ("Prepare & Transform Data", "DataSet Management", None)

    # Data models (keyword match regardless of nav)
    if "data model" in title or "data model" in excerpt:
        return ("Prepare & Transform Data", "Data Models", None)

    # 8. Analyze & Visualize fallback (for articles using other nav keywords)
    if "visualize" in nav or "interact" in nav:
        if "beast mode" in nav or "beast mode" in title:
            return ("Analyze & Visualize", "Beast Mode", None)
        if "chart" in nav or "chart" in title:
            return ("Analyze & Visualize", "Chart Types", None)
        if "analyzer" in nav or "analyzer" in title:
            return ("Analyze & Visualize", "Analyzer", None)
        if "dashboard" in nav or "dashboard" in title or "page" in nav:
            return ("Analyze & Visualize", "Dashboards & Pages", None)
        if "card" in title or "card" in nav:
            return ("Analyze & Visualize", "Cards", None)
        return ("Analyze & Visualize", "Analyzer", None)

    # 9. Build Apps & Automate
    if "automate" in nav:
        if "workflow" in title or "workflow" in nav:
            return ("Build Apps & Automate", "Workflows", None)
        if "alert" in title or "alert" in nav:
            return ("Share & Collaborate", "Alerts", None)
        if "form" in title:
            return ("Build Apps & Automate", "Forms", None)
        if "code engine" in title:
            return ("Build Apps & Automate", "Code Engine", None)
        if "task center" in title:
            return ("Build Apps & Automate", "Workflows", None)
        if "scheduled report" in title:
            return ("Share & Collaborate", "Notifications & Reports", None)
        return ("Build Apps & Automate", "Workflows", None)

    # App Studio content (anywhere)
    if "app studio" in title or "app studio" in excerpt or "appstore" in title.replace(" ", ""):
        if "appstore" in title.lower():
            return ("Build Apps & Automate", "Appstore", None)
        return ("Build Apps & Automate", "App Studio", None)

    # 10. Distribute → split between Share & Collaborate and Build Apps
    if "distribute" in nav:
        if "app studio" in title or "app studio" in excerpt:
            return ("Build Apps & Automate", "App Studio", None)
        if "workflow" in title:
            return ("Build Apps & Automate", "Workflows", None)
        if "buzz" in title or "buzz" in nav:
            return ("Share & Collaborate", "Buzz", None)
        if "project" in title or "task" in title:
            return ("Share & Collaborate", "Projects & Tasks", None)
        if "publication" in title or "publication" in nav or "subscriber" in title:
            return ("Share & Collaborate", "Publications", None)
        if "sandbox" in title:
            return ("Administer & Govern", "Sandbox & Environments", None)
        if "export" in title or "embed" in title or "email" in title or "print" in title:
            return ("Share & Collaborate", "Export & Embed", None)
        if "certif" in title:
            return ("Administer & Govern", "Governance", None)
        if "goal" in title:
            return ("Administer & Govern", "Goals", None)
        if "add-in" in title or "add-ins" in title or "office" in title:
            return ("Share & Collaborate", "Domo Add-ins", None)
        if "domo bricks" in title or "domo bricks" in excerpt:
            return ("Build Apps & Automate", "App Studio", None)
        if "wire an app" in title:
            return ("Build Apps & Automate", "App Studio", None)
        if "asset" in title:
            return ("Build Apps & Automate", "Asset Library", None)
        if "appdb" in title:
            return ("Build Apps & Automate", "App Studio", None)
        if "share" in title or "sharing" in title or "access" in title:
            return ("Share & Collaborate", "Sharing", None)
        if "course" in title or "coursebuilder" in title:
            return ("Build Apps & Automate", "CourseBuilder", None)
        return ("Share & Collaborate", "Sharing", None)

    # 11. Admin → Administer & Govern
    if "admin" in nav:
        if "sandbox" in title:
            return ("Administer & Govern", "Sandbox & Environments", None)
        if "security" in title or "sso" in title or "saml" in title or "oauth" in title or "ip address" in title:
            return ("Administer & Govern", "Security & Access", None)
        if "role" in title or "grant" in title or "permission" in title or "user" in title or "license" in title:
            return ("Administer & Govern", "Users & Roles", None)
        if "governance" in title or "certif" in title or "pdp" in title:
            return ("Administer & Govern", "Governance", None)
        if "support" in title or "ticket" in title:
            return ("Administer & Govern", "Support Resources", None)
        return ("Administer & Govern", "Instance Settings", None)

    # DomoStats → AI & Data Science (regardless of current nav placement)
    if "domostat" in title:
        return ("AI & Data Science", "DomoStats", None)

    # Profile / personal settings → Getting Started > Key Resources
    if any(x in title for x in ["Profile Picture", "Profile Background", "Personal Profile",
                                  "Your Profile", "Peers in Your Company", "Online Users"]):
        return ("Getting Started", "Key Resources", None)

    # Notifications / password / personal account → Getting Started > Key Resources
    if any(x in title for x in ["Change Your Password", "Change User Information",
                                  "Receiving and Viewing Notifications", "Managing Your Personal Photos"]):
        return ("Getting Started", "Key Resources", None)

    # 12. AI & Data Science
    if "ai" in nav and "data science" in nav:
        if "jupyter" in title or "jupyter" in nav:
            return ("AI & Data Science", "Jupyter Workspaces", None)
        if "automl" in title or "automl" in nav:
            return ("AI & Data Science", "AutoML", None)
        if "domostat" in title or "domostat" in nav:
            return ("AI & Data Science", "DomoStats", None)
        if "scripting" in title or "scripting" in nav or "python" in title or "r librar" in title:
            return ("AI & Data Science", "Jupyter Workspaces", None)
        if "ai" in title or "ai" in excerpt[:50]:
            return ("AI & Data Science", "Domo AI", None)
        return ("AI & Data Science", "Domo AI", None)

    # 13. General Information (catch-all) — redistribute
    if "general information" in nav:
        # QuickStart apps → Getting Started
        if "quickstart" in title or "quick start" in title:
            return ("Getting Started", "QuickStart Apps", None)
        # CourseBuilder
        if "coursebuilder" in title or "course" in title.lower():
            return ("Build Apps & Automate", "CourseBuilder", None)
        # Premium Apps (named dashboard apps)
        if any(x in title.lower() for x in ["dashboard app", "dashboard | ", "app |", "app guide"]):
            return ("Build Apps & Automate", "Premium Apps", None)
        # Mobile
        if "mobile" in title:
            return ("Getting Started", "Domo Mobile", None)
        # Security
        if "security" in title or "pii" in title or "compliance" in title:
            return ("Administer & Govern", "Security & Access", None)
        # Implementation guides for premium apps
        if "implementation guide" in title or "user guide" in title:
            return ("Build Apps & Automate", "Premium Apps", None)
        # Appstore
        if "appstore" in title.lower() or "app store" in title.lower():
            return ("Build Apps & Automate", "Appstore", None)
        # Domo Free/Freemium
        if "free" in title or "freemium" in title:
            return ("Getting Started", "Domo Free", None)
        # Language settings
        if "language" in title or "translate" in title:
            return ("Administer & Govern", "Instance Settings", None)
        # Instructor-led courses / sample datasets
        if "course" in title or "instructor" in title or "sample dataset" in title or "training" in title:
            return ("Getting Started", "Key Resources", None)
        # Finance app
        if "finance" in title:
            return ("Build Apps & Automate", "Premium Apps", None)
        return ("Build Apps & Automate", "Premium Apps", None)

    # 14. Fallback: try to infer from title/type
    if dtype == "connector":
        return ("Connect & Bring In Data", "Connector Library", None)
    if "alert" in title:
        return ("Share & Collaborate", "Alerts", None)
    if "dashboard" in title or "page" in title:
        return ("Analyze & Visualize", "Dashboards & Pages", None)
    if "card" in title:
        return ("Analyze & Visualize", "Cards", None)
    if "dataset" in title or "data set" in title:
        return ("Prepare & Transform Data", "DataSet Management", None)
    if "user" in title or "role" in title or "admin" in title:
        return ("Administer & Govern", "Instance Settings", None)

    return ("Getting Started", "Key Resources", None)  # final fallback


def _extract_dw_name(nav: str) -> str | None:
    for dw in ["snowflake", "bigquery", "databricks", "redshift", "athena", "azure",
               "postgresql", "mysql", "oracle", "sap hana", "dremio"]:
        if dw in nav:
            return dw.title()
    return None


def _extract_letter_group(nav: str) -> str | None:
    m = re.search(r'data providers? ([a-z\-# ]+)', nav.lower())
    if m:
        return f"Data Providers {m.group(1).strip().upper()}"
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with open(CATALOG) as f:
        catalog = json.load(f)

    mapping = {}  # filename → {pillar, group, sub_group}
    spec = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    # spec[pillar][group][sub_group or "_"] → list of articles

    for entry in catalog:
        pillar, group, sub_group = assign_pillar(entry)
        sub = sub_group or "_"
        spec[pillar][group][sub].append({
            "filename": entry["filename"],
            "title": entry["title"],
            "type": entry["type"],
            "id_scheme": entry["id_scheme"],
        })
        mapping[entry["filename"]] = {
            "pillar": pillar,
            "group": group,
            "sub_group": sub_group,
        }

    # Write mapping
    with open("scripts/output/ia-mapping.json", "w") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    # Convert spec to serializable dict
    spec_out = {}
    for pillar, groups in sorted(spec.items()):
        spec_out[pillar] = {}
        for group, subs in sorted(groups.items()):
            spec_out[pillar][group] = {}
            for sub, articles in sorted(subs.items()):
                articles.sort(key=lambda a: (
                    {"tutorial": 0, "explanation": 1, "howto": 2, "reference": 3,
                     "connector": 4, "release-notes": 5, "retire-candidate": 6}.get(a["type"], 9)
                ))
                spec_out[pillar][group][sub] = articles

    with open("scripts/output/ia-spec.json", "w") as f:
        json.dump(spec_out, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n=== IA Spec Summary ===\n")
    total_assigned = 0
    for pillar, groups in sorted(spec_out.items()):
        pillar_count = sum(
            len(articles)
            for subs in groups.values()
            for articles in subs.values()
        )
        total_assigned += pillar_count
        print(f"{pillar} ({pillar_count})")
        for group, subs in sorted(groups.items()):
            group_count = sum(len(a) for a in subs.values())
            has_subs = list(subs.keys()) != ["_"]
            if has_subs:
                print(f"  └─ {group} ({group_count})")
                for sub, articles in sorted(subs.items()):
                    if sub != "_":
                        print(f"     └─ {sub}: {len(articles)}")
            else:
                print(f"  └─ {group}: {group_count}")
        print()

    print(f"Total articles assigned: {total_assigned} / {len(catalog)}")


if __name__ == "__main__":
    main()
