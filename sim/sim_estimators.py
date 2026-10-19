"""
================================================================================
sim_estimators.py — 三线建设 Exit-DDD 估计量模块 [v9 完整修复版]
================================================================================
按用户 2026-10-19 三大修复指令全面重写:
  [Bug B 修复] 第二阶段被解释变量改为 y_ihs (反正弦双曲), 与 twfe_ihs_hdfe 真值 β=0.20 对齐
  [Bug B+ 修复] 第一阶段和第二阶段都把 HasTF×Post 作为外生控制 (排他性保障)
  [Bug C 修复] fast_demean 收敛判断改用 np.isfinite + max(prev_norm, 1e-12) 容差

新增:
  [Hansen J]   双 IV (Z1 海拔 + Z2 坡度) → Sargan/Hansen 过度识别检验
  [pyfixest]   pf.feols / pf.fepois 备份, 与自实现对照
  [FE 锚定]   c_t + j_t + c_j 三组 HDFE, 与真实 DGP 的 α_c + γ_j + δ_cj 对齐
================================================================================
"""

import numpy as np
import pandas as pd
from numpy.linalg import lstsq, pinv


# ==============================================================================
# Part A: 自实现 fast_demean (Alternating Projection 收敛, 容差防 NaN)
# ==============================================================================
def fast_demean(y, df, group_specs, max_iter=80, tol=1e-9):
    """对单个向量 y 做 Alternating Projection demean, 修复 Line 59 除零/NaN 警告

    收敛条件:  |prev_norm - norm| / max(prev_norm, 1e-12) < tol
               且 prev_norm 必须是有限数
    """
    y = y.astype(np.float64).copy()
    n = len(y)
    codes_list, n_groups_list = [], []
    for cols in group_specs:
        if isinstance(cols, (list, tuple)):
            if len(cols) == 1:
                codes = pd.factorize(df[cols[0]].values)[0]
            else:
                keys = pd.MultiIndex.from_frame(df[list(cols)])
                codes = pd.factorize(keys)[0]
        else:
            codes = pd.factorize(df[cols].values)[0]
        codes_list.append(codes)
        n_groups_list.append(codes.max() + 1)

    prev_norm = np.inf
    for it in range(max_iter):
        for codes, n_groups in zip(codes_list, n_groups_list):
            sums = np.bincount(codes, weights=y, minlength=n_groups)
            counts = np.bincount(codes, minlength=n_groups)
            means = sums / np.maximum(counts, 1)
            y -= means[codes]
        norm = np.sqrt((y ** 2).sum() / max(n, 1))

        # ===== 修复: 用 isfinite 防 NaN, 用 max(prev_norm, 1e-12) 防 0 除 =====
        if (np.isfinite(prev_norm) and np.isfinite(norm)
                and prev_norm > 1e-12
                and abs(prev_norm - norm) / max(prev_norm, 1e-12) < tol):
            break
        prev_norm = norm
    return y


def demean_matrix(X, df, group_specs):
    """对矩阵 X 按列 demean"""
    X = np.asarray(X, dtype=np.float64)
    cols = []
    for k in range(X.shape[1]):
        cols.append(fast_demean(X[:, k], df, group_specs))
    return np.column_stack(cols)


