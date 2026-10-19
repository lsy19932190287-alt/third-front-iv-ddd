"""修复 sec05 致谢段 - 解除 itext/textbf 嵌套错位"""
import re

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'r', encoding='utf-8') as f:
    sec05 = f.read()

# 旧 block (有错)
old_block = (
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

# 新 block (把 textbf 放在 itext 外)
new_block = (
    '\\begin{center}\n'
    '\n'
    '\\small\n'
    '\n'
    '\\textit{三线企业种子数据由陈东林 (2003)《中国三线建设口述史》、'
    '董志凯 (1999)《三线建设与西部地区现代化》及徐现祥 (2017) 等'
    '文献整理。通讯作者: 李仕宇, \\texttt{[your-email@example.edu.cn]}。}\n'
    '\n'
    '\n'
    '\\textbf{基金项目}: [如有, 请补充 --- 格式: 基金名 (编号)]。\n'
    '\n'
    '\\end{center}'
)

assert old_block in sec05, '未找到旧 block'
sec05 = sec05.replace(old_block, new_block)

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'w', encoding='utf-8') as f:
    f.write(sec05)

print('✓ sec05 致谢段已解除 \\textit/\\textbf 嵌套错位:')
print('  - \\textit{...} 现在独立配对 (到第一个 } 闭合)')
print('  - \\textbf{基金项目} 放在外层, 不再嵌在 itext 中')