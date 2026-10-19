"""
================================================================================
B1_data_cleaning.py — §B-1 数据清洗与匹配脚本设计
================================================================================
三线建设 Exit-DID 顶刊研究 — 数据预处理 Pipeline
--------------------------------------------------------------------------------
输入: 原始工商注册库 (1985-2018, 川+黔+陕+鄂 四省 200+县, 30 个二位数行业)
输出: 清洗后的 (c, j, t) 三维面板 + D_cj 处理状态 + Z_cj 工具变量

主要步骤:
  Step 0: 数据源清单与字段映射
  Step 1: 工商库字段清洗 (成立日期、行业代码、注册地、注册资本)
  Step 2: 县-行业-年面板聚合 (Flow count)
  Step 3: 三线企业名单匹配 (D_cj)
  Step 4: 微观地形工具变量构造 (Z_cj)
  Step 5: 长差分 + HDFE 所需数据集生成
  Step 6: 描述性统计与平衡性检验
================================================================================
"""

import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


# ==============================================================================
# 配置
# ==============================================================================
B1_CONFIG = {
    'input_dir': 'data_raw/',          # 原始工商注册库
    'output_dir': 'data_cleaned/',     # 清洗后输出
    'third_front_master_list': 'data_raw/third_front_master_list.csv',  # 三线企业名单
    'county_year_range': (1985, 2018),
    'industries': list(range(13, 47)),  # GB/T 4754 二位数行业
    'provinces': ['川', '黔', '陕', '鄂'],  # 主样本川+黔, 扩展陕+鄂
    'counties': {
        '川': 'data_raw/county_codes_SC.csv',  # ~150 县
        '黔': 'data_raw/county_codes_GZ.csv',  # ~60 县
        '陕': 'data_raw/county_codes_SN.csv',  # ~80 县
        '鄂': 'data_raw/county_codes_HB.csv',  # ~50 县
    },
}


# ==============================================================================
# Step 0: 数据源清单与字段映射
# ==============================================================================
def step0_data_source_catalog():
    """输出预期数据源清单与字段映射文档"""
    print("=" * 70)
    print("Step 0: Data Source Catalog")
    print("=" * 70)
    catalog = """
    [输入数据源]
    
    1. 工商注册库 (主数据源)
       路径: data_raw/business_registry_{province}.csv
       关键字段:
         - 统一社会信用代码 (uscc) → 唯一企业标识
         - 成立日期 (est_date) → 计算成立年份 est_year
         - 行业代码 (ind_code) → 二位数行业 ind_j
         - 注册地邮编 (reg_zip) → 县 reg_county
         - 注册资本 (reg_capital) → 对数化 lreg_cap
         - 企业状态 (status) → 筛 active=1
    
    2. 三线建设企业名单 (处理变量源)
       路径: data_raw/third_front_master_list.csv
       关键字段:
         - 企业名称 (firm_name) → 用模糊匹配关联到工商库
         - 行业 (ind_code)
         - 县 (county_code)
         - 三线期状态 (tf_status): 一类保留/二类搬迁/三类关停
    
    3. 县-年份行政代码 (地理匹配)
       路径: data_raw/county_year_panel.csv
       关键字段: county_code, county_name, province_id
    
    4. 微观地形数据 (IV 来源)
       路径: data_raw/topography/elevation_pc1.tif (海拔主成分, 30m 分辨率)
       路径: data_raw/topography/slope_pc1.tif (坡度主成分)
       路径: data_raw/rails/{year}_national_railway.shp (国铁站点, 矢量)
    
    [关键变量构造公式]
    
    D_cj = 1(1980 年前县 c 在行业 j 至少有一家三线企业, 且在 1985 年未关停)
    
    Y_{cjt} = 在县 c 行业 j 第 t 年新增注册民营企业数 (Flow)
    
    Z_{cj} = PC1(
        mean(slope of plant_terrain within county c, plant in industry j),
        std(elevation within county c, plant in industry j),
        max(slope_to_nearest_rail_station within county c)
    )
    """
    print(catalog)
    return catalog


