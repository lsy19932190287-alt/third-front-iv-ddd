"""raw bytes 精准修复"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    raw = f.read()
s = raw.decode('utf-8')

# 替换 1: $\hat{\alpha}^{2SLS}\approx 0.23$ 段 (跨行)
# 实际是: "...与\n       $\hat{\alpha}^{2SLS}\\approx 0.23$ (IV-DDD-2SLS, 一阶段 $F>5000$,"
old1 = '       $\\hat{\\alpha}^{2SLS}\\approx 0.23$ (IV-DDD-2SLS, 一阶段 $F>5000$,'
new1 = '       $\\hat{\\alpha}^{2SLS}=0.247^{**}$ (IV-DDD-2SLS, 一阶段 $F=7797$,'
if old1 in s:
    s = s.replace(old1, new1)
    print(f"✅ sec05 1: $\\hat{{\\alpha}}^{{2SLS}}\\approx 0.23$ replaced")
else:
    print(f"WARN 1 not found")

# 替换 2: \S 4 静态 ATT (实际是 \\S 4)
old2 = "$\\hat{\\alpha}=0.18$ (IHS-HDFE) 相吻合"
new2 = "$\\hat{\\alpha}=0.259^{***}$ (IHS-HDFE) 相吻合"
if old2 in s:
    s = s.replace(old2, new2)
    print(f"✅ sec05 2: ATT=0.18 → 0.259*** replaced")
else:
    print(f"WARN 2 not found")

# 替换 3: Hansen J p=0.40$ 后接的 $p=0.40$ 后接换行
# 找 "Hansen J $p=0.40$"
old3 = "Hansen J $p=0.40$"
new3 = "Hansen J $p=0.173$"
if old3 in s:
    s = s.replace(old3, new3)
    print(f"✅ sec05 3: Hansen J p=0.40 → p=0.173")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# === main.tex abstract H2/H3 ===
p2 = r"F:\三线建设\paper\main.tex"
with open(p2, 'r', encoding='utf-8') as f:
    s2 = f.read()

# main.tex abstract 中实际可能是 (2)$ multi-line): 用更宽松的 regex
import re

# 找带"三重交互"段, 替换 0.32 → 0.378 和 0.51 → 0.297
m = re.search(r'三重交互\s*(\$[^$]*\$)\s*,\s*边际效应技校组\s*(\$[^$]*\$)\s*vs\s*非技校组\s*(\$[^$]*\$)', s2)
if m:
    print(f"找到 tech 段: {m.group(1)} / {m.group(2)} / {m.group(3)}")
    # 替换整段
    new_seg = f"三重交互 $\\hat{{\\beta}}_{{\\mathrm{{tech}}}}=0.378^{{***}}$, 边际效应技校组 $0.622$ vs 非技校组 $0.244$"
    s2 = s2.replace(m.group(0), new_seg)
    print(f"✅ main.tex abstract: H2 三重交互段已替换")

m = re.search(r'三重交互\s*(\$[^$]*\$)\s*,\s*边际效应 GPTs 组\s*(\$[^$]*\$)\s*vs\s*非 GPTs 组\s*(\$[^$]*\$)', s2)
if m:
    print(f"找到 gpt 段: {m.group(1)} / {m.group(2)} / {m.group(3)}")
    new_seg = f"三重交互 $\\hat{{\\beta}}_{{\\mathrm{{gpt}}}}=0.297^{{**}}$, 边际效应 GPTs 组 $0.545$ vs 非 GPTs 组 $0.248$"
    s2 = s2.replace(m.group(0), new_seg)
    print(f"✅ main.tex abstract: H3 三重交互段已替换")

with open(p2, 'w', encoding='utf-8') as f:
    f.write(s2)