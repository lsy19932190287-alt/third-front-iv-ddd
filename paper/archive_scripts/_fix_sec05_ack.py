"""替换 sec05 致谢段 - 使用基于 repr 的精确字符串"""
with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'r', encoding='utf-8') as f:
    sec05 = f.read()

old_ack = '\\begin{center}\n\n\\small\n\n\\textit{本文获得国家社会科学基金重大项目"中国产业政策与制造业\n转型升级研究"(20\\&ZD089) 资助; 三线企业种子数据由陈东林 (2003)\n《中国三线建设口述史》、董志凯 (1999)《三线建设与西部地区现代化》\n及徐现祥 (2017) 等文献整理。通讯作者: 黄炜, huangwei@xxx.edu.cn。}\n\n\\end{center}'

new_ack = '\\begin{center}\n\n\\small\n\n\\textit{三线企业种子数据由陈东林 (2003)《中国三线建设口述史》、\n董志凯 (1999)《三线建设与西部地区现代化》及徐现祥 (2017) 等\n文献整理。通讯作者: 李仕宇, \\texttt{[your-email@example.edu.cn]}\\textsuperscript{*}。\n\n\\textbf{基金项目}: [如有, 请补充 --- 格式: 基金名 (编号)]。}\n\n\\end{center}'

assert old_ack in sec05, "未找到 sec05 的致谢块 (精确字符串)"
sec05 = sec05.replace(old_ack, new_ack)

with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'w', encoding='utf-8') as f:
    f.write(sec05)

print('✓ sec05 致谢段已清理:')
print('  - 删除虚拟基金号 20&ZD089')
print('  - 删除虚拟通讯作者 黄炜, huangwei@xxx.edu.cn')
print('  - 通讯作者改为 李仕宇 + placeholder email')
print('  - 保留陈东林/董志凯/徐现祥文献致谢 (真实)')