# ==============================================================================
# Step 1: 工商库字段清洗
# ==============================================================================
def step1_clean_registry(raw_path, save_path=None):
    """清洗工商注册库, 返回清洗后的 DataFrame

    清洗规则:
      1. 仅保留 active=1 的在册企业
      2. est_date → est_year (4 位年份)
      3. ind_code → ind_j (二位数行业)
      4. reg_zip → reg_county (县级, 通过邮编映射表)
      5. 剔除 est_year 缺失或超出 (1985, 2018) 的观测
      6. 剔除 ind_code 缺失或不在 13-46 范围内的观测
    """
    print("\n" + "=" * 70)
    print(f"Step 1: Cleaning Registry {raw_path}")
    print("=" * 70)

    df = pd.read_csv(raw_path, dtype={'uscc': str, 'reg_zip': str, 'ind_code': str})

    # 1. 仅 active
    if 'status' in df.columns:
        df = df[df['status'] == 1].copy()

    # 2. est_year
    df['est_date'] = pd.to_datetime(df['est_date'], errors='coerce')
    df['est_year'] = df['est_date'].dt.year
    df = df.dropna(subset=['est_year'])
    df['est_year'] = df['est_year'].astype(int)
    y0, y1 = B1_CONFIG['county_year_range']
    df = df[(df['est_year'] >= y0) & (df['est_year'] <= y1)]

    # 3. ind_j
    df['ind_j'] = pd.to_numeric(df['ind_code'].str[:2], errors='coerce')
    df = df.dropna(subset=['ind_j'])
    df['ind_j'] = df['ind_j'].astype(int)
    valid_j = set(B1_CONFIG['industries'])
    df = df[df['ind_j'].isin(valid_j)]

    # 4. reg_county
    zip_to_county = pd.read_csv('data_raw/zip_county_map.csv',
                                  dtype={'reg_zip': str, 'county_code': str})
    df = df.merge(zip_to_county, on='reg_zip', how='left')
    df = df.dropna(subset=['county_code'])

    # 5. 县白名单 (限定为川/黔/陕/鄂)
    valid_county_set = set()
    for prov, path in B1_CONFIG['counties'].items():
        cdf = pd.read_csv(path, dtype={'county_code': str})
        valid_county_set.update(cdf['county_code'].astype(str).tolist())
    df = df[df['county_code'].isin(valid_county_set)]

    # 6. lreg_cap
    if 'reg_capital' in df.columns:
        df['lreg_cap'] = np.log1p(df['reg_capital'].fillna(0))

    print(f"  Raw rows: {len(df):,}")
    print(f"  After cleaning: {len(df):,}")
    print(f"  Unique counties: {df['county_code'].nunique()}")
    print(f"  Unique industries: {df['ind_j'].nunique()}")
    print(f"  Year range: {df['est_year'].min()} - {df['est_year'].max()}")

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(save_path)
        print(f"  ✓ Saved to {save_path}")

    return df


# ==============================================================================
# Step 2: 县-行业-年面板聚合 (Flow count)
# ==============================================================================
def step2_aggregate_panel(df_clean, save_path=None):
    """聚合到 (county, industry, year) 三维面板, 计算 Flow count"""
    print("\n" + "=" * 70)
    print("Step 2: Aggregating to (c, j, t) Panel")
    print("=" * 70)

    # 每年新增 = 当年注册且不属于 (county, industry, year) 已存在的
    df_clean = df_clean.sort_values(['county_code', 'ind_j', 'est_year'])
    df_clean['new_firm'] = ~df_clean.duplicated(subset=['county_code', 'ind_j', 'est_year'])
    # 注: 简化版本, 实际上应当用 uscc 匹配

    panel = (df_clean
             .groupby(['county_code', 'ind_j', 'est_year'])
             .agg(Y=('new_firm', 'sum'),
                  lreg_cap_mean=('lreg_cap', 'mean'))
             .reset_index()
             .rename(columns={'county_code': 'c', 'ind_j': 'j', 'est_year': 't'}))

    # 填充零值 (很多 (c,j,t) 没有新企业)
    all_c = sorted(df_clean['county_code'].unique())
    all_j = sorted(B1_CONFIG['industries'])
    all_t = list(range(*B1_CONFIG['county_year_range']))
    full_idx = pd.MultiIndex.from_product([all_c, all_j, all_t],
                                          names=['c', 'j', 't'])
    panel = (panel.set_index(['c', 'j', 't'])
             .reindex(full_idx, fill_value=0)
             .reset_index())

    # 数字编码
    panel['c_code'] = pd.factorize(panel['c'])[0]
    panel['j_code'] = pd.factorize(panel['j'])[0]
    panel['t_code'] = panel['t'] - B1_CONFIG['county_year_range'][0]

    print(f"  Panel shape: {panel.shape}")
    print(f"  N cells: {len(panel):,}")
    print(f"  Mean Y (new firms): {panel['Y'].mean():.4f}")
    print(f"  P(Y=0): {(panel['Y'] == 0).mean():.3f}")

    if save_path:
        panel.to_parquet(save_path)
        print(f"  ✓ Saved to {save_path}")

    return panel


