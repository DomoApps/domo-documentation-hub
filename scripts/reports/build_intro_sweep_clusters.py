import json, re, os, glob

buckets = json.load(open('scripts/reports/intro_gap_buckets.json'))
sweep_files = buckets['has_para'] + buckets['opens_heading'] + buckets['opens_component']
bucket_of = {}
for b in ('has_para', 'opens_heading', 'opens_component'):
    for f in buckets[b]:
        bucket_of[f] = b

def parse_fm(path):
    txt = open(path, encoding='utf-8').read()
    fm = {}
    m = re.match(r'^---\n(.*?)\n---', txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r'^(\w+):\s*(.*)$', line)
            if mm:
                fm[mm.group(1)] = mm.group(2).strip().strip('"')
    return fm

# PM lookup from ownership reference rows: | Feature | Title | `file.mdx` | PM |
pm_map = {}
for line in open('Article-PM-Ownership-Reference.mdx', encoding='utf-8'):
    m = re.search(r'`([0-9A-Za-z\-]+\.mdx)`\s*\|\s*([^|]+?)\s*\|', line)
    if m:
        pm_map[m.group(1)] = m.group(2).strip()

rows = []
for f in sweep_files:
    fm = parse_fm(f's/article/{f}')
    rows.append({'file': f, 'title': fm.get('title', ''), 'excerpt': fm.get('excerpt', ''),
                 'bucket': bucket_of[f], 'pm': pm_map.get(f, '(unknown - grep ownership ref)')})
rows.sort(key=lambda r: r['file'])

CS = 7
clusters = [rows[i:i+CS] for i in range(0, len(rows), CS)]
os.makedirs('scripts/reports/intro_sweep_clusters', exist_ok=True)
for old in glob.glob('scripts/reports/intro_sweep_clusters/cluster_*.md'):
    os.remove(old)
for i, cl in enumerate(clusters, 1):
    with open(f'scripts/reports/intro_sweep_clusters/cluster_{i:02d}.md', 'w') as fh:
        fh.write(f'# Intro Sweep Cluster {i:02d} ({len(cl)} articles)\n\n')
        for r in cl:
            fh.write(f"## s/article/{r['file']}\n")
            fh.write(f"- **Title:** {r['title']}\n")
            fh.write(f"- **Excerpt:** {r['excerpt']}\n")
            fh.write(f"- **Bucket:** {r['bucket']}\n")
            fh.write(f"- **Owning PM (for grant-gap [pm-input]):** {r['pm']}\n\n")

print(f"Sweep target: {len(rows)} articles -> {len(clusters)} clusters of <={CS}")
from collections import Counter
print("By bucket:", dict(Counter(r['bucket'] for r in rows)))
known = sum(1 for r in rows if not r['pm'].startswith('(unknown'))
print(f"PM coverage: known={known} unknown={len(rows)-known}")
json.dump(rows, open('scripts/reports/intro_sweep_worklist.json', 'w'), indent=2)
