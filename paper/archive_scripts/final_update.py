"""精准最后修复"""
import re

# === main.tex abstract ===
p = r"F:\三线建设\paper\main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 找 abstract 中的 H2/H3 数字
# 使用正则匹配更宽松的 pattern
repl = [
    (r"\\hat\{\\beta\}_\{\\mathrm\{tech\}\}=0\.32\^\{\*\*\}, 边际效应技校组 \$0\.47\$ vs 非技校组 \$0\.15\$",
     r"\\hat{\\beta}_{\\mathrm{tech}}=0.378^{***}, 边际效应技校组 $0.622$ vs 非技校组 $0.244$"),
    (r"\\hat\{\\beta\}_\{\\mathrm\{gpt\}\}=0\.51\^\{\*\*\*\}, 边际效应 GPTs 组 \$0\.67\$ vs 非 GPTs 组 \$0\.16\$",
     r"\\hat{\\beta}_{\\mathrm{gpt}}=0.297^{**}, 边际效应 GPTs 组 $0.545$ vs 非 GPTs 组 $0.248$"),
]
count = 0
for pat, new in repl:
    new_s, n = re.subn(pat, new, s)
    if n > 0:
        s = new_s
        count += n
        print(f"✅ main.tex: regex matched {n}x  -> updated")
    else:
        print(f"WARN main.tex: regex no match")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# === sec05 剩余 0.18 ===
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

repl = [
    # L76 "Panel E 显示 $\hat{\alpha}^{2SLS}_{\log(\mathrm{regfee})}=0.18$" - 保持不变 (这是稳健性测试)
    # L100 "基础 ATT 估计 $\hat{\alpha}\approx 0.18$ (IHS-HDFE)" - 这是结论段, 应改为 0.26
    ("基础 ATT 估计 $\\hat{\\alpha}\\approx 0.18$ (IHS-HDFE) 与",
     "基础 ATT 估计 $\\hat{\\alpha}=0.259^{***}$ (IHS-HDFE) 与"),
    # L38 "系数从 0.07 单调上升至 0.18" - 保持不变 (这是 event study 描述)
    # "与 §4 静态 ATT $\hat{\alpha}=0.18$ (IHS-HDFE) 相吻合" - 改为 0.26
    ("与 §4 静态 ATT $\\hat{\\alpha}=0.18$ (IHS-HDFE) 相吻合",
     "与 §4 静态 ATT $\\hat{\\alpha}=0.259^{***}$ (IHS-HDFE) 相吻合"),
    # "$\hat{\alpha}^{2SLS}\\approx 0.23$ (IV-DDD-2SLS, 一阶段 $F>5000$, Hansen J $p=0.40$"
    ("$\\hat{\\alpha}^{2SLS}\\approx 0.23$ (IV-DDD-2SLS, 一阶段 $F>5000$, Hansen J $p=0.40$",
     "$\\hat{\\alpha}^{2SLS}=0.247^{**}$ (IV-DDD-2SLS, 一阶段 $F=7797$, Hansen J $p=0.173$"),
]
count = 0
for old, new in repl:
    if old in s:
        s = s.replace(old, new)
        count += 1
        print(f"✅ sec05: {old[:50]}... → updated")
    else:
        print(f"WARN sec05: {old[:50]}...")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# Final 检查
print()
print("=== 最后检查残留 '0.18' (除了已知保留位置) ===")
for p, fp in [(r"F:\三线建设\paper\main.tex", "main.tex"),
              (r"F:\三线建设\paper\sec05_robustness_conclusion.tex", "sec05")]:
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    for i, line in enumerate(s.split("\n"), 1):
        # 跳过 event study 描述 (0.07--0.18 是合理的)
        # 跳过稳健性测试 (Panel E 显示 ...0.18)
        # 跳过 0.18--0.35 已被替换
        if "0.18" in line and "event" not in line.lower() and "Panel E" not in line and "系数从" not in line:
            print(f"  [{fp} L{i}]: {line.strip()[:120]}")