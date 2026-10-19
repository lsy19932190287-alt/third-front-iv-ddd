"""检查 fig:eventstudy 标签一致性"""
import os, re, glob

PAPER = r"F:\三线建设\paper"
for f in sorted(glob.glob(PAPER + "\\sec*.tex")) + [PAPER + "\\main.tex"]:
    with open(f, 'r', encoding='utf-8') as fh:
        s = fh.read()
    # 找出所有 fig:eventstudy* 引用
    labels = re.findall(r'\\label\{(fig:[^}]+)\}', s)
    refs = re.findall(r'\\ref\{(fig:[^}]+)\}', s)
    if labels or refs:
        print(f"\n=== {os.path.basename(f)} ===")
        for l in labels:
            print(f"  LABEL: {l}")
        for r in refs:
            print(f"  REF:   {r}")