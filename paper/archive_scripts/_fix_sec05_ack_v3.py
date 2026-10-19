"""替换 sec05 致谢段 - 用 regex 找到精确字符串再 replace"""
import re

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'r', encoding='utf-8') as f:
    sec05 = f.read()

# 用 regex 匹配 (DOTALL)
pattern = re.compile(
    r'\\begin\{center\}.*?\\end\{center\}',
    re.DOTALL
)

# 新致谢段 (用 LF, LaTeX 通用)
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

# 找出现次数 (不用 subn, 改用 findall + 拼接)
matches = list(pattern.finditer(sec05))
print(f'找到 {len(matches)} 个 center block')
assert len(matches) == 1, f'期望1个, 实际{len(matches)}个'

# 拼接: prefix + new_block + suffix
m = matches[0]
prefix = sec05[:m.start()]
suffix = sec05[m.end():]
sec05_new = prefix + new_block + suffix

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'w', encoding='utf-8') as f:
    f.write(sec05_new)

print('✓ sec05 致谢段已清理:')
print('  - 删除虚拟基金号 20&ZD089')
print('  - 删除虚拟通讯作者 黄炜, huangwei@xxx.edu.cn')
print('  - 通讯作者改为 李仕宇 + placeholder email')
print('  - 保留陈东林/董志凯/徐现祥文献致谢 (真实文献)')