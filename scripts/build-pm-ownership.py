#!/usr/bin/env python3
"""
Build Article-PM-Ownership-Reference.mdx

Matches every article in s/article/ to a Feature (and PM) from the CSV.
Strategy (priority order):
  1. Exact or rule-based match by nav group hierarchy
  2. Title/excerpt keyword match
  3. Fallback to broad nav section defaults
"""

import json
import os
import re
import csv
import datetime
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── 1. Parse CSV ──────────────────────────────────────────────────────────────
# Prefer the row with a PM when a feature appears more than once.
features = {}  # feature_name → {pm, squad_biz}
with open(ROOT / 'Feature - Owning Squad, PM, Eng, UX.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        feat = row['Feature'].strip()
        pm = row['PM'].strip()
        squad_biz = row['Squad Business Name'].strip()
        if feat not in features or (pm and not features[feat]['pm']):
            features[feat] = {'pm': pm, 'squad_biz': squad_biz}

# ── 2. Build nav hierarchy: slug → [immediate_group, parent, grandparent, …, tab] ──
article_nav = {}  # slug → list of ancestor group names (most specific first)

def traverse(pages, ancestors):
    for item in pages:
        if isinstance(item, str):
            slug = item.replace('s/article/', '')
            if slug not in article_nav:
                article_nav[slug] = ancestors[:]
        elif isinstance(item, dict) and 'group' in item:
            traverse(item.get('pages', []), [item['group']] + ancestors)

with open(ROOT / 'docs.json', encoding='utf-8') as f:
    docs = json.load(f)

nav = docs['navigation']['languages'][0]  # 'en'
for tab in nav['tabs']:
    if 'pages' in tab:
        traverse(tab['pages'], [tab.get('tab', '')])

# ── 3. Nav-group → Feature mapping (most specific wins) ───────────────────────
# Keys are nav group names; values are Feature names from CSV.
NAV_FEATURE = {
    # ── Workbench ─────────────────────────────────────────────────────────────
    'Workbench Enterprise': 'Workbench',
    'Workbench 5':           'Workbench',
    'Workbench 4':           'Workbench',
    'On-premises Systems':   'Workbench',
    'ODBC Driver':           'ODBC Driver',

    # ── Cloud Data Warehouses (parent group with 3 overview articles) ─────────
    'Cloud Data Warehouses': 'Cloud Amplifier',
    'Connect Data':          'Cloud Amplifier',

    # ── All third-party connector provider groups ─────────────────────────────
    'Adobe':       'Third Party Connectors',
    'Amazon':      'Third Party Connectors',
    'Anaplan':     'Third Party Connectors',
    'Apache':      'Third Party Connectors',
    'Apple':       'Third Party Connectors',
    'BambooHR':    'Third Party Connectors',
    'Box':         'Third Party Connectors',
    'Cvent':       'Third Party Connectors',
    'Domo':        'Third Party Connectors',   # 'Domo' connector group
    'Dropbox':     'Third Party Connectors',
    'Facebook':    'Third Party Connectors',
    'GitHub':      'Third Party Connectors',
    'Google':      'Third Party Connectors',
    'HubSpot':     'Third Party Connectors',
    'IBM':         'Third Party Connectors',
    'JIRA':        'Third Party Connectors',
    'Kintone':     'Third Party Connectors',
    'LinkedIn':    'Third Party Connectors',
    'Lithium':     'Third Party Connectors',
    'Magento':     'Third Party Connectors',
    'Marketo':     'Third Party Connectors',
    'Microsoft':   'Third Party Connectors',
    'MongoDB':     'Third Party Connectors',
    'NetSuite':    'Third Party Connectors',
    'New Relic':   'Third Party Connectors',
    'Quandl':      'Third Party Connectors',
    'QuickBooks':  'Third Party Connectors',
    'Sage Intacct':'Third Party Connectors',
    'Salesforce':  'Third Party Connectors',
    'SAP':         'Third Party Connectors',
    'ServiceNow':  'Third Party Connectors',
    'Shopify':     'Third Party Connectors',
    'Sprinklr':    'Third Party Connectors',
    'Square':      'Third Party Connectors',
    'Sysomos':     'Third Party Connectors',
    'TikTok':      'Third Party Connectors',
    'USGS':        'Third Party Connectors',
    'Vertica':     'Third Party Connectors',   # connector group (not DB infra)
    'Workday':     'Third Party Connectors',
    'Workfront':   'Third Party Connectors',
    'Xero':        'Third Party Connectors',
    'YouTube':     'Third Party Connectors',
    'Zendesk':     'Third Party Connectors',
    'Zoom':        'Third Party Connectors',
    'Data Providers A-B':     'Third Party Connectors',
    'Data Providers C-F':     'Third Party Connectors',
    'Data Providers G-K':     'Third Party Connectors',
    'Data Providers L-P':     'Third Party Connectors',
    'Data Providers Q-S':     'Third Party Connectors',
    'Data Providers T-Z and #':'Third Party Connectors',
    'File and JSON Connectors':'Third Party Connectors',
    'General Connector Information': 'Connectors 1.0',

    # ── Transform & Manage ────────────────────────────────────────────────────
    'Magic ETL':              'Magic ETL',
    'Tiles':                  'Magic ETL',
    'Magic ETL on Snowflake': 'Magic ETL',
    'Magic ETL on Databricks':'Magic ETL',
    'Legacy Magic ETL':       'Magic ETL',
    'SQL DataFlows':          'Data Flows',
    'DataFlow Management':    'Data Flows',
    'Transform Data in Domo': 'Data Flows',   # fallback for the parent section
    'DataFusion':             'Fusions',
    'DataSet Views':          'Data Views',
    'Enterprise Stacker':     'Combined Schema',
    'Data Center Overview':   'Data Center',
    'Manage Data in Domo':    'Data Center',

    # ── Visualize & Interact ──────────────────────────────────────────────────
    'Analyzer':                           'Analyzer',
    'Build Visualization Cards in Analyzer': 'Analyzer',
    'Powering Your Card':                 'DataSets',
    'Beast Mode':                         'Beast Mode',
    'Area and Bar Charts':                'Charting',
    'Data Science Charts':                'Charting',
    'Filter and Miscellaneous Charts':    'Charting',
    'Gauges':                             'Charting',
    'Line and Lollipop Charts':           'Charting',
    'Period-over-Period Charts':          'Period over Period',
    'Pie and Funnel charts':              'Charting',
    'Tables':                             'Charting',
    'Textboxes and Map Charts':           'Charting',
    'Chart Properties':                   'Charting',
    'Chart Types for Visualization Cards':'Charting',
    'Visualization Card Details View Actions': 'Charting',
    'Card and Dashboard Management':      'Charting',
    'Other Card Types (Doc, Notebook, and Sumo Cards)': 'Doc Cards',
    'Worksheets':                         'Worksheets',
    'Slideshow Publications':             'Slideshows',
    'Visualize & Interact':               'Charting',

    # ── AI & Data Science ─────────────────────────────────────────────────────
    'AI Library':          'AI Services',
    'AI Resources Guide':  'AI Services',
    'Unstructured Data':   'Documents-Filesets',
    'Jupyter Workspaces':  'Jupyter Notebooks',
    'Machine Learning':    'Auto ML',
    'AI & Data Science':   'AI Services',

    # ── Automate ──────────────────────────────────────────────────────────────
    'Workflows':           'Workflows',
    'Alerts':              'Alerts, NLG, Smart Alerts/Insights',
    'Automate':            'Workflows',
    'Automate Actions':    'Workflows',

    # ── Distribute ────────────────────────────────────────────────────────────
    'Export Content':           'Export to CSV',     # generic export parent
    'Domo Everywhere':          'Domo Everywhere',
    'Embed Domo Everywhere':    'Domo Everywhere',
    'Domo Sandbox':             'Sandbox',
    'Microsoft Office Add-Ins': 'MS Office Plugins / Addins',
    'Plugins for Sharing Domo Content': 'MS Office Plugins / Addins',
    'Publication Groups':       'Publication Groups',
    'App Studio':               'App Studio',
    'Domo Bricks':              'Bricks/Templates',
    'Apps':                     'App Studio',
    'Approvals':                'Approvals',
    'Projects and Tasks':       'Projects & Tasks',
    'Goals Center':             'Goals',
    'Buzz':                     'Buzz',
    'Collaborate in Domo':      'Buzz',
    'Distribute Domo Content':  'Domo Everywhere',

    # ── Admin ─────────────────────────────────────────────────────────────────
    'Access Management':         'Attribute Based Access Control (ABAC)',
    'Roles':                     'Admin',
    'Toolkit':                   'Governance Toolkit',
    'Users and Groups':          'Admin',
    'Security':                  'Application Security',
    'SSO':                       'Single Sign-On',
    'DomoStats':                 'DomoStats',
    'Governance':                'Governance Toolkit',
    'Credit Consumption':        'Consumption',
    'Govern Your Domo Instance': 'Governance Toolkit',
    'Administrate Domo':         'Admin',

    # ── General Information ───────────────────────────────────────────────────
    'Domo Mobile':               'Mobile - iOS',
    'AppStore':                  'AppStore',
    'Use the Appstore':          'AppStore',
    'Publish on the Appstore':   'AppStore',
    'Available Apps':            'AppStore',
    'QuickStart Apps':           'AppStore',
    'Localization and Accessibility': 'Accessibility',
    'Education':                 'Education',
    'CourseBuilder 1.4':         'Education',
    'Domo Free':                 'Freemium',
    'User Profile':              'Profile',
    'User Settings':             'Profile',
    'Support Resources':         'Admin',
    'Getting Started':           'Onboarding',
    'General Information':       'Admin',  # default fallback for this section

    # ── Developer Portal ─────────────────────────────────────────────────────
    'API Reference':             'CLI',        # Dev portal → Data Core/CLI area
    'Build Apps':                'App Dev Framework',
    'Developer Topics':          'App Dev Framework',
    'Partner Developers':        'App Dev Framework',
    'Domo SDK':                  'App Dev Framework',
    'Other Resources':           'App Dev Framework',

    # ── Release Notes ────────────────────────────────────────────────────────
    'Archived Feature Release Notes': 'Release Management',
    'Release Notes':             'Release Management',
}

# ── 4. Title/excerpt keyword rules (for cloud provider groups and edge cases) ──
# Applied when the immediate nav group is one of the cloud-provider warehouse groups.
CLOUD_WAREHOUSE_GROUPS = {
    'Snowflake', 'Google BigQuery', 'Databricks',
    'Amazon (Redshift, Athena)', 'Dremio', 'Lakebase',
    'Microsoft Azure', 'MySQL', 'Oracle', 'PostgreSQL',
}

def classify_cloud_warehouse_article(title_lower, excerpt_lower):
    """Return Feature name for articles in cloud-warehouse nav groups."""
    # Connector keyword → Connectors 1.0
    if re.search(r'\bconnector\b', title_lower):
        return 'Connectors 1.0'
    if 'federated' in title_lower or 'federated' in excerpt_lower:
        return 'Federated'
    if 'cloud amplifier' in title_lower or 'cloud amplifier' in excerpt_lower:
        return 'Cloud Amplifier'
    if re.search(r'\bdomo on\b', title_lower):
        return 'Cloud Amplifier'
    if 'writeback' in title_lower:
        return 'Connectors 1.0'
    if 'minimum permissions' in title_lower:
        return 'Connectors 1.0'
    # Default: Cloud Amplifier (integration setup articles)
    return 'Cloud Amplifier'

# Keyword patterns for articles not matched by nav (title/excerpt scan)
# Ordered: more specific patterns first to prevent false positives.
KEYWORD_RULES = [
    (r'documents.filesets?|fileset', 'Documents-Filesets'),
    (r'unstructured data',   'Documents-Filesets'),
    (r'workbench',           'Workbench'),
    (r'magic etl',           'Magic ETL'),
    (r'dataflow|data flow',  'Data Flows'),
    (r'datafusion|data fusion', 'Fusions'),
    (r'beast mode',          'Beast Mode'),
    (r'analyzer',            'Analyzer'),
    (r'jupyter',             'Jupyter Notebooks'),
    (r'notebook',            'Jupyter Notebooks'),
    (r'sandbox',             'Sandbox'),
    (r'domo everywhere',     'Domo Everywhere'),
    (r'publication group',   'Publication Groups'),
    (r'app studio',          'App Studio'),
    (r'code engine',         'Code Engine'),
    (r'workflow',            'Workflows'),
    (r'\balerts?\b',         'Alerts, NLG, Smart Alerts/Insights'),
    (r'smart alert',         'Alerts, NLG, Smart Alerts/Insights'),
    (r'domo stats|domostats','DomoStats'),
    (r'governance toolkit',  'Governance Toolkit'),
    (r'single sign.on|sso',  'Single Sign-On'),
    (r'data center',        'Data Center'),
    (r'data science',       'Data Science'),
    (r'auto ml|automl',     'Auto ML'),
    (r'ai chat',            'AI Chat'),
    (r'custom assistant',   'Custom Assistants'),
    (r'app catalyst',       'App Catalyst'),
    (r'model management',   'Model Management'),
    (r'ai dictionar',       'AI Dictionaries'),
    (r'ai readiness',       'AI Readiness'),
    (r'buzz',               'Buzz'),
    (r'projects? and tasks?|projects? & tasks?', 'Projects & Tasks'),
    (r'\bgoals?\b',         'Goals'),
    (r'\bapprovals?\b',     'Approvals'),
    (r'mobile',             'Mobile - iOS'),
    (r'appstore|app store', 'AppStore'),
    (r'domo free|freemium', 'Freemium'),
    (r'brand kit',          'Brand Kit'),
    (r'chameleon',          'Chameleon'),
    (r'consumption|credits?', 'Consumption'),
    (r'pdp|personalized data permission', 'PDP'),
    (r'scim',               'SCIM'),
    (r'oauth|sso|saml',     'Single Sign-On'),
    (r'variable',           'Variables'),
    (r'export to pdf|export to powerpoint|export to excel|export to email|export to csv', 'Export to CSV'),
    (r'scheduled report',   'Scheduled Reports'),
    (r'slideshow',          'Slideshows'),
    (r'period.over.period', 'Period over Period'),
    (r'data view',          'Data Views'),
    (r'dataset view',       'Data Views'),
    (r'datafusion',         'Fusions'),
    (r'combined schema',    'Combined Schema'),
    (r'enterprise stacker', 'Combined Schema'),
    (r'sumo',               'Sumo'),
    (r'doc card',           'Doc Cards'),
    (r'notebook card',      'Notebook Cards'),
    (r'webform',            'Webform'),
    (r'\bforms?\b',          'Forms'),
    (r'annotation',         'Snaphsot Annotations'),
    (r'connector ide',      'Connector IDE'),
    (r'custom connector',   'Custom Connector IDE'),
    (r'odbc',               'ODBC Driver'),
    (r'adrenaline',         'Adrenaline'),
    (r'fiscal calendar',    'Fiscal Calendars'),
    (r'upsert',             'Upsert'),
    (r'vault',              'Vault'),
    (r'dql',                'DQL'),
    (r'webhook',            'Webhooks'),
    (r'data account',       'Data Accounts'),
    (r'access token',       'CLI'),
    (r'\bcli\b',            'CLI'),
    (r'federated',          'Federated'),
    (r'cloud amplifier',    'Cloud Amplifier'),
    (r'google suite|google workspace add.in', 'Google Suite Addins'),
    (r'ms office|microsoft office|excel add.in|powerpoint add.in', 'MS Office Plugins / Addins'),
    (r'inline edit',        'Inline Editing'),
    (r'card filter',        'Card Filters'),
    (r'quick filter',       'Card Quick Filters'),
    (r'save as',            'Card Save as'),
    (r'sharing|share',      'Cards Sharing'),
    (r'drill',              'Drill'),
    (r'color rule',         'Color Rules'),
    (r'drill path',         'Drill'),
    (r'date annotation',    'Date Annotations'),
    (r'card lineage|data lineage', 'Card Data Lineage'),
    (r'certified content',  'Certified Content'),
    (r'publication group',  'Publication Groups'),
    (r'publish',            'Publish'),
    (r'embed',              'Embed (Stories)'),
    (r'activity log',       'Activity Log'),
    (r'left navigation|navigation',  'Navigation'),
    (r'profile',            'Profile'),
    (r'user email|invite',  'User emails and invites'),
    (r'notification',       'Notifications'),
    (r'search',             'Search'),
    (r'social',             'Social'),
    (r'teams integration|microsoft teams', 'Teams integration'),
    (r'workspac',           'Workspaces'),
    (r'customer communi',   'Customer Communications Center'),
    (r'mr roboto',          'Mr Roboto'),
    (r'discoverabilit',     'Discoverabliity'),
    (r'daily domo|domo home', 'Daily Domo Page (Domo Home)'),
    (r'collections?',       'Collections'),
    (r'page filter',        'Page Filters'),
    (r'stories?\s+\(|page layout', 'Stories (Page Layouts)'),
    (r'bricks?',            'Bricks/Templates'),
    (r'identity',           'Identity'),
    (r'license',            'Licenses'),
    (r'attribute.based|abac', 'Attribute Based Access Control (ABAC)'),
    (r'access management|role',  'Admin'),
    (r'admin',              'Admin'),
    (r'domo\.ai',           'Domo.AI'),
    (r'data model',         'Data Models'),
    (r'domo data experience|ddx', 'Domo Data Experiences (DDX)'),
    (r'slide show presentation', 'Slide Show Presentation'),
    (r'worksheet',          'Worksheets'),
    (r'java|python script|r script', 'Data Science'),
    (r'python',             'Python'),
    (r'sql',                'Data Flows'),
    (r'domo connector',     'Connectors 1.0'),
    (r'connector',          'Third Party Connectors'),
    (r'app dev framework',  'App Dev Framework'),
    (r'app data structure', 'App Data Structures'),
    (r'asset library',      'Asset Library'),
    (r'locali[sz]ation|internationali[sz]ation', 'Internationalization'),
    (r'accessibility',      'Accessibility'),
    (r'sandbox',            'Sandbox'),
    (r'orchestration',      'Orchestration'),
    (r'global identity',    'Global Identity'),
    (r'education|coursebuilder', 'Education'),
    (r'app store|appstore', 'AppStore'),
]

# ── 5. Frontmatter extractor ───────────────────────────────────────────────────
_FM_RE = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
_TITLE_RE = re.compile(r'^title:\s*(?:"([^"]+)"|\'([^\']+)\'|(.*?))\s*$', re.MULTILINE)
_EXCERPT_RE = re.compile(r'^excerpt:\s*(?:"([^"]+)"|\'([^\']+)\'|(.*?))\s*$', re.MULTILINE)

def read_frontmatter(path):
    try:
        with open(path, encoding='utf-8') as f:
            text = f.read(4096)
        fm = _FM_RE.match(text)
        if not fm:
            return '', ''
        body = fm.group(1)
        tm = _TITLE_RE.search(body)
        title = (tm.group(1) or tm.group(2) or tm.group(3) or '').strip() if tm else ''
        em = _EXCERPT_RE.search(body)
        excerpt = (em.group(1) or em.group(2) or em.group(3) or '').strip() if em else ''
        return title, excerpt
    except Exception:
        return '', ''

# ── 6. Assign feature to each article ─────────────────────────────────────────
def assign_feature(slug, title, excerpt):
    groups = article_nav.get(slug, [])
    tl = title.lower()
    el = excerpt.lower()

    # Check if this is in a cloud warehouse provider subgroup
    if groups and groups[0] in CLOUD_WAREHOUSE_GROUPS:
        return classify_cloud_warehouse_article(tl, el)

    # Walk nav groups most-specific first
    for grp in groups:
        if grp in NAV_FEATURE:
            return NAV_FEATURE[grp]

    # Title/excerpt keyword scan
    combined = tl + ' ' + el
    for pattern, feat in KEYWORD_RULES:
        if re.search(pattern, combined):
            return feat

    # Last resort: broad tab fallback
    if groups:
        tab = groups[-1]
        if tab == 'Connect & Integrate':
            return 'Third Party Connectors'
        if tab in ('Transform & Manage',):
            return 'Data Flows'
        if tab in ('Visualize & Interact',):
            return 'Charting'
        if tab in ('API Reference', 'Build Apps', 'Developer Topics',
                   'Partner Developers', 'Domo SDK', 'Other Resources'):
            return 'App Dev Framework'
        if tab in ('Admin',):
            return 'Admin'
        if tab in ('General Information',):
            return 'Admin'

    return 'Admin'  # absolute last resort

# ── 7. Process all articles ────────────────────────────────────────────────────
article_dir = ROOT / 's' / 'article'
rows = []

for fname in sorted(os.listdir(article_dir)):
    if not fname.endswith('.mdx'):
        continue
    slug = fname[:-4]
    path = article_dir / fname
    title, excerpt = read_frontmatter(path)
    feature = assign_feature(slug, title, excerpt)
    pm = features.get(feature, {}).get('pm', '(no PM listed)')
    rows.append({
        'feature': feature,
        'title':   title or slug,
        'filename': fname,
        'pm':      pm or '(no PM listed)',
    })

# ── 8. Print stats ─────────────────────────────────────────────────────────────
from collections import Counter
feat_count = Counter(r['feature'] for r in rows)
print(f"Total articles: {len(rows)}")
print(f"Distinct features used: {len(feat_count)}")
print(f"Features assigned that are NOT in CSV:")
for feat, cnt in feat_count.most_common():
    if feat not in features:
        print(f"  {cnt:4d}  '{feat}'")
print()
print(f"Top 20 feature assignments:")
for feat, cnt in feat_count.most_common(20):
    pm = features.get(feat, {}).get('pm', '???')
    print(f"  {cnt:4d}  {feat}  [{pm}]")

# ── 9. Write MDX ───────────────────────────────────────────────────────────────
# Sort: by feature (Product Group), then by title within each group
rows_sorted = sorted(rows, key=lambda r: (r['feature'].lower(), r['title'].lower()))

today = datetime.date.today().isoformat()
out_path = ROOT / 'Article-PM-Ownership-Reference.mdx'

def esc(s):
    """Escape pipe chars so they don't break Markdown table cells."""
    return s.replace('|', '\\|')

lines = [
    '---',
    'title: "Article PM Ownership Reference"',
    'excerpt: "Maps every KB article in s/article/ to its owning Feature and Product Manager, cross-referenced from the internal squad ownership CSV."',
    '---',
    '',
    'This reference maps every article in `s/article/` to its owning **Feature** (using the same nomenclature as the internal squad-ownership CSV) and the associated **Product Manager**.',
    '',
    '> **How to use:** Search this page (Ctrl/Cmd+F) for a feature name, article title, or PM name to quickly find ownership. '
    'The Feature column matches the "Feature" column in the *Feature – Owning Squad, PM, Eng, UX* CSV at the repo root.',
    '',
    f'_Last generated: {today} · {len(rows)} articles_',
    '',
    '| Feature | Article Title | Article File Name | PM |',
    '|---|---|---|---|',
]

for r in rows_sorted:
    lines.append(
        f"| {esc(r['feature'])} | {esc(r['title'])} | `{r['filename']}` | {esc(r['pm'])} |"
    )

lines.append('')

# ── 10. Pad table columns so all pipes align ────────────────────────────────
# Cells may contain \| (escaped pipe, renders as |); treat \| as 1 display
# char when measuring widths so columns align as they appear on screen.

_PLACEHOLDER = '\x01'

def _split_cells(line: str) -> list[str]:
    """Split a pipe-table row into cells, treating \\| as a single unit."""
    escaped = line.replace('\\|', _PLACEHOLDER)
    inner = escaped.strip().lstrip('|').rstrip('|')
    return [c.strip().replace(_PLACEHOLDER, '\\|') for c in inner.split('|')]

def _disp(cell: str) -> int:
    """Display width of a cell (\\| counts as 1, not 2)."""
    return len(cell.replace('\\|', '|'))

def pad_table(lines: list[str]) -> list[str]:
    """Pad every data/header row so column pipes align."""
    # Identify table rows (non-separator pipe rows)
    table_idxs = []
    for i, line in enumerate(lines):
        if line.startswith('| ') and not line.startswith('|---'):
            cells = _split_cells(line)
            if len(cells) == 4:
                table_idxs.append(i)

    # Compute max RAW length per column (raw alignment = pipes line up in a text editor)
    # Cells with \\| are 1 raw char longer than their display width, so we pad by raw length
    # to keep all row lengths equal. The rendered display difference is imperceptible (1 char).
    col_widths = [0, 0, 0, 0]
    for i in table_idxs:
        for j, cell in enumerate(_split_cells(lines[i])):
            col_widths[j] = max(col_widths[j], len(cell))  # raw length, not display width

    # Rebuild
    result = []
    for i, line in enumerate(lines):
        if i in set(table_idxs):
            cells = _split_cells(line)
            padded = [cell + ' ' * (col_widths[j] - len(cell))
                      for j, cell in enumerate(cells)]
            result.append('| ' + ' | '.join(padded) + ' |')
        elif line.startswith('|---'):
            # Separator: dash-pad each column to match its max width
            result.append('| ' + ' | '.join('-' * w for w in col_widths) + ' |')
        else:
            result.append(line)
    return result

lines = pad_table(lines)

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"\nWrote {out_path} ({len(rows)} rows, columns padded)")
