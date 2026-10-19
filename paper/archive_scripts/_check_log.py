"""查看 main.log 中错误位置和上下文"""
with open(r'F:\三线建设\paper\main.log', 'r', encoding='utf-8', errors='ignore') as f:
    log = f.read()

lines = log.split('\n')
print(f'main.log 共 {len(lines)} 行')

# 找 ! 错误
for i, l in enumerate(lines):
    if l.startswith('!') or 'Paragraph ended' in l or 'Extra }' in l:
        print(f'\n[ERROR at line {i}]: {l}')
        # 打印上下文
        ctx_start = max(0, i-3)
        ctx_end = min(len(lines), i+15)
        for j in range(ctx_start, ctx_end):
            marker = ' >>> ' if j == i else '     '
            print(f'  {marker}[{j}] {lines[j]}')

# 也找 l.<num> 引用
print('\n--- l.XXX 错误引用 ---')
import re
for i, l in enumerate(lines):
    if re.search(r'l\.\d+', l):
        print(f'  [{i}] {l}')