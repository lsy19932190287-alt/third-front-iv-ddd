"""诊断 Z1 与 HasTF 的相关性 — 修复版"""
import numpy as np
from numpy.random import default_rng

rng = default_rng(20261019)
C, J = 210, 30

# 原始 Z1
elev_std = rng.uniform(0, 1.5, C)
Z1 = (elev_std - elev_std.mean()) / elev_std.std()
print(f'Z1 整体: mean={Z1.mean():+.4e}, std={Z1.std():.4f}')

# HasTF
industry_TF = rng.normal(0, 0.04, J)
HasTF_logits = np.log(0.15/(1-0.15)) + industry_TF[None, :]
HasTF_probs = 1 / (1 + np.exp(-HasTF_logits))
HasTF = (rng.random((C, J)) < HasTF_probs).astype(np.int8)
print(f'HasTF 稀疏度 = {HasTF.mean():.4f}')

# 正确做法: np.where(2D) 直接返回 (c_array, j_array)
c_idx_TF, j_idx_TF = np.where(HasTF == 1)
print(f'c_idx_TF shape = {c_idx_TF.shape}, unique c = {len(np.unique(c_idx_TF))} / {C}')
print(f'Z1 mean over HasTF=1 c (raw, before demean): {Z1[c_idx_TF].mean():+.4e}')

# demean
Z1_demean = Z1 - Z1[c_idx_TF].mean()
print(f'Z1_demean mean over HasTF=1 c: {Z1_demean[c_idx_TF].mean():+.4e}')

# 但 Z1_cj = Z1_demean × HasTF + micro_noise
micro_noise = rng.normal(0, 0.45, (C, J)) * HasTF
Z1_cj = (Z1_demean[:, None] * HasTF) + micro_noise
print(f'E[Z1_cj | HasTF=1] = {Z1_cj[HasTF==1].mean():+.4e}  (理论=0)')
