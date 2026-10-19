"""
sim_debug2.py — PPML Newton step 精细调试
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')

import numpy as np
from sim_dgp import build_skeleton, generate_outcomes, TRUE_BETA_PPML
from sim_estimators import fast_demean, demean_matrix

df, _, _ = build_skeleton(seed=42)
df = generate_outcomes(df, seed=42)
Y = df['Y'].values.astype(np.float64)
X = df['D_cj_x_Post'].values.astype(np.float64).reshape(-1, 1)
group_specs = [('c', 't'), ('j', 't'), ('c', 'j')]

# 比较 OLS 起点 vs 真实 PPML
X_dm = demean_matrix(X, df, group_specs)
Y_dm = fast_demean(Y.copy(), df, group_specs)
from numpy.linalg import lstsq
beta_ols, *_ = lstsq(X_dm, Y_dm, rcond=None)
print(f"OLS β (起点) = {beta_ols[0]:.4f}")
print(f"真实 PPML β = {TRUE_BETA_PPML:.4f}")
print(f"差距 = {beta_ols[0] - TRUE_BETA_PPML:.4f}")

# 检查 OLS vs PPML 的关系
# 在泊松中, 处理效应 = ln(E[Y_treat]) - ln(E[Y_ctrl])
treat_mask = df['D_cj'] == 1
ctrl_mask = df['D_cj'] == 0
mean_treat = df.loc[treat_mask, 'Y'].mean()
mean_ctrl = df.loc[ctrl_mask, 'Y'].mean()
beta_direct = np.log(mean_treat / mean_ctrl)
print(f"\n直接 ln(E[Y_treat]/E[Y_ctrl]) = {beta_direct:.4f}")

# 处理组的 PPML: 只在 treat 上做
print("\n=== 朴素 PPML (无 FE, 仅截距) ===")
import statsmodels.api as sm
mask_post = df['D_cj_x_Post'] == 1
Y_post = df.loc[mask_post, 'Y'].values
Y_pre = df.loc[~mask_post, 'Y'].values
print(f"Pre-treatment  mean(Y) = {Y_pre.mean():.4f}, E[Y]=exp(μ)")
print(f"Post-treatment mean(Y) = {Y_post.mean():.4f}")
print(f"log ratio = {np.log(Y_post.mean() / Y_pre.mean()):.4f}")

# 不 damping 的 Newton-Raphson
print("\n=== Newton-Raphson 无 damping ===")
beta = np.array([0.0])
for it in range(40):
    eta = np.clip(X[:, 0] * beta[0], -15, 15)
    mu = np.maximum(np.exp(eta), 1e-8)
    resid = Y - mu
    resid_dm = fast_demean(resid, df, group_specs)
    X_dm = demean_matrix(X, df, group_specs)
    Xw = X_dm * np.sqrt(mu)[:, None]
    yw = resid_dm * np.sqrt(mu)
    step, *_ = lstsq(Xw, yw, rcond=None)
    print(f"  iter {it}: β = {beta[0]:+.4f}, step = {step[0]:+.4f}, max|step| = {np.abs(step[0]):.4f}")
    beta = beta + step
    if np.abs(step[0]) < 1e-7:
        print(f"  收敛 at iter {it}")
        break
print(f"\n最终 β = {beta[0]:.4f}")
print(f"真实 β = {TRUE_BETA_PPML:.4f}")