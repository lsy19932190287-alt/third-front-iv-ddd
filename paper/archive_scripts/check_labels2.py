"""检查 sec:mech / sec:concl / tab:longdiff 是否定义"""
import re
import os

PAPER = r"F:\三线建设\paper"

# 找所有 sec*.tex 中的 \label 和 \ref
for fn in ["sec01_intro.tex", "sec02_background.tex", "sec03_empirical_strategy.tex",
          "sec04_results.tex", "sec05_robustness_conclusion.tex"]:
    p = os.path.join(PAPER, fn)
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    labels = re.findall(r'\\label\{([^}]+)\}', s)
    refs = re.findall(r'\\ref\{([^}]+)\}', s)
    print(f"\n=== {fn} ===")
    if labels:
        print(f"  labels: {labels}")
    if refs:
        print(f"  refs: {refs}")