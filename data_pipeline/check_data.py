import pandas as pd
df = pd.read_csv(r"F:\三线建设\data_pipeline\tables\county_anchor_1985.csv")
print(f"county_anchor_1985 总行数: {len(df)}")
print(f"is_in_main_sample 值:")
print(df['is_in_main_sample'].value_counts())

seed = pd.read_csv(r"F:\三线建设\data_pipeline\seed\B0_third_front_seed_db.csv")
print(f"\nseed 行数: {len(seed)}")
print(f"seed 列: {seed.columns.tolist()}")
print(f"seed industries: {sorted(seed['cic2_code'].unique().tolist())}")
print(f"seed counties 唯一: {seed['county_1985'].nunique()}")
print(f"seed has_tech_school 分布: {seed['has_tech_school'].value_counts().to_dict()}")
print(f"seed is_gpt_sector 分布: {seed['is_gpt_sector'].value_counts().to_dict()}")
