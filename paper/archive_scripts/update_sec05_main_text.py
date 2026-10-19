"""更新 main.tex abstract + sec05 中数字 (Round 11)"""
import re

# === main.tex abstract ===
p = r"F:\三线建设\paper\main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

main_replacements = [
    # abstract
    ("基础 ATT $\\hat{\\alpha}=0.18^{***}$ (TWFE-IHS-HDFE),\n   $\\hat{\\alpha}^{2SLS}=0.23$ (IV-DDD-2SLS, F=5701, Hansen J $p=0.40$)。\n   PPML 独立泊松估计给出 $\\hat{\\alpha}_{\\mathrm{PPML}}=0.57^{***}$",
     "基础 ATT $\\hat{\\alpha}=0.259^{***}$ (TWFE-IHS-HDFE),\n   $\\hat{\\alpha}^{2SLS}=0.247^{**}$ (IV-DDD-2SLS, F=7797, Hansen J $p=0.173$)。\n   PPML 独立泊松估计给出 $\\hat{\\alpha}_{\\mathrm{PPML}}=0.409^{***}$"),
    ("三重交互 $\\hat{\\beta}_{\\mathrm{tech}}=0.32^{**}$, 边际效应技校组 $0.47$ vs 非技校组 $0.15$",
     "三重交互 $\\hat{\\beta}_{\\mathrm{tech}}=0.378^{***}$, 边际效应技校组 $0.622$ vs 非技校组 $0.244$"),
    ("三重交互 $\\hat{\\beta}_{\\mathrm{gpt}}=0.51^{***}$, 边际效应 GPTs 组 $0.67$ vs 非 GPTs 组 $0.16$",
     "三重交互 $\\hat{\\beta}_{\\mathrm{gpt}}=0.297^{**}$, 边际效应 GPTs 组 $0.545$ vs 非 GPTs 组 $0.248$"),
    # appendix DGP 真实 beta
    ("H2 技校溢价: $\\beta_{\\mathrm{tech}} = 0.14$", "H2 技校溢价: $\\beta_{\\mathrm{tech}} = 0.14$  (Round 11 实际估计 $\\hat{\\beta}_{\\mathrm{tech}}=0.378$)"),
    ("H3 GPT 溢价: $\\beta_{\\mathrm{gpt}} = 0.16$", "H3 GPT 溢价: $\\beta_{\\mathrm{gpt}} = 0.16$  (Round 11 注入 $\\beta_{\\mathrm{gpt}}=0.45$, 实际估计 $\\hat{\\beta}_{\\mathrm{gpt}}=0.297$)"),
]
count = 0
for old, new in main_replacements:
    if old in s:
        s = s.replace(old, new)
        count += 1
    else:
        print(f"WARN: main.tex 找不到 old: {old[:50]}...")
print(f"main.tex: {count}/{len(main_replacements)} 替换成功")
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# === sec05_robustness_conclusion.tex ===
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

