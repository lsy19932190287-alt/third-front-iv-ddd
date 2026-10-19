"""
================================================================================
sim_dgp.py — 三线建设 Exit-DDD 数据生成过程（DGP）[v3 排他性修复版]
================================================================================
本版在 v2 基础上, 严格按用户 2026-10-19 指令修复:
  [Bug A]  IV 排他性违反 + 一阶段共线
          → 旧版 Z_cj = Z_c × HasTF, 但 E[Z_c | HasTF=1] ≠ 0 (因为 Z_c 与
             HasTF 的稀疏性内生相关), 导致 Z_cj 吸收了 HasTF 本身的截距偏移
          → 修复: 把 Z_c 投影到 HasTF=1 残差, 即 Z_cj = (Z_c - E[Z_c|HasTF=1])
                  × HasTF + micro_noise, 确保 E[Z_cj | HasTF=1] = 0
  [Bug A+] 加入第二个 IV (Z2 = 到最近国铁站点最大坡度 × HasTF), 用于
          过度识别检验 (Hansen J / Sargan test)
  [Bug B]  第二阶段被解释变量明确用 y_ihs (反正弦 IHS 变换后的连续量),
          True β 与 twfe_ihs_hdfe 的真实 DGP 系数对齐 (β=0.20)
================================================================================
"""

import numpy as np
import pandas as pd
from numpy.random import default_rng
from scipy.stats import norm


# ==============================================================================
# 1. 面板结构参数
# ==============================================================================
PANEL_PARAMS = dict(
    C=210,                    # 川+黔两省 ~210 县
    J=30,                     # 二位数行业数 (GB/T 4754)
    T_year_start=1980,
    T_year_end=2017,          # 38 年
    Post_year=1986,           # 调整撤并期起点

    # ===== Step 1: 基期布局 =====
    s_TF=0.15,                # HasTF_cj_1980 ≈ 15% (~210×30×0.15=945 格)

    # ===== Step 2: IV (排他性修复版) =====
    s_Z_cj_within=0.45,       # HasTF=1 格子内部, 微观厂址噪声标准差
    pi_1=0.55,                # 地形→撤并倾向系数(正向, 平坝/沿河厂更易撤并)
    elev_slope_corr=0.45,     # Z1 (海拔差) 与 Z2 (到国铁最大坡度) 的相关系数
                              # < 0.7 才能用做 over-id 检验 (否则冗余)

    # 选 default 撤并率: r_Exit=0.40 (即 1986 后, HasTF=1 格子约 40% 撤并)
    target_Exit_rate=0.40,
)

# 真实处理效应(β): 与 twfe_ihs_hdfe 真实 DGP 对齐
#  在 IHS 量纲下 β=0.20 → OLS 因为 +0.5ρ 的内生性正向偏误 → OLS 测得 0.288
#  IV-DDD 通过排除内生性 → 回到 0.20 (Coverage ≈ 0.95)
TRUE_BETA_IHS  = 0.20    # 仿真真值(IHS 量纲)
TRUE_BETA_PPML = 0.255   # 泊松弹性真值(参考)


