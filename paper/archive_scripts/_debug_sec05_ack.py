"""调试: 打印 sec05 致谢段的真实 repr"""
import re

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'r', encoding='utf-8') as f:
    s = f.read()

# 找 center block
matches = list(re.finditer(r'\\begin\{center\}.*?\\end\{center\}', s, re.DOTALL))
print(f'Found {len(matches)} center blocks')
for i, m in enumerate(matches):
    print(f'\n--- Block {i} ---')
    print(repr(m.group()))