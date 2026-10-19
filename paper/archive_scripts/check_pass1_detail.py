"""看 pass 1 log 错误详情"""
import re

p = r"F:\三线建设\paper\logs\xelatex_final1.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

# 找所有错误上下文
errors = re.finditer(r'! [^\n]+\n[^\n]*\nl\.\d+ [^\n]*\n?', s, re.MULTILINE)
for i, e in enumerate(list(errors)[:15]):
    print(f"=== Error #{i+1} ===")
    print(e.group(0))
    print()