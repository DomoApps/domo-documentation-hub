import os, re, json, glob

ART = glob.glob('s/article/*.mdx')

def parse(path):
    with open(path, encoding='utf-8') as fh:
        txt = fh.read()
    fm = {}
    body = txt
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r'^(\w+):\s*(.*)$', line)
            if mm:
                fm[mm.group(1)] = mm.group(2).strip().strip('"')
        body = m.group(2)
    return fm, body

rows = []
for p in sorted(ART):
    fm, body = parse(p)
    title = fm.get('title', '')
    excerpt = fm.get('excerpt', '')
    status = fm.get('status', '')
    # First heading in body
    headings = re.findall(r'^(#{2,3})\s+(.*)$', body, re.M)
    first_h = headings[0][1].strip() if headings else ''
    has_intro_heading = bool(re.search(r'^##\s+Intro\b', body, re.M))
    # Does the body start with a paragraph before any heading? (intro-without-heading)
    pre_heading = body
    if headings:
        idx = body.find('## ' + headings[0][1]) if headings else -1
    starts_with_this_article = bool(re.match(r'\s*(##\s+Intro\s*\n+)?\s*This article\b', body))
    # Categorize
    low = title.lower()
    is_connector = ('connector' in low) or bool(re.search(r'connect to ', low))
    is_release = 'release' in low and 'note' in low
    rows.append({
        'file': os.path.basename(p),
        'title': title,
        'status': status,
        'has_excerpt': bool(excerpt),
        'has_intro_heading': has_intro_heading,
        'first_heading': first_h,
        'is_connector': is_connector,
        'is_release': is_release,
    })

missing = [r for r in rows if not r['has_intro_heading']]
print(f"TOTAL articles: {len(rows)}")
print(f"Missing '## Intro' heading: {len(missing)}")
print()
conn = [r for r in missing if r['is_connector']]
rel  = [r for r in missing if r['is_release'] and not r['is_connector']]
other = [r for r in missing if not r['is_connector'] and not r['is_release']]
print(f"  of which connector-library articles: {len(conn)}")
print(f"  of which release-notes articles:     {len(rel)}")
print(f"  of which OTHER (candidate for sweep): {len(other)}")
print(f"     - with excerpt (intro derivable): {sum(1 for r in other if r['has_excerpt'])}")
print(f"     - without excerpt:                {sum(1 for r in other if not r['has_excerpt'])}")
print(f"     - status set (non-active):        {sorted(set(r['status'] for r in other if r['status'] and r['status']!='active'))}")
print()
print("=== First-heading distribution among OTHER (what they currently open with) ===")
from collections import Counter
c = Counter(r['first_heading'] for r in other)
for h, n in c.most_common(25):
    print(f"  {n:4d}  {h[:70]!r}")

# Save the OTHER worklist
with open('scripts/reports/intro_gap_worklist.json', 'w') as fh:
    json.dump(other, fh, indent=2)
print(f"\nWrote {len(other)} candidate rows to scripts/reports/intro_gap_worklist.json")