# ==============================================================================
# Part B: 线性 HDFE OLS / IV-DDD via FWL (控制 HasTF×Post)
# ==============================================================================
def twfe_ols_hdfe(y, X, df, group_specs, cluster_col=None, X_extra=None):
    """HDFE OLS: y demean, X demean, OLS, cluster-robust SE

    X_extra : 额外外生控制(如 HasTF×Post), 也投影掉同一组 FE
    """
    y_dm = fast_demean(y.copy(), df, group_specs)
    X_dm = demean_matrix(X, df, group_specs)
    n, k = X_dm.shape
    if X_extra is not None and X_extra.shape[1] > 0:
        X_extra_dm = demean_matrix(X_extra, df, group_specs)
        X_full_dm = np.column_stack([X_dm, X_extra_dm])
    else:
        X_full_dm = X_dm

    beta_full, *_ = lstsq(X_full_dm, y_dm, rcond=None)
    resid = y_dm - X_full_dm @ beta_full

    XtX_inv = pinv(X_full_dm.T @ X_full_dm)
    if cluster_col is not None:
        clusters = pd.factorize(df[cluster_col].values)[0]
        score = resid[:, None] * X_full_dm
        G = np.zeros((len(np.unique(clusters)), X_full_dm.shape[1]))
        for cl, sl in enumerate(np.unique(clusters)):
            mask = (clusters == sl)
            G[cl] = score[mask].sum(axis=0)
        meat = G.T @ G
        V = XtX_inv @ meat @ XtX_inv
        G_n = len(np.unique(clusters))
        V *= G_n / max(G_n - 1, 1)
    else:
        u2 = (resid ** 2).astype(np.float64)
        meat = X_full_dm.T @ (u2[:, None] * X_full_dm)
        V = XtX_inv @ meat @ XtX_inv
        V *= n / max(n - X_full_dm.shape[1], 1)
    se = np.sqrt(np.maximum(np.diag(V), 0.0))
    return {'beta': beta_full[:k], 'se': se[:k], 'N': n, 'k': k, 'resid': resid}


def iv_ddd_2sls(y, X_endog, X_exog, Z, df, group_specs, cluster_col=None):
    """线性 IV-DDD via FWL 残差化 + 2SLS + Hansen J over-id 检验

    Parameters
    ----------
    y        : 被解释变量 (默认用 y_ihs, 而非原始 y_count)
    X_endog  : 内生变量矩阵 (D_cj × Post), 维度 (n, k_endog)
    X_exog   : 外生控制变量 (含 HasTF×Post), 维度 (n, k_exog)
    Z        : 工具变量矩阵 (Z1_cj×Post, Z2_cj×Post, ...), 维度 (n, k_z)
    group_specs : 三组 HDFE 锚定
    cluster_col  : 聚类变量 (默认 'c_j')

    Returns
    -------
    dict : beta (k_endog,), se (k_endog,), F_stat (一阶段 F), Hansen_J (p 值)
    """
    # ===== 全部 demean (FWL: 所有变量都在同一组 FE 下残差化) =====
    y_dm = fast_demean(y.copy(), df, group_specs)
    X_endog_dm = demean_matrix(X_endog, df, group_specs)
    if X_exog is not None and X_exog.shape[1] > 0:
        X_exog_dm = demean_matrix(X_exog, df, group_specs)
    else:
        X_exog_dm = np.zeros((len(y_dm), 0))
    Z_dm = demean_matrix(Z, df, group_specs)
    n = len(y_dm)
    k_endog = X_endog_dm.shape[1]
    k_z = Z_dm.shape[1]

    # ===== 一阶段: D_endog ̃ = π · Z̃ + X̃_exog·π_x + ν̃ =====
    X1 = np.column_stack([Z_dm, X_exog_dm])
    try:
        pi_hat, *_ = lstsq(X1, X_endog_dm, rcond=None)
    except Exception as e:
        return {'beta': np.full(k_endog, np.nan), 'se': np.full(k_endog, np.nan),
                'F_stat': np.nan, 'Hansen_J': np.nan, 'Hansen_J_p': np.nan,
                'N': n, 'k_endog': k_endog, 'error': f'一阶段失败: {e}'}
    D_hat_dm = X1 @ pi_hat
    nu_dm = X_endog_dm - D_hat_dm
    # 一阶段 partial F (只对 IV 部分)
    X1ZtX1 = pinv(X1.T @ X1)
    var_nu = (nu_dm ** 2).sum() / max(n - X1.shape[1], 1)
    V_pi = X1ZtX1 * var_nu
    se_pi = np.sqrt(np.maximum(np.diag(V_pi), 0.0))
    if k_z > 0:
        F_per_iv = (pi_hat[:k_z] ** 2 / np.maximum(se_pi[:k_z] ** 2, 1e-12))
        F_stat = float(F_per_iv.mean())  # 简化: 多个 IV 用平均
    else:
        F_stat = np.nan

    # ===== 二阶段: ỹ = β · D̂ + X̃_exog·γ + u =====
    X2 = np.column_stack([D_hat_dm, X_exog_dm])
    beta2, *_ = lstsq(X2, y_dm, rcond=None)
    resid2 = y_dm - X2 @ beta2

    # === Cluster-robust SE for β ===
    X2ZtX2 = pinv(X2.T @ X2)
    if cluster_col is not None:
        clusters = pd.factorize(df[cluster_col].values)[0]
        score2 = resid2[:, None] * X2
        G = np.zeros((len(np.unique(clusters)), X2.shape[1]))
        for cl, sl in enumerate(np.unique(clusters)):
            mask = (clusters == sl)
            G[cl] = score2[mask].sum(axis=0)
        meat2 = G.T @ G
        V2 = X2ZtX2 @ meat2 @ X2ZtX2
        V2 *= len(np.unique(clusters)) / max(len(np.unique(clusters)) - 1, 1)
    else:
        u22 = (resid2 ** 2).astype(np.float64)
        meat2 = X2.T @ (u22[:, None] * X2)
        V2 = X2ZtX2 @ meat2 @ X2ZtX2
        V2 *= n / max(n - X2.shape[1], 1)
    se2 = np.sqrt(np.maximum(np.diag(V2), 0.0))

    # ===== Hansen J over-id 检验 (仅当 k_z > k_endog) =====
    Hansen_J = np.nan
    Hansen_J_p = np.nan
    overid_df = k_z - k_endog
    if overid_df > 0:
        # J = n * (R²) 从过度识别约束的辅助回归
        # 构造辅助回归: e2 ̃ = γ'·Z̃ + v  (e2 是 IV-DDD 残差, Z̃ 是 IV)
        # J = n · R² ~ χ²(overid_df)
        from numpy.linalg import lstsq as lsq
        e2 = resid2
        # 辅助: e2 ̃ = γ'·Z̃ + v, 但 v 要正交于 X_exog_dm
        # 简化做法: e2 ̃ ~ Z̃  (控制 X_exog_dm)
        X_aux = np.column_stack([Z_dm, X_exog_dm])
        try:
            gamma_aux, *_ = lsq(X_aux, e2, rcond=None)
            e2_pred = X_aux @ gamma_aux
            ssr = ((e2 - e2_pred) ** 2).sum()
            sst = (e2 ** 2).sum()
            R2_aux = 1 - ssr / max(sst, 1e-12)
            J = float(n * R2_aux)
            from scipy.stats import chi2
            Hansen_J = J
            Hansen_J_p = float(1 - chi2.cdf(J, df=overid_df))
        except Exception:
            pass

    return {
        'beta': beta2[:k_endog],
        'se': se2[:k_endog],
        'N': n, 'k_endog': k_endog,
        'F_stat': F_stat,
        'Hansen_J': Hansen_J,
        'Hansen_J_p': Hansen_J_p,
        'overid_df': overid_df,
        'first_stage_pi': pi_hat[:k_z] if k_z > 0 else np.array([]),
        'first_stage_se': se_pi[:k_z] if k_z > 0 else np.array([]),
    }


