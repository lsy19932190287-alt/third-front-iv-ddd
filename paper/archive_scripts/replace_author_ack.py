"""替换作者与致谢信息"""
import re

# ============ main.tex 作者块 ============
MAIN_PATH = r'F:\三线建设\paper\main.tex'

with open(MAIN_PATH, 'r', encoding='utf-8') as f:
    main = f.read()

# 替换 author block
old_author = r'''\author{
  黄炜\thanks{通讯作者, 邮箱: huangwei@xxx.edu.cn}\textsuperscript{a,b}\quad
  王雪\textsuperscript{b}\quad
  陈思远\textsuperscript{c}
  \small
  \textsuperscript{a}中国宏观经济研究院\quad
  \textsuperscript{b}清华大学经济管理学院\quad
  \textsuperscript{c}中国社会科学院数量经济与技术经济研究所
}'''

new_author = r'''\author{
  李仕宇\footnote{通讯作者.
    Email: \texttt{[your-email@example.edu.cn]}.}
  \\[0.5em]
  \small\textsuperscript{*} [作者单位 --- 请补充]
}'''

assert old_author in main, "未找到 main.tex 的 author block"
main = main.replace(old_author, new_author)

# 替换 pdfauthor 行
old_pdf = '  pdfauthor={黄炜, 王雪, 陈思远},'
new_pdf = '  pdfauthor={李仕宇},'
assert old_pdf in main, "未找到 pdfauthor 行"
main = main.replace(old_pdf, new_pdf)

with open(MAIN_PATH, 'w', encoding='utf-8') as f:
    f.write(main)

print("✓ main.tex 作者块已替换为 李仕宇 (通讯作者)")
print("✓ main.tex pdfauthor 已替换")

# ============ sec05_robustness_conclusion.tex 致谢 ============
SEC05_PATH = r'F:\三线建设\paper\sec05_robustness_conclusion.tex'

with open(SEC05_PATH, 'r', encoding='utf-8') as f:
    sec05 = f.read()

# 致谢段 (注意: 实际文件里是 \&, 在 Python 字符串里写 \\&)
old_ack = r'''\begin{center}
\small
\textit{本文获得国家社会科学基金重大项目"中国产业政策与制造业
转型升级研究"(20\&ZD089) 资助; 三线企业种子数据由陈东林 (2003)
《中国三线建设口述史》、董志凯 (1999)《三线建设与西部地区现代化》
及徐现祥 (2017) 等文献整理。通讯作者: 黄炜, huangwei@xxx.edu.cn。}
\end{center}'''

new_ack = r'''\begin{center}
\small
\textit{三线企业种子数据由陈东林 (2003)《中国三线建设口述史》、
董志凯 (1999)《三线建设与西部地区现代化》及徐现祥 (2017) 等
文献整理。通讯作者: 李仕宇, \texttt{[your-email@example.edu.cn]。

\textbf{基金项目}: [如有, 请补充 --- 格式: 基金名 (编号)]。}
\end{center}'''

assert old_ack in sec05, "未找到 sec05 的致谢块"
sec05 = sec05.replace(old_ack, new_ack)

with open(SEC05_PATH, 'w', encoding='utf-8') as f:
    f.write(sec05)

print("✓ sec05 致谢段已清理:")
print("    - 删除虚拟基金号 20&ZD089")
print("    - 删除虚拟通讯作者 黄炜, huangwei@xxx.edu.cn")
print("    - 通讯作者改为 李仕宇 + placeholder email")
print("    - 保留陈东林/董志凯/徐现祥文献致谢 (这部分是真实的)")