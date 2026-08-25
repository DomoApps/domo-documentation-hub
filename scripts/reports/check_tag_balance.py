import subprocess, re

files = subprocess.check_output(
    ["git", "diff", "--name-only", "s/article/"]).decode().split()
tags = ["Note", "Warning", "Tip", "Accordion", "AccordionGroup", "Frame"]
bad = 0
for f in files:
    t = open(f).read()
    for tag in tags:
        opens = len(re.findall(r"<" + tag + r"(?:\s[^>]*?)?>", t))   # <Tag> or <Tag ...>
        selfc = len(re.findall(r"<" + tag + r"(?:\s[^>]*?)?/>", t))  # <Tag ... />
        closes = len(re.findall(r"</" + tag + r">", t))
        if opens != closes:
            print(f"  MISMATCH {f}  <{tag}> open(non-self)={opens} close={closes} selfclosed={selfc}")
            bad += 1
print("MISMATCHES:", bad, "(0 = all balanced)")
print("files checked:", len(files))