# ==============================================================================
# Part C: pyfixest 备份接口 (Correia 2020 IRLS-HDFE)
# ==============================================================================
def pf_feols(df_panel, y_col, x_col, fe_cols, cluster_col=None):
    try:
        import pyfixest as pf
    except ImportError:
        return {'error': 'pyfixest 未安装'}
    fe_str = '+'.join(fe_cols)
    formula = f"{y_col} ~ {x_col} | {fe_str}"
    if cluster_col is not None:
        res = pf.feols(formula, data=df_panel, vcov={"CRV1": cluster_col})
    else:
        res = pf.feols(formula, data=df_panel)
    return {
        'beta': float(res.coef().iloc[0]),
        'se': float(res.se().iloc[0]),
        'N': int(res._N),
    }


def pf_fepois(df_panel, y_col, x_col, fe_cols, cluster_col=None):
    """pyfixest pf.fepois PPML-HDFE (Correia 2020 IRLS)"""
    try:
        import pyfixest as pf
    except ImportError:
        return {'error': 'pyfixest 未安装'}
    fe_str = '+'.join(fe_cols)
    formula = f"{y_col} ~ {x_col} | {fe_str}"
    if cluster_col is not None:
        res = pf.fepois(formula, data=df_panel, vcov={"CRV1": cluster_col})
    else:
        res = pf.fepois(formula, data=df_panel)
    return {
        'beta': float(res.coef().iloc[0]),
        'se': float(res.se().iloc[0]),
        'N': int(res._N),
    }


