import sys
p = r"F:\三线建设\data_pipeline\B6_event_study.py"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 1. POST_YEAR 加注释
s = s.replace('POST_YEAR = 1986\nBASE_YEAR = 1985',
              'POST_YEAR = 1986  # 1986 年撤并启动\nBASE_YEAR = 1985  # k = -1 基期 (omitted)')

# 2. rel_year 公式: t - 1985 → t - 1986
s = s.replace('df["rel_year"] = df["year"] - BASE_YEAR  # k = t - 1985',
              'df["rel_year"] = df["year"] - POST_YEAR  # k = t - 1986 (1985 基期 = k=-1)')

# 3. xlabel 改
s = s.replace(r"ax.set_xlabel(r'相对年份 $k = t - 1985$ (1985 为基期)', fontsize=10.5)",
              r"ax.set_xlabel(r'相对年份 $k = t - 1986$ (1985 为基期 $k=-1$)', fontsize=10.5)")

# 4. print 年份: 1985+k → 1986+k
s = s.replace('print(f"{k:>4d} {1985+k:>5d}',
              'print(f"{k:>4d} {1986+k:>5d}')
s = s.replace('theta_dict[str(k)] = {"year": int(1985 + k),',
              'theta_dict[str(k)] = {"year": int(1986 + k),')

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("B6 替换完成")