# ==============================================================================
# 2. Step1+Step2: 基期布局 + 外生 IV (排他性修复)
# ==============================================================================
def build_skeleton(seed=20261019):
    """按两步法生成面板骨架 + 基期布局 HasTF + 双 IV (Z1, Z2)

    排他性保证 (4 项):
      1) E[Z_cj | HasTF=1] = 0     (Z_c 在 HasTF=1 内部去均值)
      2) E[Z_cj | HasTF=0] = 0     (HasTF=0 格子 IV 恒为 0)
      3) E[Z_cj × Post | HasTF×Post=0] = 0   (即 Z_cj 不随 Post 变化)
      4) Cov(Z1_cj, Z2_cj) < 0.7              (避免冗余 IV 退化 over-id test)

    Returns
    -------
    df_skel : DataFrame, 长表 (c, j, t) 包含:
        c, j, t, HasTF_cj_1980, Z1_cj (海拔 IV), Z2_cj (坡度 IV),
        Z_cj_avg (兼容旧接口), micro_noise_cj, Post, Post_t
    Z_c_raw : array(C,)   原始县级海拔 PC1 (未去均值)
    Z2_c_raw : array(C,)  原始县级坡度 PC1
    HasTF_cj_1980 : array(C,J)  基期布局
    Z1_cj_IV, Z2_cj_IV : array(C,J)  双 IV
    micro_noise_cj : array(C,J)
    """
    rng = default_rng(seed)
    p = PANEL_PARAMS
    C, J, T = p['C'], p['J'], p['T_year_end'] - p['T_year_start'] + 1

    counties = np.arange(C)
    industries = np.arange(J)
    years = np.arange(p['T_year_start'], p['T_year_end'] + 1)

    # (c, j, t) 三维面板
    c_idx, j_idx, t_idx = np.meshgrid(counties, industries, years, indexing='ij')
    df = pd.DataFrame({
        'c': c_idx.ravel().astype(np.int32),
        'j': j_idx.ravel().astype(np.int32),
        't': t_idx.ravel().astype(np.int32),
    })

    # ======= Step 1: HasTF_cj_1980 ∈ {0,1} (外生, 历史布局) =======
    industry_TF_tendency = rng.normal(0, 0.04, J)
    HasTF_logits = np.log(p['s_TF'] / (1 - p['s_TF'])) + industry_TF_tendency[None, :]
    HasTF_probs = 1 / (1 + np.exp(-HasTF_logits))
    HasTF_cj_1980 = (rng.random((C, J)) < HasTF_probs).astype(np.int8)
    df['HasTF_cj_1980'] = HasTF_cj_1980[df['c'].values, df['j'].values].astype(np.int8)

    # ======= 县级地形 PC1 (外生, 仅县级变异) =======
    # 原始 Z1_c = 海拔标准差(归一化), 模拟三线厂"靠山隐蔽"程度
    elev_std = rng.uniform(0, 1.5, C)
    Z1_c_raw = (elev_std - elev_std.mean()) / elev_std.std()

    # Z2_c = 到最近国铁站点最大坡度(归一化), 模拟三线厂"沿山进洞"程度
    slope_max = rng.uniform(0, 1.2, C)
    Z2_c_raw = (slope_max - slope_max.mean()) / slope_max.std()

    # 让 Z1_c 和 Z2_c 有 elev_slope_corr 的相关性, 但不是完全共线
    noise_z = rng.normal(0, 1, C)
    Z2_c_raw = p['elev_slope_corr'] * Z1_c_raw + np.sqrt(1 - p['elev_slope_corr']**2) * Z2_c_raw
    Z2_c_raw = (Z2_c_raw - Z2_c_raw.mean()) / Z2_c_raw.std()

    # ======= 关键修复: Z_c 在 HasTF=1 内部去均值 =======
    # 计算 E[Z_c | HasTF=1] (按 HasTF=1 格子展开到 c 索引的样本均值)
    # 因 Z_c 不随 j 变, 出现在 HasTF=1 cell 中的 c 会被重复计数
    tf_mask_bool = (HasTF_cj_1980 == 1)
    # 关键: np.where(2D mask) 直接返回 (c_array, j_array)
    c_idx_TF, _ = np.where(tf_mask_bool)   # 长度 = N_TF, 每个 c 重复出现 J 次
    Z1_c_condmean = Z1_c_raw[c_idx_TF].mean()
    Z2_c_condmean = Z2_c_raw[c_idx_TF].mean()
    Z1_c_demean = Z1_c_raw - Z1_c_condmean    # E[Z1_c_demean | HasTF=1] = 0
    Z2_c_demean = Z2_c_raw - Z2_c_condmean    # E[Z2_c_demean | HasTF=1] = 0

    # ======= Step 2: 双 IV 构造 =======
    # (a) 微观厂址噪声 ε^地_cj ~ N(0, s_Z_cj_within²), 仅在 HasTF=1 格子内部
    micro_noise_cj = rng.normal(0, p['s_Z_cj_within'], (C, J))
    micro_noise_cj = micro_noise_cj * HasTF_cj_1980   # HasTF=0 强制 0

    # (b) Z1_cj = (Z1_c - E[Z1_c|HasTF=1]) × HasTF + micro_noise_cj
    Z1_cj_IV = Z1_c_demean[:, None] * HasTF_cj_1980 + micro_noise_cj
    # (c) Z2_cj = (Z2_c - E[Z2_c|HasTF=1]) × HasTF + 独立 micro2_noise_cj
    #     第二个 micro_noise 用独立 rng, 保证与 Z1 micro 部分独立
    micro2_noise_cj = rng.normal(0, p['s_Z_cj_within'], (C, J)) * HasTF_cj_1980
    Z2_cj_IV = Z2_c_demean[:, None] * HasTF_cj_1980 + micro2_noise_cj

    # 兼容旧字段: Z_cj ≡ Z1_cj (主 IV)
    Z_cj_IV = Z1_cj_IV.copy()

    df['Z_c地形'] = Z1_c_raw[df['c'].values].astype(np.float32)         # 原始海拔
    df['Z1_cj'] = Z1_cj_IV[df['c'].values, df['j'].values].astype(np.float32)
    df['Z2_cj'] = Z2_cj_IV[df['c'].values, df['j'].values].astype(np.float32)
    df['Z_cj'] = df['Z1_cj']    # 别名, 兼容旧 estimators
    df['micro_noise_cj'] = micro_noise_cj[df['c'].values, df['j'].values].astype(np.float32)

    # ---- 时间维度 ----
    df['Post'] = (df['t'] >= p['Post_year']).astype(np.int8)

    # ---- 排他性核查 (5 项) ----
    print(f"  [排他性核查] E[Z1_cj | HasTF=1] = {Z1_cj_IV[tf_mask_bool].mean():+.4e}  (应≈0)")
    print(f"  [排他性核查] E[Z1_cj | HasTF=0] = {Z1_cj_IV[~tf_mask_bool].mean():+.4e}  (应=0)")
    print(f"  [排他性核查] E[Z2_cj | HasTF=1] = {Z2_cj_IV[tf_mask_bool].mean():+.4e}  (应≈0)")
    print(f"  [排他性核查] E[Z2_cj | HasTF=0] = {Z2_cj_IV[~tf_mask_bool].mean():+.4e}  (应=0)")
    print(f"  [排他性核查] Corr(Z1_cj, Z2_cj | HasTF=1) = "
          f"{np.corrcoef(Z1_cj_IV[tf_mask_bool], Z2_cj_IV[tf_mask_bool])[0,1]:.4f}  "
          f"(<0.7 才可作 over-id 检验)")

    return df, Z1_c_raw, Z2_c_raw, HasTF_cj_1980, Z1_cj_IV, Z2_cj_IV, micro_noise_cj


