from pathlib import Path
import re, html
p = Path('s/article/000005353.mdx')
text = p.read_text(encoding='utf-8')
m = re.search(r'<table.*?</table>', text, re.S)
if not m:
    raise SystemExit('TABLE NOT FOUND')
table = m.group(0)
rows = []
for tr in re.findall(r'<tr.*?>(.*?)</tr>', table, re.S):
    row = []
    for cell in re.findall(r'<t[dh].*?>(.*?)</t[dh]>', tr, re.S):
        cleaned = re.sub(r'<.*?>', '', cell)
        cleaned = html.unescape(cleaned).strip()
        row.append(' '.join(cleaned.split()))
    if row:
        rows.append(row)
if not rows:
    raise SystemExit('NO ROWS')
widths = [max(len(row[i]) if i < len(row) else 0 for row in rows) for i in range(max(len(row) for row in rows))]
md = []
for idx, row in enumerate(rows):
    padded = [' ' + (row[i] if i < len(row) else '').ljust(widths[i]) + ' ' for i in range(len(widths))]
    md.append('|' + '|'.join(padded) + '|')
    if idx == 0:
        sep = [' ' + '-' * widths[i] + ' ' for i in range(len(widths))]
        md.append('|' + '|'.join(sep) + '|')
print('\n'.join(md))