sec05_replacements = [
    # 引用 IV-DDD-2SLS
    ("$\\hat{\\alpha}_{\\mathrm{LD}}^{2SLS}$ 在 0.22--0.26 之间, 与 §4 主回归的 $\\hat{\\alpha}^{2SLS}=0.232$\n高度一致", "$\\hat{\\alpha}_{\\mathrm{LD}}^{2SLS}$ 在 0.22--0.26 之间, 与 §4 主回归的 $\\hat{\\alpha}^{2SLS}=0.247$\n高度一致"),
    ("Hansen J 检验在 10\\% 水平上不拒绝\n($\\chi^2(1)\\approx 0.7$, $p\\approx 0.40$)", "Hansen J 检验在 10\\% 水平上不拒绝\n($\\chi^2(1)\\approx 1.86$, $p\\approx 0.17$)"),
    # sec05 中描述 DDD 主回归
    ("DDD 主回归 $\\hat{\\alpha}=0.18$--$0.35$ 在\n§4 中得到一致支持",
     "DDD 主回归 $\\hat{\\alpha}=0.24$--$0.26$ 在\n§4 中得到一致支持"),
    ("与 §4 静态 ATT $\\hat{\\alpha}=0.18$ (IHS-HDFE) 相吻合",
     "与 §4 静态 ATT $\\hat{\\alpha}=0.26$ (IHS-HDFE) 相吻合"),
    # 结论段
    ("Panel B 显示, 剥离后的 $\\hat{\\alpha}^{2SLS}=0.219$ 与全样本 0.232 接近",
     "Panel B 显示, 剥离后的 $\\hat{\\alpha}^{2SLS}=0.219$ 与全样本 0.247 接近"),
    ("Panel C 第 (1) 列的虚假 Post 时点 4 年提前处理, 给出 $\\hat{\\alpha}_{\\mathrm{placebo}}=0.04$",
     "Panel C 第 (1) 列的虚假 Post 时点 4 年提前处理, 给出 $\\hat{\\alpha}_{\\mathrm{placebo}}=0.040$"),
    ("Panel C 第 (2) 列的虚假处理组 $\\hat{\\alpha}_{\\mathrm{placebo}}=0.02$",
     "Panel C 第 (2) 列的虚假处理组 $\\hat{\\alpha}_{\\mathrm{placebo}}=0.022$"),
    ("Panel D 显示, 排除这 6 年观测后, $\\hat{\\alpha}^{2SLS}=0.241$",
     "Panel D 显示, 排除这 6 年观测后, $\\hat{\\alpha}^{2SLS}=0.241$"),
    ("Panel E 显示 $\\hat{\\alpha}^{2SLS}_{\\log(\\mathrm{regfee})}=0.18$",
     "Panel E 显示 $\\hat{\\alpha}^{2SLS}_{\\log(\\mathrm{regfee})}=0.18$"),
    # 结论 H1 / H2 / H3
    ("$\\hat{\\alpha}^{2SLS}\\approx 0.23$ (IV-DDD-2SLS, 一阶段 $F>5000$, Hansen J $p=0.40$",
     "$\\hat{\\alpha}^{2SLS}=0.247^{**}$ (IV-DDD-2SLS, 一阶段 $F=7797$, Hansen J $p=0.173$"),
    ("PPML 估计独立给出 $\\hat{\\alpha}_{\\mathrm{PPML}}\\approx 0.57$",
     "PPML 估计独立给出 $\\hat{\\alpha}_{\\mathrm{PPML}}=0.409^{***}$"),
    ("三重交互项 $\\hat{\\beta}_{\\mathrm{tech}}=0.32^{**}$\n       (全样本, $p=0.020$), 边际效应: 技校组 $0.47$ vs 非技校组 $0.15$",
     "三重交互项 $\\hat{\\beta}_{\\mathrm{tech}}=0.378^{***}$\n       (全样本, $t=3.12$, $p=0.002$), 边际效应: 技校组 $0.622$ vs 非技校组 $0.244$"),
    ("三重交互项 $\\hat{\\beta}_{\\mathrm{gpt}}=0.51^{***}$\n       (全样本, $p=0.006$), 边际效应: GPTs 组 $0.67$ vs 非 GPTs 组 $0.16$",
     "三重交互项 $\\hat{\\beta}_{\\mathrm{gpt}}=0.297^{**}$\n       (全样本, $t=2.13$, $p=0.033$), 边际效应: GPTs 组 $0.545$ vs 非 GPTs 组 $0.248$"),
    # 政策启示
    ("H2 三重交互 (技校人力资本溢价 0.32) 显著大于 H3 GPTs 资产专用性\n       折价 (-0.34)",
     "H2 三重交互 (技校人力资本溢价 0.378) 显著大于 H3 GPTs 资产专用性\n       折价 (-0.297)"),
    ("约 0.18--0.23 个 IHS 单位的县域-行业民营经济增量",
     "约 0.24--0.26 个 IHS 单位的县域-行业民营经济增量"),
    # 结束语
    ("1980 年代的三线企业\"脱险搬迁\" (Adjust$\\rightarrow$Exit), 在 1990 年代之后\n释放出 \\textbf{约 0.18--0.23 个 IHS 单位",
     "1980 年代的三线企业\"脱险搬迁\" (Adjust$\\rightarrow$Exit), 在 1990 年代之后\n释放出 \\textbf{约 0.24--0.26 个 IHS 单位"),
    # 综合评估
    ("估计效应在 0.15--0.27 之间", "估计效应在 0.22--0.27 之间"),
]
count = 0
for old, new in sec05_replacements:
    if old in s:
        s = s.replace(old, new)
        count += 1
    else:
        print(f"WARN: sec05 找不到 old: {old[:50]}...")
print(f"sec05: {count}/{len(sec05_replacements)} 替换成功")
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)