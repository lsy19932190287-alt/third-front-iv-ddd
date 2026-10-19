"""核查 reg_sample.dta 实际 HasTF 状态"""
import pandas as pd

df = pd.read_stata(r"F:\三线建设\data_pipeline\reg_sample.dta")
print(f"总行数: {len(df):,}")
print(f"HasTF=1 总数: {int(df['HasTF_cj_1980'].sum()):,}")
mask = df['HasTF_cj_1980'] == 1
print(f"HasTF=1 唯一 (county_id, industry2) 格子数: {df[mask][['county_id','industry2']].drop_duplicates().shape[0]}")
print(f"HasTF=1 county 唯一数: {df[mask]['county'].nunique()}")
print(f"HasTF=1 county 样本: {df[mask]['county'].unique()[:15]}")
print(f"HasTF=1 industry 唯一: {sorted(df[mask]['industry2'].unique())}")
print(f"\ncounty 列前 5 个唯一值: {df['county'].unique()[:10]}")
print(f"county 总唯一数: {df['county'].nunique()}")
print(f"\ncounty_id ∈ [1,44] (seed) HasTF=1 数量: {df[(df['county_id']<=44) & (df['HasTF_cj_1980']==1)]['HasTF_cj_1980'].sum()}")
print(f"county_id ∈ [45,216] (control) HasTF=1 数量: {df[(df['county_id']>=45) & (df['HasTF_cj_1980']==1)]['HasTF_cj_1980'].sum()}")
