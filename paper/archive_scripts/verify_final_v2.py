import re, os
p = r"F:\三线建设\paper\logs\xelatex_run3.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

err_count = len(re.findall(r'^! ', s, re.MULTILINE))
print(f"Errors: {err_count}")
print(f"Undefined: {s.count('undefined')}")

out = re.search(r'Output written on (\S+) \((\d+) pages', s)
if out:
    print(f"Output: {out.group(1)} ({out.group(2)} pages)")

pdf = r"F:\三线建设\paper\main.pdf"
if os.path.exists(pdf):
    print(f"main.pdf: {os.path.getsize(pdf):,} bytes")

# bibtex 状态
bp = r"F:\三线建设\paper\logs\bibtex_run.log"
if os.path.exists(bp):
    with open(bp, 'r', encoding='utf-8', errors='replace') as f:
        bs = f.read()
    print()
    print("=== bibtex log ===")
    print(bs[:800])