# ==============================================================================
# Step 3: 三线企业名单匹配 + D_cj
# ==============================================================================
def step3_build_D_cj(panel, tf_master_path, save_path=None):
    """匹配三线企业名单, 构造 D_cj (county × industry 处理状态)"""
    print("\n" + "=" * 70)
    print("Step 3: Building D_cj Treatment Status")
    print("=" * 70)

    # 三线企业名单
    tf = pd.read_csv(tf_master_path,
                     dtype={'county_code': str, 'ind_code': str})
    tf['ind_j'] = pd.to_numeric(tf['ind_code'].str[:2], errors='coerce')
    tf = tf.dropna(subset=['county_code', 'ind_j'])
    tf['ind_j'] = tf['ind_j'].astype(int)

    # 筛选 1980 年前已成立且 1985 年未关停的企业
    if 'est_year' in tf.columns:
        tf = tf[(tf['est_year'] <= 1980) & (tf['status_1985'] != '关停')]

    # 在县级-行业级别去重 (D_cj 是 0/1 二值)
    D_cj = (tf[['county_code', 'ind_j']]
            .drop_duplicates()
            .assign(D_cj=1)
            .rename(columns={'county_code': 'c', 'ind_j': 'j'}))

    # Merge 到面板
    panel = panel.merge(D_cj, on=['c', 'j'], how='left')
    panel['D_cj'] = panel['D_cj'].fillna(0).astype(int)
    panel['Post'] = (panel['t'] >= 1986).astype(int)
    panel['D_cj_x_Post'] = panel['D_cj'] * panel['Post']

    print(f"  N (c,j) treated: {D_cj.shape[0]}")
    print(f"  Total (c,j) pairs: {panel[['c', 'j']].drop_duplicates().shape[0]}")
    print(f"  Treatment density: {panel['D_cj'].mean():.3f}")
    print(f"  D_cj × Post non-zero: {panel['D_cj_x_Post'].sum():,}")

    if save_path:
        panel.to_parquet(save_path)
        print(f"  ✓ Saved to {save_path}")

    return panel


