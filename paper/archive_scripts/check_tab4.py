"""看 tab4 实际内容 (line 14 附近)"""
p = r"F:\三线建设\paper\tables\tab4_h3.tex"
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[10:25], start=11):
    print(f'{i:3d}: {line.rstrip()}')
