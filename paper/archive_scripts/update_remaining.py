"""精确修复剩余未替换的 main.tex abstract + sec05 段"""
# === main.tex abstract H2/H3 ===
p = r"F:\三线建设\paper\main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

repl = [
    ("三重交互 $\\hat{\\beta}_{\\mathrm{tech}}=0.32^{**}$, 边际效应技校组 $0.47$ vs 非技校组 $0.15$",
     "三重交互 $\\hat{\\beta}_{\\mathrm{tech}}=0.378^{***}$, 边际效应技校组 $0.622$ vs 非技校组 $0.244$"),
    ("三重交互 $\\hat{\\beta}_{\\mathrm{gpt}}=0.51^{***}$, 边际效应 GPTs 组 $0.67$ vs 非 GPTs 组 $0.16$",
     "三重交互 $\\hat{\\beta}_{\\mathrm{gpt}}=0.297^{**}$, 边际效应 GPTs 组 $0.545$ vs 非 GPTs 组 $0.248$"),
]
for old, new in repl:
    if old in s:
        s = s.replace(old, new)
        print(f"✅ main.tex: {old[:50]}... → updated")
    else:
        print(f"WARN main.tex: {old[:50]}...")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# === sec05 剩余 ===
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

repl = [
    # 注意 `§4` 实际上是 `\\S 4` 中间有空格的两种
    ("DDD 主回归 $\\hat{\\alpha}=0.18$--$0.35$ 在\n\\S 4 中得到一致支持",
     "DDD 主回归 $\\hat{\\alpha}=0.24$--$0.26$ 在\n\\S 4 中得到一致支持"),
    ("与 §4 静态 ATT $\\hat{\\alpha}=0.18$ (IHS-HDFE) 相吻合",
     "与 §4 静态 ATT $\\hat{\\alpha}=0.26$ (IHS-HDFE) 相吻合"),
    ("$\\hat{\\alpha}^{2SLS}\\approx 0.23$ (IV-DDD-2SLS, 一阶段 $F>5000$, Hansen J $p=0.40$",
     "$\\hat{\\alpha}^{2SLS}=0.247^{**}$ (IV-DDD-2SLS, 一阶段 $F=7797$, Hansen J $p=0.173$"),
    # H3 GPTs 折价 (-0.34) 已经是上一轮成功替换了. 检查:
    # 但根据用户之前 sec05 中"折价 (-0.34)"是 Round 9 老数字, 现在应为 (-0.297)
    # 之前的更新已经替换为 (-0.297). 现在不需要再改
    # 检查文中是否有 0.18 残留
]
for old, new in repl:
    if old in s:
        s = s.replace(old, new)
        print(f"✅ sec05: {old[:50]}... → updated")
    else:
        print(f"WARN sec05: {old[:50]}...")

# 检查残留的 0.18 数字 (Round 11 应已替换完)
print()
print("=== 检查残留的'0.18'数字 (Round 9 数字) ===")
for i, line in enumerate(s.split("\n"), 1):
    if "0.18" in line or "0.179" in line or "0.149" in line:
        print(f"  L{i}: {line.strip()[:120]}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)