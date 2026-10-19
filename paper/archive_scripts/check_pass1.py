"""分析 xelatex pass 1 错误"""
import re

p = r"F:\三线建设\paper\logs\xelatex_final1.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

print("=== Pass 1 Status ===")
# Errors
err_count = len(re.findall(r'^! ', s, re.MULTILINE))
print(f"Errors (!): {err_count}")

# Undefined refs
undef_count = len(re.findall(r'undefined', s, re.MULTILINE))
print(f"Undefined references: {undef_count}")

# Output written
output_match = re.search(r'Output written on ([^\s]+) \((\d+) pages', s)
if output_match:
    print(f"Output: {output_match.group(1)} ({output_match.group(2)} pages)")

# Show first few errors
print("\n=== First errors ===")
errors = re.findall(r'^! .+', s, re.MULTILINE)
for e in errors[:20]:
    print(f"  {e[:120]}")

# Show undefined refs
print("\n=== Undefined refs ===")
undefs = re.findall(r"Reference `([^`]+)' on page \d+ undefined", s)
for u in undefs[:10]:
    print(f"  {u}")