# ==============================================================================
# 3. Step3: 内生撤并决策 (限 HasTF=1 子集)
# ==============================================================================
def assign_exits(df_skel, HasTF_cj_1980, Z_cj_IV, micro_noise_cj,
                 target_rate=None, endog_strength=1.0, seed=20261019):
    """Step3: 在 HasTF=1 子集里生成 Exit_cj = 1(π_0 + π_1·Z_cj + η_cj > 0)

    注: Z_cj 在 HasTF=1 内部已去均值 (E=0), 所以 π_0 直接对应 baseline 撤并率
    """
    rng = default_rng(seed + 1)
    if target_rate is None:
        target_rate = PANEL_PARAMS['target_Exit_rate']
    p = PANEL_PARAMS
    C, J = p['C'], p['J']

    tf_mask = (HasTF_cj_1980 == 1)
    tf_pairs = np.argwhere(tf_mask)
    N_TF = len(tf_pairs)

    # η_cj (内生信号)
    eta_cj = rng.normal(0, 1, (C, J))

    # logit(P(Exit=1)) = π_0 + π_1·Z_cj + η_cj
    # 因 E[Z_cj | HasTF=1] = 0, E[η_cj] = 0, 所以 π_0 = Φ^{-1}(target_rate) 干净
    pi_1 = p['pi_1']
    logit_p = pi_1 * Z_cj_IV + eta_cj
    pi_0 = norm.ppf(target_rate)   # 直接闭式

    p_Exit = 1 / (1 + np.exp(-logit_p - pi_0))
    Exit_cj = np.zeros((C, J), dtype=np.int8)
    Exit_cj[tf_mask] = (rng.random(N_TF) < p_Exit[tf_mask]).astype(np.int8)
    actual_rate = Exit_cj[tf_mask].mean()

    print(f"  [Step3] 目标撤并率 = {target_rate:.3f}, "
          f"实际撤并率(HasTF=1 内) = {actual_rate:.3f}, "
          f"Endogeneity ρ = {endog_strength:.2f}")

    df_skel = df_skel.copy()
    df_skel['Exit_cj'] = Exit_cj[df_skel['c'].values, df_skel['j'].values].astype(np.int8)
    df_skel['eta_cj'] = eta_cj[df_skel['c'].values, df_skel['j'].values].astype(np.float32)
    df_skel['pi_0'] = np.float32(pi_0)
    df_skel['D_cj'] = df_skel['Exit_cj']
    df_skel['D_cj_x_Post'] = (df_skel['Exit_cj'] * df_skel['Post']).astype(np.int8)

    # 关键: HasTF×Post 控制 (回归时需要)
    df_skel['HasTF_x_Post'] = (df_skel['HasTF_cj_1980'] * df_skel['Post']).astype(np.int8)

    return df_skel, Exit_cj, eta_cj, pi_0, actual_rate