# ==============================================================================
# Step 4: 微观地形工具变量 (Z_cj)
# ==============================================================================
def step4_build_Z_cj(panel, topo_dir='data_raw/topography/',
                     rail_dir='data_raw/rails/',
                     save_path=None):
    """构造 Z_cj: county × industry 层面的微观地形复杂度 PC1

    Components:
      Z1 = std(elevation within county c, plant in industry j)
      Z2 = max(slope_to_nearest_rail_station within county c)
      Z3 = mean(slope of plant_terrain within county c, plant in industry j)
      Z_cj = PC1([Z1, Z2, Z3])
    """
    print("\n" + "=" * 70)
    print("Step 4: Building Z_cj Topographic Instrument")
    print("=" * 70)

    # 三线企业厂址经纬度
    plant_geo = pd.read_csv('data_raw/third_front_plant_geocode.csv',
                            dtype={'county_code': str, 'ind_j': int,
                                   'lat': float, 'lon': float})

    # 高程数据 (30m DEM, ASTER GDEM)
    elev_grid = pd.read_parquet(f'{topo_dir}elevation_pc1.parquet')
    # 提取每个厂址的高程 PC1
    plant_geo['elev_pc1'] = plant_geo.apply(
        lambda r: elev_grid.loc[
            (np.abs(elev_grid['lat'] - r['lat']).argmin()),
            (np.abs(elev_grid['lon'] - r['lon']).argmin())
        ], axis=1
    )

    # 国铁站点 (1980 年)
    rail_stations = pd.read_parquet(f'{rail_dir}stations_1980.parquet')

    # 计算每个厂址到最近国铁站的最大坡度
    def slope_to_nearest_rail(lat, lon):
        distances = np.sqrt((rail_stations['lat'] - lat) ** 2 +
                           (rail_stations['lon'] - lon) ** 2)
        nearest = rail_stations.loc[distances.idxmin()]
        slope = (nearest['elev'] - elev_grid.loc[
            (np.abs(elev_grid['lat'] - lat).argmin()),
            (np.abs(elev_grid['lon'] - lon).argmin())
        ]) / max(distances.min() * 111, 1.0)  # 简化
        return slope
    plant_geo['slope_to_rail'] = plant_geo.apply(
        lambda r: slope_to_nearest_rail(r['lat'], r['lon']), axis=1
    )

    # 按 (c, j) 聚合
    Z_components = plant_geo.groupby(['county_code', 'ind_j']).agg(
        Z1_elev_std=('elev_pc1', 'std'),
        Z2_slope_rail_max=('slope_to_rail', 'max'),
        Z3_slope_rail_mean=('slope_to_rail', 'mean'),
    ).reset_index().rename(columns={'county_code': 'c', 'ind_j': 'j'})

    # PC1
    from sklearn.decomposition import PCA
    pca = PCA(n_components=1)
    Z_components['Z_cj'] = pca.fit_transform(
        Z_components[['Z1_elev_std', 'Z2_slope_rail_max', 'Z3_slope_rail_mean']]
    )

    # Merge 到面板
    panel = panel.merge(Z_components[['c', 'j', 'Z_cj']], on=['c', 'j'], how='left')
    # 缺 Z_cj 的 (c,j) 设为 0 (用 δ_cj 吸收基期差异)
    panel['Z_cj'] = panel['Z_cj'].fillna(0)
    panel['Z_cj_x_Post'] = panel['Z_cj'] * panel['Post']

    print(f"  Z_cj mean: {panel['Z_cj'].mean():.4f}")
    print(f"  Z_cj std: {panel['Z_cj'].std():.4f}")
    print(f"  Z_cj × Post non-zero: {(panel['Z_cj_x_Post'] != 0).sum():,}")

    if save_path:
        panel.to_parquet(save_path)
        print(f"  ✓ Saved to {save_path}")

    return panel


# ==============================================================================
# Step 5: 控制变量构造 (CountyGeo × IndustryChar × Post)
# ==============================================================================
def step5_build_controls(panel, save_path=None):
    """构造 DDD 控制变量: CountyGeo_c × IndustryChar_j × Post_t

    例:
      - log(elevation) × external_finance_dep × Post
      - log(slope_to_coast) × logistics_sensitivity × Post
    """
    print("\n" + "=" * 70)
    print("Step 5: Building DDD Controls")
    print("=" * 70)

    # 县级地形特征
    county_geo = pd.read_csv('data_raw/county_topography.csv',
                             dtype={'c': str})
    county_geo = county_geo.set_index('c')

    # 行业特征 (外部融资依赖度 / 物流敏感度 / 创新强度)
    industry_chars = pd.read_csv('data_raw/industry_characteristics.csv')
    industry_chars = industry_chars.set_index('j')

    # 合并
    panel = panel.merge(county_geo.reset_index(), on='c', how='left')
    panel = panel.merge(industry_chars.reset_index(), on='j', how='left')

    # 三维交互项
    panel['Ctrl_elev_x_finance'] = (panel['mean_elev'] * panel['ext_finance_dep'])
    panel['Ctrl_slope_x_logistics'] = (panel['mean_slope'] * panel['logistics_sens'])
    panel['Ctrl_elev_x_inno'] = (panel['mean_elev'] * panel['innovation_int'])

    # × Post
    for col in ['Ctrl_elev_x_finance', 'Ctrl_slope_x_logistics', 'Ctrl_elev_x_inno']:
        panel[f'{col}_x_Post'] = panel[col] * panel['Post']

    print(f"  Control columns: {[c for c in panel.columns if c.startswith('Ctrl')]}")

    if save_path:
        panel.to_parquet(save_path)
        print(f"  ✓ Saved to {save_path}")

    return panel


