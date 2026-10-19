"""
================================================================================
B6_event_study.py [Round 10] — 顶刊级 Event Study 平行趋势图
================================================================================
提取相对搬迁年份 k ∈ [-6, +12] 的动态交互项系数 theta_k 及其 95% 置信区间:
  k ∈ [-6, -2] 事前 (pre): 系数围绕 0 平缓波动且 95% CI 包含 0
  k = -1  基期 (1985): 空心圆 (omitted reference period)
  k ∈ [0, +12] 事后 (post): 1986 年撤并启动后系数稳步攀升并显著大于 0

模型: y_cjt = Sum_{k != -1} theta_k * 1{t - 1986 = k} * HasTF_cj + FE + eps_cjt
聚类: c_j 双维聚类 (county_id x industry2)
输出: F:\\三线建设\\paper\\figures\\fig1_event_study.pdf
"""
import sys
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 非交互 backend
import matplotlib.pyplot as plt
from matplotlib import rcParams
from numpy.linalg import lstsq, pinv

# 直接 import sim_estimators 的 fast_demean
sys.path.insert(0, str(Path(r"F:\三线建设\sim")))
from sim_estimators import fast_demean, demean_matrix

# ===== 路径 =====
BASE = Path(r"F:\三线建设\data_pipeline")
PAPER = Path(r"F:\三线建设\paper")
FIG_DIR = PAPER / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DTA = BASE / "reg_sample.dta"

# ===== 全局 matplotlib 设置 (顶刊学术风) =====
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['SimSun', 'Songti SC', 'Times New Roman']
rcParams['font.size'] = 10
rcParams['axes.unicode_minus'] = False
rcParams['axes.linewidth'] = 0.8
rcParams['xtick.major.width'] = 0.8
rcParams['ytick.major.width'] = 0.8
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']

print("="*70)
print("Event Study 平行趋势图生成 [Round 10]")
print("="*70)

# ===== 加载数据 =====
df = pd.read_stata(DTA)
df["c_j"] = df["county_id"].astype(str) + "_" + df["industry2"].astype(str)
print(f"加载 {len(df):,} 行")

# 政策时间: 1986 (Post_year), 基期 k=-1 即 1985
POST_YEAR = 1986  # 1986 年撤并启动
BASE_YEAR = 1985  # k = -1 基期 (omitted)
df["rel_year"] = df["year"] - POST_YEAR  # k = t - 1986
# k=0  -> 1986 (撤并启动)
# k=-1 -> 1985 (基期, omitted)
# k=+12 -> 1998

df_treated = df[df["HasTF_cj_1980"] == 1].copy()
print(f"HasTF=1 格子数: {df_treated.groupby(['county_id','industry2']).ngroups}")

# ===== 取 k ∈ [-6, +12] = 19 个窗口 =====
K_MIN, K_MAX = -6, 12
all_ks = list(range(K_MIN, K_MAX + 1))
event_ks = [k for k in all_ks if k != -1]
print(f"事件研究窗口 k ∈ [{K_MIN}, {K_MAX}], 共 {len(event_ks)} 个非基期 (omitted k=-1)")

# ===== 生成事件研究交互项 =====
for k in event_ks:
    df[f"D_k{k}"] = ((df["rel_year"] == k) & (df["HasTF_cj_1980"] == 1)).astype(np.int8)

y = df["y_ihs"].values.astype(np.float64)
group_specs = [["county_id", "year"], ["industry2", "year"], ["county_id", "industry2"]]
y_dm = fast_demean(y.copy(), df, group_specs)

# 自变量: 19 个事件研究 D_k + Post 期 dummy (吸收 common shock)
# 注意: 不能放 HasTF×Post 控制, 它与 sum D_k_k 共线 (sum_k D_k_k = HasTF×Post)
X_list = []
for k in event_ks:
    X_list.append(demean_matrix(df[f"D_k{k}"].values.astype(np.float64).reshape(-1, 1),
                                  df, group_specs))
# Post dummy 控制 (吸收 Post 期 common shock, 不与 D_k_k 共线)
X_list.append(demean_matrix(df["Post"].values.astype(np.float64).reshape(-1, 1),
                              df, group_specs))
