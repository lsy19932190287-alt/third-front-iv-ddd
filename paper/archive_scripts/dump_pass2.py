"""dump pass 2 errors"""
import re

p = r"F:\三线建设\paper\logs\xelatex_final2.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
lines = s.split('\n')
for i, line in enumerate(lines):
    if re.match(r'l\.\d+', line) or line.startswith('!'):
        start = max(0, i-1)
        end = min(len(lines), i+3)
        print(f"\n--- L{i+1} ---")
        for j in range(start, end):
            marker = ">>>" if j == i else "   "
            print(f"  {marker} L{j+1}: {lines[j][:140]}")