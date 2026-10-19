"""看 xelatex pass 4 log 末尾错误"""
p = r"F:\三线建设\paper\logs\xelatex_pass4.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
import re
# 输出最后 100 行 (含 \n\n)
lines = s.split('\n')
for line in lines[-80:]:
    print(line)
