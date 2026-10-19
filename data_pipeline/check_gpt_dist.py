"""查 seed 92 家企业中 is_gpt_sector 的分布 + 调整策略"""
import pandas as pd
import sys

p = r"F:\三线建设\data_pipeline\seed\B0_third_front_seed_db.csv"
df = pd.read_csv(p, encoding="utf-8")
print(f"92 家种子企业行数: {len(df)}")
print(f"列: {list(df.columns)}")

# is_gpt_sector 分布
print(f"\n[is_gpt_sector] 各值计数:")
print(df["is_gpt_sector"].value_counts(dropna=False))
print(f"[is_gpt_sector] 均值: {df['is_gpt_sector'].mean():.4f}")
print(f"[is_gpt_sector] 在 Exit=1 子集中: {df.loc[df['has_exit']==1, 'is_gpt_sector'].mean():.4f}")
print(f"[has_exit] 均值: {df['has_exit'].mean():.4f}")
print(f"[has_tech_school] 均值: {df['has_tech_school'].mean():.4f}")

# Exit x GPT 联合
print(f"\n[Exit × GPT 联合分布]")
ct = pd.crosstab(df['has_exit'], df['is_gpt_sector'], margins=True)
print(ct)

# Exit x GPT 联合 / 在 92 家企业中的比例
print(f"\n[92 家种子企业] has_exit=1 且 is_gpt_sector=1: {((df['has_exit']==1) & (df['is_gpt_sector']==1)).sum()}")
print(f"[92 家种子企业] has_exit=1 且 is_gpt_sector=0: {((df['has_exit']==1) & (df['is_gpt_sector']==0)).sum()}")
print(f"[92 家种子企业] has_exit=0 且 is_gpt_sector=1: {((df['has_exit']==0) & (df['is_gpt_sector']==1)).sum()}")
print(f"[92 家种子企业] has_exit=0 且 is_gpt_sector=0: {((df['has_exit']==0) & (df['is_gpt_sector']==0)).sum()}")
print(f"在 has_exit=1 的子集中 is_gpt_sector=1 占比: {((df['has_exit']==1) & (df['is_gpt_sector']==1)).sum() / max((df['has_exit']==1).sum(), 1):.4f}")

# 现在看 (county, industry) 唯一格子
df_cj = df.drop_duplicates(subset=['county_1985', 'cic2_code'])
print(f"\n[92 家企业 → 唯一 (county, industry) 格子]: {len(df_cj)}")
print(f"[格子] is_gpt_sector=1: {(df_cj['is_gpt_sector']==1).sum()}")
print(f"[格子] is_gpt_sector=0: {(df_cj['is_gpt_sector']==0).sum()}")

# 在 Exit_cj 子集中
df_cj_exit = df_cj[df_cj['has_exit'] == 1]
print(f"\n[格子且 Exit=1]: {len(df_cj_exit)}")
print(f"  其中 is_gpt_sector=1: {(df_cj_exit['is_gpt_sector']==1).sum()} ({(df_cj_exit['is_gpt_sector']==1).mean():.4f})")