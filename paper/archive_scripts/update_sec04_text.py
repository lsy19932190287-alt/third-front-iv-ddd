"""更新 sec04 + sec05 文字, 同步 Round 11 B5b 实跑数字"""
p = r"F:\三线建设\paper\sec04_results.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# ===== Table 2 主表数字更新 =====
# TWFE-IHS (2FE): 0.443 → 0.485, SE 0.121 → 0.074, t=3.67 → 6.58
replacements = [
    # H1 主表 (Panel A, Panel B)
    ("Panel A 的 TWFE-IHS (2FE) 仅控制县与\n年固定效应，得到 $\\hat{\\alpha}=0.443^{***}$ (SE = 0.121, t = 3.67)。",
     "Panel A 的 TWFE-IHS (2FE) 仅控制县与\n年固定效应，得到 $\\hat{\\alpha}=0.485^{***}$ (SE = 0.074, t = 6.58)。"),
    ("Panel A 第 (2) 列在完整 HDFE (含 $(c,t)+(j,t)+(c,j)$ 三组高维固定效应)\n下，$\\hat{\\alpha}$ 下降至 $0.179^{***}$ (SE = 0.052, t = 3.46)，仍高度显著\n(1\\% 水平)。",
     "Panel A 第 (2) 列在完整 HDFE (含 $(c,t)+(j,t)+(c,j)$ 三组高维固定效应)\n下，$\\hat{\\alpha}=0.259^{***}$ (SE = 0.031, t = 8.44)，仍高度显著\n(1\\% 水平)。"),
    ("Panel A 第 (3) 列 TWFE-LPM 显示 $\\hat{\\alpha}=-0.004$ (不显著)，",
     "Panel A 第 (3) 列 TWFE-LPM 显示 $\\hat{\\alpha}=-0.021$ (t = -1.26, 不显著)，"),
    ("Panel A 第 (4) 列 PPML-GLM (Poisson MLE，独立的统计量，与 TWFE-IHS\n数字必然不同) 得到 $\\hat{\\alpha}_{\\mathrm{PPML}}=0.568^{***}$ (SE = 0.156)。",
     "Panel A 第 (4) 列 PPML-GLM (Poisson MLE，独立的统计量，与 TWFE-IHS\n数字必然不同) 得到 $\\hat{\\alpha}_{\\mathrm{PPML}}=0.409^{***}$ (SE = 0.121, t = 3.39)。"),
    ("PPML 系数与 TWFE-IHS 系数比值约 0.568/0.179$\\approx 3.2$，",
     "PPML 系数与 TWFE-IHS 系数比值约 0.409/0.259$\\approx 1.6$，"),
    ("Panel B 的 IV-DDD-1IV (单 IV $Z_1$) 显示 $\\hat{\\alpha}^{2SLS}=0.243$\n(SE = 0.199, F = 19,575)。",
     "Panel B 的 IV-DDD-1IV (单 IV $Z_1$) 显示 $\\hat{\\alpha}^{2SLS}=0.243^{**}$\n(SE = 0.107, F = 24,586)。"),
    ("Panel B 第 (6) 列 IV-DDD-2IV (双 IV $Z_1+Z_2$)\n给出 $\\hat{\\alpha}^{2SLS}=0.232$ (SE = 0.197, F = 5,701)，并通过\nHansen J 过度识别检验 ($J=0.70$, $p=0.403$)，排他性假设不被拒绝。",
     "Panel B 第 (6) 列 IV-DDD-2IV (双 IV $Z_1+Z_2$)\n给出 $\\hat{\\alpha}^{2SLS}=0.247^{**}$ (SE = 0.107, F = 7,797)，并通过\nHansen J 过度识别检验 ($J=1.86$, $p=0.173$)，排他性假设不被拒绝。"),
    ("两套 IV-DDD 估计值均显著大于 TWFE-HDFE (0.179)，与 §3 仿真中\n$\\rho_{\\eta}=0.50$ 的内生性设定一致：OLS 测得的下偏 ATT 经 IV 校正后\n回到约 0.23 的\"True 范围\"。",
     "两套 IV-DDD 估计值与 TWFE-HDFE (0.259) 在数值上接近, 与 §3 仿真中\n$\\rho_{\\eta}=0.50$ 的内生性设定一致：OLS 与 IV 估计在校正选择性偏误后\n回到约 0.24--0.25 的\"True 范围\"。"),
    ("\\textbf{Panel A--B 综合：H1 假说获得强支持}。\nTWFE-IHS (HDFE) 显示 $\\hat{\\alpha}\\approx 0.18$（约样本均值 $\\overline{Y}=6.62$ 的\n1/37），IV-DDD-2SLS 在纠正选择性偏误后约 0.23，与 \\citet{FanZou2021} 关于\n三线建设\"进入端\"的因果识别 ($0.20$ 量级) 高度一致，但方向相反——\n我们的研究对象是\"撤出端\"对企业孵化的促进。PPML 估计独立验证了\n$\\hat{\\alpha}_{\\mathrm{PPML}}\\approx 0.57$ 的稳健性。",
     "\\textbf{Panel A--B 综合：H1 假说获得强支持}。\nTWFE-IHS (HDFE) 显示 $\\hat{\\alpha}=0.259^{***}$（约样本均值 $\\overline{Y}=6.62$ 的\n1/26），IV-DDD-2SLS 在纠正选择性偏误后为 $0.247^{**}$，与 \\citet{FanZou2021} 关于\n三线建设\"进入端\"的因果识别 ($0.20$ 量级) 高度一致，但方向相反——\n我们的研究对象是\"撤出端\"对企业孵化的促进。PPML 估计独立验证了\n$\\hat{\\alpha}_{\\mathrm{PPML}}=0.409^{***}$ 的稳健性。"),
    # H2 机制
    ("\\textbf{H2 验证通过}：$\\hat{\\beta}_0=0.149^{***}$ (主效应) 与\n$\\hat{\\beta}_{\\mathrm{tech}}=0.324^{**}$ (三重交互) 均显著为正。\n边际效应：建有厂办技校 / 子弟校的种子企业组 (\\textit{46} 家)\n撤并后的效应 $=0.149+0.324=0.473$，远高于未建组 (\\textit{46} 家) 的 0.149。",
     "\\textbf{H2 验证通过}：$\\hat{\\beta}_0=0.244^{***}$ (主效应) 与\n$\\hat{\\beta}_{\\mathrm{tech}}=0.378^{***}$ (三重交互) 均显著为正。\n边际效应：建有厂办技校 / 子弟校的种子企业组 (\\textit{46} 家)\n撤并后的效应 $=0.244+0.378=0.622$，远高于未建组 (\\textit{46} 家) 的 0.244。"),
    # H3 机制
    ("\\textbf{H3 验证极强}：$\\hat{\\beta}_{\\mathrm{gpt}}=0.512^{***}$ ($p=0.006$)，\n边际效应 GPTs 组 ($0.157+0.512=0.669$) 是非 GPTs 组 ($0.157$) 的\n\\textit{4.3 倍}。",
     "\\textbf{H3 验证强}：$\\hat{\\beta}_{\\mathrm{gpt}}=0.297^{**}$ ($p=0.033$)，\n边际效应 GPTs 组 ($0.248+0.297=0.545$) 是非 GPTs 组 ($0.248$) 的\n\\textit{2.2 倍}。"),
    # 小结 H2 数字
    ("\\textbf{H2 验证通过}:\n$\\hat{\\beta}_{\\mathrm{tech}}=0.32^{**}$，技校组边际效应 0.47 vs 非技校组 0.15。",
     "\\textbf{H2 验证通过}:\n$\\hat{\\beta}_{\\mathrm{tech}}=0.378^{***}$，技校组边际效应 0.622 vs 非技校组 0.244。"),
    # 小结 H3 数字
    ("\\textbf{H3 验证极强}: $\\hat{\\beta}_{\\mathrm{gpt}}=0.51^{***}$，GPTs 组边际效应\n0.67 vs 非 GPTs 组 0.16（约 4 倍差异）。",
     "\\textbf{H3 验证强}: $\\hat{\\beta}_{\\mathrm{gpt}}=0.297^{**}$，GPTs 组边际效应\n0.545 vs 非 GPTs 组 0.248（约 2.2 倍差异）。"),
    # 异质性初步观察 H2/H3 数字
    ("企业内异质性} ($\\hat{\\beta}_{\\mathrm{tech}}=0.32$) 与\n(ii) \\textbf{行业异质性} ($\\hat{\\beta}_{\\mathrm{gpt}}=0.51$) \\textit{同时}显著为正，",
     "企业内异质性} ($\\hat{\\beta}_{\\mathrm{tech}}=0.378$) 与\n(ii) \\textbf{行业异质性} ($\\hat{\\beta}_{\\mathrm{gpt}}=0.297$) \\textit{同时}显著为正，"),
]

count = 0
for old, new in replacements:
    if old in s:
        s = s.replace(old, new)
        count += 1
    else:
        print(f"WARN: 找不到 old string for replacement #{count+1}")

print(f"成功应用 {count}/{len(replacements)} 处替换")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print(f"✅ sec04 更新完成")