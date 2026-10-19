"""看 pass 2 log 中 line 81 前后 50 字符 (精确)"""
with open(r"F:\三线建设\paper\logs\xelatex_final2.log", 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

# 找所有 "l.81" 或 "l.81\n" 后接的字符
import re

# 找 "l.\d+ " 后跟几行的内容
for m in re.finditer(r'l\.(\d+)\s*\n([^\n]*)', s):
    line_no = m.group(1)
    content = m.group(2)
    if int(line_no) in [80, 81, 82, 83, 84, 85, 90, 91, 92, 93, 94, 95, 126]:
        print(f"l.{line_no}: {content[:200]}")