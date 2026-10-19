import pandas as pd
anchor = pd.read_csv(r"F:\三线建设\data_pipeline\tables\county_anchor_1985.csv")
seed = pd.read_csv(r"F:\三线建设\data_pipeline\seed\B0_third_front_seed_db.csv")

anchor_counties = set(anchor["county_v1985"].values)
seed_counties = set(seed["county_1985"].values)

intersect = anchor_counties & seed_counties
seed_only = seed_counties - anchor_counties

print(f"anchor 县数: {len(anchor_counties)}")
print(f"seed county_1985 唯一数: {len(seed_counties)}")
print(f"intersect (两者共有): {len(intersect)}")
print(f"仅 seed (不在 anchor): {len(seed_only)}")
print(f"\n仅 seed 的县名: {sorted(seed_only)[:20]}")
print(f"\nseed county 涉及县名: {sorted(seed_counties)[:20]}")
print(f"\nanchor 县前 30 个: {sorted(anchor_counties)[:30]}")
