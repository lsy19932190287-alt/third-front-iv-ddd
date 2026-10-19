"""看 pass 3 log"""
import re
p = r"F:\三线建设\paper\logs\xelatex_pass3.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
print("=== Pass 3 ===")
err_count = len(re.findall(r'^! ', s, re.MULTILINE))
print(f"Errors (!): {err_count}")
undef = len(re.findall(r'undefined', s, re.MULTILINE))
print(f"Undefined: {undef}")
output = re.search(r'Output written on ([^\s]+) \((\d+) pages', s)
if output:
    print(f"Output: {output.group(1)} ({output.group(2)} pages, {len(s):,} chars)")
print()
print("=== First errors ===")
errors = re.findall(r'^! [^\n]+', s, re.MULTILINE)
for e in errors[:10]:
    print(f"  {e[:120]}")