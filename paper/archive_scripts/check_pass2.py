"""检查 pass 2 log"""
import re

p = r"F:\三线建设\paper\logs\xelatex_final2.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

print("=== Pass 2 Status ===")
err_count = len(re.findall(r'^! ', s, re.MULTILINE))
print(f"Errors (!): {err_count}")

undef_count = len(re.findall(r'undefined', s, re.MULTILINE))
print(f"Undefined references: {undef_count}")

output_match = re.search(r'Output written on ([^\s]+) \((\d+) pages', s)
if output_match:
    print(f"Output: {output_match.group(1)} ({output_match.group(2)} pages)")

# 哪些 refs undefined
undefs = re.findall(r"Reference `([^`]+)' on page \d+ undefined", s)
if undefs:
    print("\nUndefined refs:")
    for u in undefs:
        print(f"  {u}")

# 错误首几行
print("\nFirst errors:")
errors = re.findall(r'^! [^\n]+', s, re.MULTILINE)
for e in errors[:10]:
    print(f"  {e[:120]}")