X = np.column_stack(X_list)
K = X.shape[1]
print(f"X 维度: {X.shape} (19 个事件期 D_k + 1 个 HasTF×Post 控制)")

# ===== OLS 估计 =====
beta, *_ = lstsq(X, y_dm, rcond=None)
resid = y_dm - X @ beta
theta_k = beta[:len(event_ks)]

# ===== c_j 双维聚类稳健 SE =====
clusters = pd.factorize(df["c_j"])[0]
G = len(np.unique(clusters))
score = resid[:, None] * X
sum_G = np.zeros((G, K))
for cl in range(G):
    mask = (clusters == cl)
    sum_G[cl] = score[mask].sum(axis=0)
meat = sum_G.T @ sum_G
XtX_inv = pinv(X.T @ X)
V = XtX_inv @ meat @ XtX_inv * (G / max(G - 1, 1))
se = np.sqrt(np.maximum(np.diag(V), 0.0))
se_k = se[:len(event_ks)]

print(f"\n聚类数: {G}, 总样本: {len(df):,}")

# ===== 打印 theta_k 及其 95% CI =====
print(f"\n{'k':>4s} {'年份':>5s} {'theta_k':>9s} {'se':>8s} {'t':>6s} {'95% CI':>16s} {'显著':>5s}")
theta_dict = {}
for i, k in enumerate(event_ks):
    t = theta_k[i] / se_k[i] if se_k[i] > 0 else 0
    ci_lo = theta_k[i] - 1.96 * se_k[i]
    ci_hi = theta_k[i] + 1.96 * se_k[i]
    sig = "***" if abs(t) > 2.576 else ("**" if abs(t) > 1.96 else ("*" if abs(t) > 1.645 else ""))
    print(f"{k:>4d} {1986+k:>5d} {theta_k[i]:>9.4f} {se_k[i]:>8.4f} {t:>6.2f} "
          f"[{ci_lo:>6.3f},{ci_hi:>6.3f}] {sig:>5s}")
    theta_dict[str(k)] = {"year": int(1986 + k), "theta": float(theta_k[i]),
                          "se": float(se_k[i]), "ci_lo": float(ci_lo),
                          "ci_hi": float(ci_hi), "t": float(t)}

# ===== 画图 =====
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)

plot_ks = all_ks
plot_theta = []
plot_se = []
plot_ci_lo = []
plot_ci_hi = []
for k in plot_ks:
    if k == -1:
        plot_theta.append(0.0)
        plot_se.append(0.0)
        plot_ci_lo.append(0.0)
        plot_ci_hi.append(0.0)
    else:
        idx = event_ks.index(k)
        plot_theta.append(theta_k[idx])
        plot_se.append(se_k[idx])
        plot_ci_lo.append(theta_k[idx] - 1.96 * se_k[idx])
        plot_ci_hi.append(theta_k[idx] + 1.96 * se_k[idx])

plot_theta = np.array(plot_theta)
plot_ci_lo = np.array(plot_ci_lo)
plot_ci_hi = np.array(plot_ci_hi)

# 95% CI 阴影
ax.fill_between(plot_ks, plot_ci_lo, plot_ci_hi,
                 color='#2166AC', alpha=0.20, linewidth=0, label='95% CI')
# 0 参考线
ax.axhline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.7)
# 政策分界 (k=0 即 1986 年, 分界在 k=-0.5 处)
ax.axvline(-0.5, color='#B2182B', linewidth=1.2, linestyle='--', alpha=0.8)
# 主曲线
ax.plot(plot_ks, plot_theta, color='#2166AC', linewidth=1.6,
        marker='o', markersize=5, markerfacecolor='#2166AC',
        markeredgecolor='white', markeredgewidth=0.8,
        label=r'$\hat{\theta}_k$ (point estimate)')

# k=-1 基期空心圆
ax.scatter([-1], [0], s=70, facecolors='white', edgecolors='#2166AC',
           linewidths=1.6, zorder=5, label='Base year (k=-1, 1985)')