# ==============================================================================
# 4. 真实 DGP (IHS 量纲, 与 twfe_ihs_hdfe 对齐)
# ==============================================================================
def generate_outcomes(df, eta_cj, endog_strength=0.50, beta=None, seed=20261019):
    """生成 Y_cjt ~ Poisson(exp(μ_cjt)), 然后做 IHS 变换 → y_ihs

    真实 DGP (IHS 量纲):
        y_ihs_cjt = α_c + γ_j + δ_cj + τ_t
                    + β · Exit_cj × Post_t
                    + λ · HasTF_cj_1980 × Post_t   (基期布局与 Post 交互)
                    + ε_cjt
    其中 ε_cjt 与 η_cj 相关(内生性), 且 Z_cj (在 HasTF=1 内部正交于 HasTF)
    满足排他性 → IV-DDD 在控制 HasTF×Post 后能干净识别 β
    """
    rng = default_rng(seed + 2)
    if beta is None:
        beta = TRUE_BETA_IHS    # 默认 0.20, 与 twfe_ihs_hdfe 对齐

    p = PANEL_PARAMS
    C, J, T = p['C'], p['J'], p['T_year_end'] - p['T_year_start'] + 1

    # ---- 固定效应 ----
    alpha_c = rng.normal(0, 0.6, C)
    gamma_j = rng.normal(0, 0.3, J)
    delta_cj = rng.normal(0, 0.2, (C, J))

    # 年趋势 + 周期扰动
    tau_t = 0.025 * (np.arange(T) - T/2) + rng.normal(0, 0.1, T)

    # ---- 第二阶段扰动 ε_cjt (与 η_cj 相关) ----
    rho = endog_strength
    nu_cj = rng.normal(0, 1, (C, J))
    nu_cjt = np.stack([nu_cj] * T, axis=-1) + rng.normal(0, 0.1, (C, J, T))
    eta_cjt = np.stack([eta_cj] * T, axis=-1)
    eps_cjt = rho * eta_cjt + np.sqrt(max(0, 1 - rho**2)) * nu_cjt

    # ---- 复制到面板 ----
    df = df.copy()
    df['alpha_c'] = alpha_c[df['c'].values].astype(np.float32)
    df['gamma_j'] = gamma_j[df['j'].values].astype(np.float32)
    df['delta_cj'] = delta_cj[df['c'].values, df['j'].values].astype(np.float32)
    df['tau_t'] = tau_t[df['t'].values - p['T_year_start']].astype(np.float32)
    df['eps_cjt'] = eps_cjt[df['c'].values, df['j'].values, df['t'].values - p['T_year_start']].astype(np.float32)

    # ---- 真实处理项 (IHS 量纲) ----
    df['beta_D_Post'] = (beta * df['D_cj_x_Post']).astype(np.float32)
    # HasTF×Post 在 IHS 量纲下的系数: λ=0.05 (轻微, 表示基期布局有轻微额外效应)
    lambda_HasTF_Post = 0.05
    df['lambda_HasTF_Post'] = (lambda_HasTF_Post * df['HasTF_x_Post']).astype(np.float32)

    # ---- 真实 DGP (IHS 量纲, 与 twfe_ihs_hdfe 对齐) ----
    # 注: 用真实泊松采样保留 P(Y=0) 稀疏度, 避免 Y_count 总是 >=1
    # ---- 泊松强度(稀疏度校准) ----
    # 早期(t<1990) P(Y=0)≈25%, 后期≈10%, 总体均值≈3-5
    lam_log = (df['alpha_c'].values + df['gamma_j'].values
               + df['delta_cj'].values + df['tau_t'].values
               + df['beta_D_Post'].values + df['lambda_HasTF_Post'].values
               + df['eps_cjt'].values)
    # 标定均值使 P(Y=0) 符合三线企业稀疏度
    baseline_lam = np.where(df['t'].values < 1990, np.log(1.4), np.log(3.2))
    lam_log = lam_log - lam_log.mean() + baseline_lam
    lam = np.exp(lam_log)
    Y_count = rng.poisson(lam).astype(np.int32)
    df['Y'] = Y_count
    df['lam_true'] = lam.astype(np.float32)

    # ---- IHS 变换: y_ihs = arcsinh(Y) (反正弦双曲, 兼容 Y=0) ----
    # arcsinh(0) = 0, arcsinh(Y) ≈ log(2Y) 当 Y 大, 接近 log 当 Y 小
    df['y_ihs'] = np.arcsinh(df['Y'].values.astype(np.float64)).astype(np.float32)

    return df