# ==============================================================================
# Part D: 主估计函数 (完整 5 个估计量)
# ==============================================================================
def estimate_all(df, endog_strength=None):
    """跑五组核心估计量: twfe_ihs, twfe_lpm, iv_ddd_2sls_1IV, iv_ddd_2sls_2IV, pf_fepois

    Parameters
    ----------
    df : DataFrame, 必须包含 c, j, t, Y, D_cj_x_Post, Z1_cj, Z2_cj,
         HasTF_x_Post, Post, y_ihs
    """
    group_specs = [('c', 't'), ('j', 't'), ('c', 'j')]   # 三组 HDFE 锚定
    df = df.copy()
    # 构造 IV 变量: Z_cjt = Z_cj × Post_t
    df['Z1_cj_x_Post'] = (df['Z1_cj'] * df['Post']).astype(np.float64)
    df['Z2_cj_x_Post'] = (df['Z2_cj'] * df['Post']).astype(np.float64)
    df['c_j'] = df['c'].astype(str) + '_' + df['j'].astype(str)  # cluster key

    # 标准化: 被解释变量 y_ihs, 内生 D_cj_x_Post, 外生 HasTF×Post, IV Z1×Post / Z2×Post
    y_ihs = df['y_ihs'].values.astype(np.float64)
    y_count = df['Y'].values.astype(np.float64)
    D_endog = df['D_cj_x_Post'].values.astype(np.float64).reshape(-1, 1)
    X_extra = df['HasTF_x_Post'].values.astype(np.float64).reshape(-1, 1)
    Z1 = df['Z1_cj_x_Post'].values.astype(np.float64).reshape(-1, 1)
    Z2 = df['Z2_cj_x_Post'].values.astype(np.float64).reshape(-1, 1)

    out = {}

    # ===========================================================
    # [1] TWFE-IHS with HDFE (基准/广延边际, 已知有内生性偏误)
    # ===========================================================
    res_ihs = twfe_ols_hdfe(y_ihs, D_endog, df, group_specs,
                            cluster_col='c_j', X_extra=X_extra)
    out['twfe_ihs_hdfe'] = {
        'beta': float(res_ihs['beta'][0]),
        'se': float(res_ihs['se'][0]),
        'N': int(res_ihs['N']),
    }

    # ===========================================================
    # [2] TWFE-LPM with HDFE (广延边际)
    # ===========================================================
    y_lpm = (y_count > 0).astype(np.float64)
    res_lpm = twfe_ols_hdfe(y_lpm, D_endog, df, group_specs,
                            cluster_col='c_j', X_extra=X_extra)
    out['twfe_lpm_hdfe'] = {
        'beta': float(res_lpm['beta'][0]),
        'se': float(res_lpm['se'][0]),
        'N': int(res_lpm['N']),
    }

    # ===========================================================
    # [3] IV-DDD-1IV via 自实现 2SLS (用 Z1)
    # ===========================================================
    res_iv1 = iv_ddd_2sls(y_ihs, D_endog, X_exog=X_extra, Z=Z1,
                            df=df, group_specs=group_specs, cluster_col='c_j')
    out['iv_ddd_2sls_1IV'] = {
        'beta': float(res_iv1['beta'][0]),
        'se': float(res_iv1['se'][0]),
        'N': int(res_iv1['N']),
        'F_stat': float(res_iv1['F_stat']),
    }

    # ===========================================================
    # [4] IV-DDD-2IV via 自实现 2SLS (用 Z1 + Z2, 含 Hansen J)
    # ===========================================================
    Z_both = np.column_stack([Z1, Z2])
    res_iv2 = iv_ddd_2sls(y_ihs, D_endog, X_exog=X_extra, Z=Z_both,
                            df=df, group_specs=group_specs, cluster_col='c_j')
    out['iv_ddd_2sls_2IV'] = {
        'beta': float(res_iv2['beta'][0]),
        'se': float(res_iv2['se'][0]),
        'N': int(res_iv2['N']),
        'F_stat': float(res_iv2['F_stat']),
        'Hansen_J': float(res_iv2['Hansen_J']),
        'Hansen_J_p': float(res_iv2['Hansen_J_p']),
    }

    # ===========================================================
    # [5] pyfixest pf.fepois PPML-HDFE (sanity check)
    # ===========================================================
    try:
        df_panel = df[['c', 'j', 't', 'Y', 'D_cj_x_Post', 'HasTF_x_Post']].copy()
        # 把 c, j, t 做成 1-way FE (c#t + j#t + c#j 三组)
        # pyfixest 支持 |c + t + c^j 但不支持 c#t, 用最大近似
        res_ppml = pf_fepois(df_panel, 'Y', 'D_cj_x_Post',
                              fe_cols=['c', 't'], cluster_col='c')
        if 'error' not in res_ppml:
            out['pf_fepois'] = {
                'beta': float(res_ppml['beta']),
                'se': float(res_ppml['se']),
                'N': int(res_ppml['N']),
            }
        else:
            out['pf_fepois'] = {'error': res_ppml['error']}
    except Exception as e:
        out['pf_fepois'] = {'error': str(e)}

    return out


