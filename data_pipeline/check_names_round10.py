"""诊断 seed CSV 和 anchor CSV 县名格式差异"""
import pandas as pd
import re

BASE = r"F:\三线建设\data_pipeline"
seed = pd.read_csv(f"{BASE}/seed/B0_third_front_seed_db.csv")
anchor = pd.read_csv(f"{BASE}/tables/county_anchor_1985.csv")

# 1) 看 seed 县名
print("="*70)
print("[1] SEED 县名 (92 家企业映射) — 前 30 条 county_1985:")
print("="*70)
print(seed["county_1985"].head(30).to_list())
print(f"\nseed county_1985 唯一数: {seed['county_1985'].nunique()}")
print(f"seed cic2_code 唯一: {sorted(seed['cic2_code'].unique())}")
print(f"seed county × industry 唯一组合数: {seed[['county_1985','cic2_code']].drop_duplicates().shape[0]}")

# 2) 看 anchor 县名
print("\n" + "="*70)
print("[2] ANCHOR 县名 (county_anchor_1985) — 前 30 条:")
print("="*70)
print(anchor["county_v1985"].head(30).to_list())
print(f"\nanchor 县数: {len(anchor)}")
print(f"anchor in_main_sample=True: {(anchor['is_in_main_sample']==True).sum()}")

# 3) 标准化对比
def norm(s):
    """提取核心地名: 去掉 市/县/区/自治县/特区/旗/州/盟 等后缀"""
    if pd.isna(s):
        return ""
    s = str(s).strip()
    # 先去掉 自治州/地区/盟 这类大区
    s = re.sub(r"(自治州|自治县|自治旗|地区|盟|市辖区|街道|镇|乡)$", "", s)
    # 再去掉 县/市/区/特区/旗
    s = re.sub(r"(自治县|县|市|区|特区|旗)$", "", s)
    return s

seed["county_norm"] = seed["county_1985"].map(norm)
anchor["county_norm"] = anchor["county_v1985"].map(norm)

print("\n" + "="*70)
print("[3] 标准化后 (norm) 县名对比:")
print("="*70)
seed_set = set(seed["county_norm"].unique())
anchor_set = set(anchor["county_norm"].unique())
inter = seed_set & anchor_set
print(f"seed norm 唯一数: {len(seed_set)}")
print(f"anchor norm 唯一数: {len(anchor_set)}")
print(f"交集 (norm 后): {len(inter)}")
print(f"  交集前 20: {sorted(inter)[:20]}")
print(f"  seed 独有 (norm): {sorted(seed_set - anchor_set)[:20]}")
print(f"  anchor 独有 (norm): {sorted(anchor_set - seed_set)[:20]}")

# 4) 验证原始字符串交集
seed_raw = set(seed["county_1985"].unique())
anchor_raw = set(anchor["county_v1985"].unique())
print("\n" + "="*70)
print("[4] 原始字符串交集对比 (未标准化):")
print("="*70)
print(f"seed raw 唯一: {len(seed_raw)}, anchor raw 唯一: {len(anchor_raw)}")
print(f"原始交集: {len(seed_raw & anchor_raw)}")
if len(seed_raw & anchor_raw) > 0:
    print(f"  原始交集: {sorted(seed_raw & anchor_raw)[:10]}")
