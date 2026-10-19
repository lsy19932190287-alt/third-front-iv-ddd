"""用 raw bytes 替换, 处理可能的空格/换行差异"""
import re

p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# sec05 中"与 §4"实际可能是 "与 \S 4" 或 "与§4"
# "$\hat{\alpha}^{2SLS}\\approx 0.23$" 实际可能是 "$\\hat{\\alpha}^{2SLS}\\approx 0.23$" 编码差异
# 让我搜两个没替换的实际位置

# search patterns
for kw in ["0.23$", "0.18$ (IHS-HDFE)", "0.23$"]:
    for m in re.finditer(re.escape(kw), s):
        start = max(0, m.start() - 80)
        end = min(len(s), m.end() + 50)
        print(f"找到 '{kw}' at {m.start()}:")
        print(f"  ...{s[start:end]}...")
        print()