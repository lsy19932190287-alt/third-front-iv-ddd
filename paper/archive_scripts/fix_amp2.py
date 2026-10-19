"""F-stat 和 Hansen J 各加一个 & (用 read+write)"""
p = r"F:\三线建设\paper\tables\tab2_main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# F-stat: 1 stage $F$ & & & & & & & & & & 24586.11 & 7796.74 \\
old1 = "一阶段 $F$ & & & & & & & & & & 24586.11 & 7796.74 \\\\"
new1 = "一阶段 $F$ & & & & & & & & & & & 24586.11 & 7796.74 \\\\"
print(f"F-stat 替换: {old1 in s}")
s = s.replace(old1, new1)

# Hansen J: Hansen $J$ ($p$-val) & & & & & & & & & & & 1.86 (0.173) \\
old2 = "Hansen $J$ ($p$-val) & & & & & & & & & & & 1.86 (0.173) \\\\"
new2 = "Hansen $J$ ($p$-val) & & & & & & & & & & & & 1.86 (0.173) \\\\"
print(f"Hansen J 替换: {old2 in s}")
s = s.replace(old2, new2)

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("✅ 完成")

# 验证
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in [12, 13, 14]:
    n_amp = lines[i-1].count('&')
    print(f"L{i} (n_&={n_amp}): {lines[i-1].rstrip()}")