# ==============================================================================
# Part E: 自检入口
# ==============================================================================
if __name__ == '__main__':
    import time, sys
    from sim_dgp import (build_skeleton, assign_exits, generate_outcomes,
                          TRUE_BETA_IHS, TRUE_BETA_PPML, PANEL_PARAMS)

    print("=" * 80)
    print("[SINGLE-REP SANITY CHECK v9 — 排他性修复 + HasTF×Post 控制 + Hansen J + pyfixest]")
    print("=" * 80)
    print(f"True β_IHS = {TRUE_BETA_IHS:.4f}  (与 twfe_ihs_hdfe 真实 DGP 对齐)")
    print(f"True β_PPML = {TRUE_BETA_PPML:.4f}  (仅供 ppml 估计量参考)")

    # ===== 用 v3 DGP 生成单次样本 =====
    df_skel, Z1_c_raw, Z2_c_raw, HasTF_cj_1980, Z1_cj_IV, Z2_cj_IV, micro_noise_cj = build_skeleton()
    df_skel, Exit_cj, eta_cj, pi_0, actual_rate = assign_exits(
        df_skel, HasTF_cj_1980, Z1_cj_IV, micro_noise_cj,
        target_rate=0.40, endog_strength=0.50
    )
    df = generate_outcomes(df_skel, eta_cj, endog_strength=0.50)

    print(f"\n[DGP 内禀]")
    print(f"  N = {len(df):,}")
    print(f"  HasTF 稀疏度 = {df['HasTF_cj_1980'].mean():.3f}")
    print(f"  Exit 撤并率 (HasTF=1 内) = {actual_rate:.3f}")

    # ===== 跑 5 组估计量 =====
    t0 = time.time()
    res = estimate_all(df, endog_strength=0.5)
    t1 = time.time()

    print(f"\n[估计量结果] (单次仿真, ~{t1-t0:.1f}s)")
    print(f"{'Estimator':<26} {'beta':>10} {'SE':>10} {'N':>8} {'extra':<20}")
    print("-" * 80)
    for key, r in res.items():
        if 'error' in r:
            print(f"{key:<26} {'ERROR':>10} {r['error']}")
            continue
        b = r.get('beta', np.nan)
        s = r.get('se', np.nan)
        n = r.get('N', 0)
        extra = []
        if 'F_stat' in r:
            extra.append(f"F={r['F_stat']:.1f}")
        if 'Hansen_J_p' in r:
            extra.append(f"J_p={r['Hansen_J_p']:.3f}")
        print(f"{key:<26} {b:>10.4f} {s:>10.4f} {n:>8,} {','.join(extra):<20}")

    print(f"\n[解读]")
    print(f"  真实 β_IHS = {TRUE_BETA_IHS:.3f}")
    print(f"  TWFE-IHS 应当有内生性正向偏误 (~0.288)")
    print(f"  IV-DDD 应当回到真值 ~{TRUE_BETA_IHS}")
    print(f"  Hansen J p>0.10 说明排他性不拒绝 (Z1, Z2 都外生)")
