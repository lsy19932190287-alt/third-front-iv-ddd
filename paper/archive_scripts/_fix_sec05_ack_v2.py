"""替换 sec05 致谢段 - 用 regex 匹配 (兼容 CRLF/LF)"""
import re

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'r', encoding='utf-8') as f:
    sec05 = f.read()

# 用 regex 匹配整个 center block (DOTALL 模式)
pattern = re.compile(
    r'\\begin\{center\}.*?\\end\{center\}',
    re.DOTALL
)

# 新致谢段 - 用 LF 换行 (LaTeX 通用)
new_block = (
    '\\begin{center}\n'
    '\n'
    '\\small\n'
    '\n'
    '\\textit{三线企业种子数据由陈东林 (2003)《中国三线建设口述史》、'
    '董志凯 (1999)《三线建设与西部地区现代化》及徐现祥 (2017) 等'
    '文献整理。通讯作者: 李仕宇, \\texttt{[your-email@example.edu.cn]}。'
    '\n'
    '\n'
    '\\textbf{基金项目}: [如有, 请补充 --- 格式: 基金名 (编号)]。}'
    '\n'
    '\n'
    '\\end{center}'
)

# 找出现次数
matches = pattern.findall(sec05)
print(f'找到 {len(matches)} 个 center block')
for i, m in enumerate(matches):
    print(f'\n--- Block {i} ---')
    print(m[:200])
    print('...' if len(m) > 200 else '')

# 替换第一个 (也只应该有1个)
sec05_new, n = pattern.subn(new_block, sec05, count=1)
print(f'\n替换次数: {n}')

if n == 0:
    raise SystemExit('替换失败')

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'w', encoding='utf-8') as f:
    f.write(sec05_new)

print('\n✓ sec05 致谢段已清理:')
print('  - 删除虚拟基金号 20&ZD089')
print('  - 删除虚拟通讯作者 黄炜, huangwei@xxx.edu.cn')
print('  - 通讯作者改为 李仕宇 + placeholder email')
print('  - 保留陈东林/董志凯/徐现祥文献致谢 (真实文献)')