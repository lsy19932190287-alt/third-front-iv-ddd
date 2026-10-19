"""看 pass 1 log: 找所有错误位置及上下文 (l.数字)"""
import re

p = r"F:\三线建设\paper\logs\xelatex_final1.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()

# 找 "l.\d+ " 行 (报错行号) 并打印前一行 (error)
lines = s.split('\n')
print(f"Total lines: {len(lines)}")

# 找包含 "l." 和 "!" 的行
for i, line in enumerate(lines):
    if re.match(r'l\.\d+', line) or line.startswith('!'):
        # 打印 [i-2:i+3] 上下文
        start = max(0, i-1)
        end = min(len(lines), i+3)
        print(f"\n--- L{i+1} ---")
        for j in range(start, end):
            marker = ">>>" if j == i else "   "
            print(f"  {marker} L{j+1}: {lines[j][:150]}")