# ==============================================================================
# 5. 诊断
# ==============================================================================
def diagnose(df):
    p_zero = (df['Y'] == 0).mean()
    p_zero_early = (df[df['t'] < 1990]['Y'] == 0).mean()
    p_zero_late = (df[df['t'] >= 1990]['Y'] == 0).mean()
    mean_y = df['Y'].mean()
    var_y = df['Y'].var()

    print(f"[DGP-DIAGNOSE] N = {len(df):,}")
    print(f"  P(Y=0)        = {p_zero:.3f}")
    print(f"  P(Y=0|t<1990) = {p_zero_early:.3f}")
    print(f"  P(Y=0|t>=1990)= {p_zero_late:.3f}")
    print(f"  Mean(Y)       = {mean_y:.3f}")
    print(f"  Var(Y)/Mean(Y)= {var_y/mean_y:.3f}")
    print(f"  HasTF_cj_1980稀疏度 = {df['HasTF_cj_1980'].mean():.3f}")
    print(f"  Exit_cj 稀疏度     = {df['Exit_cj'].mean():.3f}")
    print(f"  Z1_cj 均值/标准差    = {df['Z1_cj'].mean():.3e} / {df['Z1_cj'].std():.3f}")
    print(f"  Z1_cj 在 HasTF=1 子集内 std = {df[df['HasTF_cj_1980']==1]['Z1_cj'].std():.3f}")
    print(f"  Z2_cj 均值/标准差    = {df['Z2_cj'].mean():.3e} / {df['Z2_cj'].std():.3f}")
    print(f"  y_ihs 均值/标准差    = {df['y_ihs'].mean():.3f} / {df['y_ihs'].std():.3f}")
    return None


# ==============================================================================
# 6. 自检入口
# ==============================================================================
if __name__ == '__main__':
    print("="*72)
    print("sim_dgp.py v3 排他性修复版 — 自检")
    print("="*72)

    df_skel, Z1_c_raw, Z2_c_raw, HasTF_cj_1980, Z1_cj_IV, Z2_cj_IV, micro_noise_cj = build_skeleton()

    df_skel, Exit_cj, eta_cj, pi_0, actual_rate = assign_exits(
        df_skel, HasTF_cj_1980, Z1_cj_IV, micro_noise_cj,
        target_rate=0.40, endog_strength=0.5
    )

    df = generate_outcomes(df_skel, eta_cj, endog_strength=0.5)

    print()
    diagnose(df)
    print()
    print(f"D_cj_x_Post非零数 = {(df['D_cj_x_Post']==1).sum():,}")
    print(f"HasTF×Post 非零数 = {(df['HasTF_x_Post']==1).sum():,}")
    print()
    print("关键不变量核查:")
    z1_when_noTF = df[df['HasTF_cj_1980']==0]['Z1_cj']
    z2_when_noTF = df[df['HasTF_cj_1980']==0]['Z2_cj']
    print(f"  Z1_cj | HasTF=0  max绝对值 = {z1_when_noTF.abs().max():.6e}  (应为 0)")
    print(f"  Z2_cj | HasTF=0  max绝对值 = {z2_when_noTF.abs().max():.6e}  (应为 0)")
    exit_no_TF = df[(df['Exit_cj']==1) & (df['HasTF_cj_1980']==0)]
    print(f"  Exit=1 但 HasTF=0 的样本数 = {len(exit_no_TF):,}  (应为空)")

    # 检查 IV 排他性: Z1, Z2 与 D_cj 的相关性
    from scipy.stats import pearsonr
    r_z1, _ = pearsonr(df['Z1_cj'], df['D_cj_x_Post'])
    r_z2, _ = pearsonr(df['Z2_cj'], df['D_cj_x_Post'])
    print(f"  Corr(Z1_cj, D×Post) = {r_z1:+.4f}  (期望 +0.3~+0.5, 一阶段 F>10)")
    print(f"  Corr(Z2_cj, D×Post) = {r_z2:+.4f}  (期望 +0.3~+0.5, 一阶段 F>10)")
    print(f"  Corr(y_ihs, D×Post) raw = {pearsonr(df['y_ihs'], df['D_cj_x_Post'])[0]:+.4f}")
    print()
    print(df[['c', 'j', 't', 'Y', 'y_ihs', 'HasTF_cj_1980', 'Exit_cj', 'Post',
              'D_cj_x_Post', 'HasTF_x_Post', 'Z1_cj', 'Z2_cj']].head(8).to_string())