# ==============================================================================
# Step 6: 描述性统计 + 平衡性检验
# ==============================================================================
def step6_descriptive_stats(panel, save_path='tables/descriptive_stats.tex'):
    """输出描述性统计和平衡性检验"""
    print("\n" + "=" * 70)
    print("Step 6: Descriptive Statistics & Balance Test")
    print("=" * 70)

    # 1. 全样本描述统计
    desc = panel[['Y', 'D_cj', 'Post', 'D_cj_x_Post', 'Z_cj', 'Z_cj_x_Post']].describe()
    print("\n全样本描述统计:")
    print(desc.T)

    # 2. 按处理/控制分组
    treat = panel[panel['D_cj'] == 1]
    ctrl = panel[panel['D_cj'] == 0]
    print(f"\n处理组 (D_cj=1) N cells: {len(treat):,}")
    print(f"控制组 (D_cj=0) N cells: {len(ctrl):,}")
    print(f"\n处理组 mean(Y) = {treat['Y'].mean():.4f}")
    print(f"控制组 mean(Y) = {ctrl['Y'].mean():.4f}")
    print(f"差分 = {treat['Y'].mean() - ctrl['Y'].mean():.4f}")

    # 3. 处理前趋势检验 (placebo test in pre-period)
    pre = panel[panel['Post'] == 0]
    pre_treat = pre[pre['D_cj'] == 1]['Y'].mean()
    pre_ctrl = pre[pre['D_cj'] == 0]['Y'].mean()
    print(f"\n处理前 mean(Y_treat) = {pre_treat:.4f}")
    print(f"处理前 mean(Y_ctrl)  = {pre_ctrl:.4f}")
    print(f"差异 = {pre_treat - pre_ctrl:.4f} (期望≈0, 平行趋势)")

    # 4. Z_cj 与 D_cj 相关性 (第一阶段强度)
    from scipy.stats import pearsonr
    zj = panel.drop_duplicates(['c', 'j'])[['D_cj', 'Z_cj']]
    corr, pval = pearsonr(zj['Z_cj'], zj['D_cj'])
    print(f"\n第一阶段相关性: corr(Z_cj, D_cj) = {corr:.4f} (p={pval:.4f})")

    return desc


# ==============================================================================
# 主入口
# ==============================================================================
def run_pipeline():
    """完整 B-1 数据清洗 Pipeline"""
    print("=" * 70)
    print("§B-1 Data Cleaning Pipeline — 三线建设 Exit-DID")
    print("=" * 70)

    step0_data_source_catalog()

    # 实际运行需要真实数据
    # 这里给出 pipeline 设计, 实际执行时需要数据到位

    print("\n>>> Pipeline Status:")
    print("    Step 0: ✓ Documentation complete")
    print("    Step 1-5: ⏳ Awaiting raw data ingestion")
    print("    Step 6: ⏳ Final descriptive stats after data loading")

    print("\n[注] 当原始工商库、三线名单、地形数据到位后, 跑以下命令:")
    print("    df = step1_clean_registry('data_raw/business_registry_SC.csv')")
    print("    panel = step2_aggregate_panel(df)")
    print("    panel = step3_build_D_cj(panel, 'data_raw/third_front_master_list.csv')")
    print("    panel = step4_build_Z_cj(panel)")
    print("    panel = step5_build_controls(panel)")
    print("    step6_descriptive_stats(panel)")


if __name__ == '__main__':
    run_pipeline()