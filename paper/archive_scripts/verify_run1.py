import re
p = r"F:\三线建设\paper\logs\xelatex_run1.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

print("=" * 60)
print("🎯 xelatex run1 (final) 验证")
print("=" * 60)

err_count = len(re.findall(r'^! ', s, re.MULTILINE))
print(f"Errors (!): {err_count}")

undef = len(re.findall(r'undefined', s, re.MULTILINE))
print(f"Undefined references: {undef}")

overfull = len(re.findall(r'Overfull', s, re.MULTILINE))
print(f"Overfull boxes (warning): {overfull}")

output = re.search(r'Output written on ([^\s]+) \((\d+) pages', s)
if output:
    print(f"Output: {output.group(1)} ({output.group(2)} pages)")

import os
pdf = r"F:\三线建设\paper\main.pdf"
if os.path.exists(pdf):
    size = os.path.getsize(pdf)
    print(f"main.pdf size: {size:,} bytes ({size/1024:.1f} KB)")

errors = re.findall(r'^! [^\n]+', s, re.MULTILINE)
for e in errors[:5]:
    print(f"  {e[:120]}")

print()
print("=" * 60)