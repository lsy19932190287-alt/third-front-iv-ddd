"""查 sec01_intro line 81 实际内容"""
import os
PAPER = r"F:\三线建设\paper"
# sec01_intro.tex line 81
p = os.path.join(PAPER, "sec01_intro.tex")
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"sec01_intro.tex 总行数: {len(lines)}")
# 看 line 7 (整体 xelatex line 81 = main.tex 76 + sec01 line 5)
# 但 main.tex line 76 = \begin{document}, line 77 = 空, line 78 = \maketitle...
# main.tex line 81 = ?
# \input{sec01_intro.tex} 在 main.tex line 69 (相对前一次读)
# 实际上从 dump 看 l.81 字符可能是 sec03 里的 "陈"字

# 检查所有文件
for fn in ["sec01_intro.tex", "sec02_background.tex", "sec03_empirical_strategy.tex",
          "sec04_results.tex", "sec05_robustness_conclusion.tex", "main.tex"]:
    fp = os.path.join(PAPER, fn)
    with open(fp, 'r', encoding='utf-8') as f:
        ls = f.readlines()
    print(f"\n=== {fn} ({len(ls)} lines) ===")
    # search 陈东林 and 陈思远
    for i, line in enumerate(ls, 1):
        if "陈" in line:
            print(f"  L{i}: {line.strip()[:130]}")