# 标注事前/事后区域
ax.axvspan(K_MIN, -0.5, alpha=0.06, color='gray', zorder=0)
ax.axvspan(-0.5, K_MAX, alpha=0.06, color='#B2182B', zorder=0)
ax.text(-4.5, max(plot_theta) * 0.92, 'Pre-policy\n(事前)', ha='center', va='top',
        fontsize=8.5, color='gray', style='italic')
ax.text(5.5, max(plot_theta) * 0.92, 'Post-policy\n(事后)', ha='center', va='top',
        fontsize=8.5, color='#B2182B', style='italic')

# 轴
ax.set_xlabel(r'相对年份 $k = t - 1986$ (1985 为基期 $k=-1$)', fontsize=10.5)
ax.set_ylabel(r'动态处理效应 $\hat{\theta}_k$ (IHS)', fontsize=10.5)
ax.set_xticks(plot_ks)
ax.set_xticklabels([str(k) for k in plot_ks], rotation=0, fontsize=8.5)
ax.set_xlim(K_MIN - 0.5, K_MAX + 0.5)
ax.set_ylim(min(plot_ci_lo) - 0.05, max(plot_ci_hi) + 0.10)
ax.grid(True, axis='y', linestyle=':', linewidth=0.5, alpha=0.5)
ax.legend(loc='upper left', frameon=True, fontsize=8.5, framealpha=0.9)

# 标题
ax.set_title('Event Study: 1986 nian san xian jian she tiao zhe che bing de dong tai xiao ying'.replace(
    '1986 nian san xian jian she tiao zhe che bing de dong tai xiao ying',
    'Event Study: 1986 nian'),
    fontsize=11, fontweight='bold', pad=8)

ax.text(0.99, 0.02, f'N = {len(df):,}, G = {G} clusters',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=7.5, color='gray', style='italic')

plt.tight_layout()
fig_path = FIG_DIR / "fig1_event_study.pdf"
plt.savefig(fig_path, format='pdf', bbox_inches='tight', dpi=300)
plt.savefig(FIG_DIR / "fig1_event_study.png", format='png', bbox_inches='tight', dpi=200)
plt.close()
print(f"\n✅ 写出 {fig_path}")
print(f"✅ 写出 {FIG_DIR / 'fig1_event_study.png'}")

# ===== 写出 JSON 摘要 =====
summary = {
    "model": "Event Study with HDFE",
    "N_total": int(len(df)),
    "N_treated_groups": int(df[df['HasTF_cj_1980']==1].groupby(['county_id','industry2']).ngroups),
    "G_clusters_cj": int(G),
    "k_min": K_MIN,
    "k_max": K_MAX,
    "base_year": BASE_YEAR,
    "post_year": POST_YEAR,
    "base_k": -1,
    "omitted_base": True,
    "controls": ["Post_t (common shock absorbed)"],
    "fe": ["(county_id, year)", "(industry2, year)", "(county_id, industry2)"],
    "cluster": "county_id x industry2",
    "theta": theta_dict,
}
with open(FIG_DIR / "fig1_event_study.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"✅ 写出 {FIG_DIR / 'fig1_event_study.json'}")

# ===== 关键判定 =====
pre_ks = [k for k in range(-6, -1) if str(k) in theta_dict]
all_pre_zero = all(abs(theta_dict[str(k)]["t"]) < 1.96 for k in pre_ks)
print(f"\n事前平行趋势检验 (k ∈ [-6,-2] 全部 |t|<1.96): {all_pre_zero}")
if all_pre_zero:
    print("✅ 事前系数均不显著, 平行趋势假设成立")
else:
    print(f"⚠ 部分事前系数显著: {[(k, theta_dict[str(k)]['t']) for k in pre_ks if abs(theta_dict[str(k)]['t']) >= 1.96]}")

post_ks = [k for k in range(0, 13) if str(k) in theta_dict]
post_signif = [k for k in post_ks if abs(theta_dict[str(k)]["t"]) > 1.96]
print(f"事后显著期数: {len(post_signif)} / 13 (k ∈ [0,12])")
print(f"事后显著期: {post_signif}")
