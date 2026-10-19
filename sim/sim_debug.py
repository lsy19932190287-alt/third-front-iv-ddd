"""
sim_debug.py — 调试 PPML demean 算法
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
from sim_dgp import build_skeleton, generate_outcomes, TRUE_BETA_PPML
from sim_estimators import fast_demean, demean_matrix, twfe_ols, ppml_hdfe

df, _, _ = build_skeleton(seed=42)
df = generate_outcomes(df, seed=42)

# === Test 1: demean 后 X = D_cj × Post 还有多少变异? ===
group_specs = [('c', 't'), ('j', 't'), ('c', 'j')]
X = df['D_cj_x_Post'].values.astype(np.float64).reshape(-1, 1)
X_dm = demean_matrix(X, df, group_specs)

print(f"X demean before std = {X.std():.4f},  mean = {X.mean():.4f}")
print(f"X demean after  std = {X_dm[:,0].std():.6f}")
print(f"X demean after  abs max = {np.abs(X_dm[:,0]).max():.6f}")
print(f"X demean after  ||X||^2 = {(X_dm**2).sum():.2f}")
print(f"X demean after  ||X_dm||^2 / ||X||^2 = {(X_dm**2).sum() / (X**2).sum():.4f}")

# === Test 2: demean 后 Y 还有多少变异? ===
Y = df['Y'].values.astype(np.float64)
Y_dm = fast_demean(Y.copy(), df, group_specs)
print(f"\nY demean before std = {Y.std():.4f}")
print(f"Y demean after  std = {Y_dm.std():.4f}")

# === Test 3: demean 后 X × Y 的相关性 ===
print(f"\ndemean after X*Y correlation = {np.corrcoef(X_dm[:,0], Y_dm)[0,1]:.4f}")

# === Test 4: OLS 测试 ===
from numpy.linalg import lstsq
beta_ols, *_ = lstsq(X_dm, Y_dm, rcond=None)
print(f"\nOLS β̂ = {beta_ols[0]:.4f}  (真实 PPML β = {TRUE_BETA_PPML:.4f})")

# === Test 5: PPML verbose 模式 ===
print("\n=== PPML Verbose ===")
X = X.astype(np.float64)
beta = np.zeros(1)
max_iter = 30
for it in range(max_iter):
    eta = np.clip(X @ beta, -10, 10)
    mu = np.exp(eta)
    with np.errstate(divide='ignore', invalid='ignore'):
        z = np.where(mu > 1e-12, (Y - mu) / mu, 0.0) + eta
    w = mu.copy()
    z_dm = fast_demean(z, df, group_specs)
    X_dm2 = demean_matrix(X, df, group_specs)
    Xw = X_dm2 * w[:, None]
    yw = z_dm * w
    beta_new, *_ = lstsq(Xw, yw, rcond=None)
    print(f"  iter {it}: eta_max={np.abs(eta).max():.3f}, mu_range=[{mu.min():.3f},{mu.max():.3f}], beta={beta_new[0]:.4f}")
    if np.max(np.abs(beta_new - beta)) < 1e-7:
        beta = beta_new
        print(f"  → 收敛 at iter {it}, β={beta[0]:.4f}")
        break
    beta = beta_new
print(f"\n最终 β = {beta[0]:.4f}, 真实 = {TRUE_BETA_PPML:.4f}, 偏差 = {(beta[0]-TRUE_BETA_PPML)/TRUE_BETA_PPML*100:.1f}%")