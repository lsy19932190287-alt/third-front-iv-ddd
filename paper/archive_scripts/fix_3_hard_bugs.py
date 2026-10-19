"""3 个硬伤修复:
1. main.tex line 56: 作者上标 $^{}$ -> \\textsuperscript{}
2. sec05: \\textbf{...} 跨行空行 (blank line 结束段落) -> 删空行
3. tab2_main.tex: tabular 列数 7 -> 13 (l + 6*2)
"""

# === 1. main.tex 作者上标修复 ===
p = r"F:\三线建设\paper\main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 替换 $^{b}$ -> \textsuperscript{b}, $^{c}$ -> \textsuperscript{c}
repl = [
    ('黄炜\\footnote{通讯作者, 邮箱: huangwei@xxx.edu.cn}~{}^{,a,b}$\\quad$%',
     '黄炜\\thanks{通讯作者, 邮箱: huangwei@xxx.edu.cn}\\textsuperscript{a,b}\\quad'),
    ('王雪$^{b}$\\quad', '王雪\\textsuperscript{b}\\quad'),
    ('陈思远$^{c}$\\\\[0.3em]', '陈思远\\textsuperscript{c}'),
    ('$^{a}$中国宏观经济研究院\\quad', '\\textsuperscript{a}中国宏观经济研究院\\quad'),
    ('$^{b}$清华大学经济管理学院\\quad', '\\textsuperscript{b}清华大学经济管理学院\\quad'),
    ('$^{c}$中国社会科学院数量经济与技术经济研究所',
     '\\textsuperscript{c}中国社会科学院数量经济与技术经济研究所'),
]
count = 0
for old, new in repl:
    if old in s:
        s = s.replace(old, new)
        count += 1
    else:
        print(f"WARN main.tex: {old[:50]}...")
print(f"main.tex: {count}/{len(repl)} 替换成功")
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# === 2. sec05 跨行 \textbf{} 空行修复 ===
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 把 \textbf{...} 中间的空行 (即 \n\n 在 \textbf{ 和 } 之间) 替换为 \n (用 \\ 强制换行)
import re

# 先标记 \textbf{ 开始位置
# 找出所有 \textbf{ ... } 配对（跨行）
# 但因为可能嵌套, 我们用一个简单的策略:
# 在 \textbf{ ... } 范围内部, 把 \n\n 替换为 \n (合并空行)

# 使用状态机扫描
new_s = []
i = 0
n = len(s)
while i < n:
    # 检查是否遇到 \textbf{
    if s[i:i+8] == '\\textbf{':
        # 找到匹配的 }
        # 用栈深度跟踪 (考虑嵌套)
        depth = 1
        j = i + 8
        while j < n and depth > 0:
            if s[j:j+2] == '\\{':  # \{
                j += 2
                continue
            if s[j:j+2] == '\\}':  # \}
                j += 2
                continue
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
            j += 1
        # 现在 s[i:j] 是完整的 \textbf{...}
        block = s[i:j]
        # 把 block 内部的 \n\n 替换为 \n
        cleaned = block.replace('\n\n', '\n')
        new_s.append(cleaned)
        i = j
    else:
        new_s.append(s[i])
        i += 1

s2 = ''.join(new_s)
n_replaced = s.count('\n\n') - s2.count('\n\n')
print(f"sec05: \\textbf{{}} 跨行空行 -> 合并, 共清理 {n_replaced} 个空行")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s2)

# === 3. tab2_main.tex 列数 7 -> 13 ===
p = r"F:\三线建设\paper\tables\tab2_main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 当前 tabular 是 lcccccc (7 列), 但 D×Post 行有 12 个 & (13 列) - 实际是 12 个数据 + 1 标签
# 应该改为 l + 12 c = 13 列

# 主效应行
s = s.replace("\\begin{tabular}{lcccccc}",
              "\\begin{tabular}{lcccccccccccc}")

# F-stat 行 (5 空 + IV 列, 占 6 列)
# 原: "一阶段 $F$ & & & & & "
# 新: "一阶段 $F$ & & & & & & & & & & " (10 个 & + 11 个空 = 11 列)
# 但 tabular 是 13 列 (l + 12 c), 主效应行 13 列, F-stat 行也要 13 列
# F-stat 行 6 个 coef 列 (l 后): IV 占 2 (5 + 6 列), 其他 4 列空
# 改为: "一阶段 $F$ & & & & & & & & & & 24586.11 & 7796.74 \\\\"
# 数: 1 (label) + 9 (空) + 2 (数字) = 12 个分隔符, 13 列 ✓

s = s.replace("一阶段 $F$ & & & & & ",
              "一阶段 $F$ & & & & & & & & & & ")

# Hansen J 行 (6 列 + 1 label = 7, 现在需要 13)
# 原: "Hansen $J$ ($p$-val) & & & & & & "
# 新: "Hansen $J$ ($p$-val) & & & & & & & & & & & "
s = s.replace("Hansen $J$ ($p$-val) & & & & & & ",
              "Hansen $J$ ($p$-val) & & & & & & & & & & & ")

# N 行 (1 label + 6 个 multicolumn{2}{c}{N})
# 原: "$N$ & " + 6 个 "\multicolumn{2}{c}{N} " (12 列 + label = 13 列)
# 检查原代码是否已正确
# 原: f.write("$N$ & ")
# for label, key in cols2:
#     f.write(f"\\multicolumn{{2}}{{c}}{{{results[key]['N']:,}}} ")
# 这是 l + 6*multicolumn{2} = l + 12 = 13 列 ✓ 但前面是 \multicolumn{2}{c}{TWFE-IHS} (合并 2 列) 等
# 所以 \multicolumn 计数: \multicolumn{2} 占 2 列
# 总列数: l (1) + \multicolumn{2}{c}{TWFE-IHS} (2) + TWFE-LPM (1) + PPML (1) + \multicolumn{2}{c}{IV-DDD} (2) = 7 列 (label 总数)
# 但数据行有 12 列 (6 coef + 6 SE)，所以 tabular 应该是 13 列
# N 行的 \multicolumn{2}{c}{...} 各占 2 列，共 6 个 = 12 列
# 加上前面的 $N$ label 占 1 列 = 13 列 ✓

# 检查 N 行是否已经是 13 列
n_line = re.search(r'\$N\$ & .*?\\\\\\\\', s)
if n_line:
    block = n_line.group(0)
    count_amp = block.count('&')
    print(f"  N 行分隔符 (\\&): {count_amp}, 应为 12 (= 13 列 - 1)")

# 主效应行 (line 12) 应该是 13 列
main_line = re.search(r'\$[^$]*\$.*?\\\\\\\\', s)
if main_line:
    block = main_line.group(0)
    count_amp = block.count('&')
    print(f"  主效应行分隔符 (\\&): {count_amp}, 应为 12 (= 13 列 - 1)")

# 主效应行最后应改为: ..., β_6 & SE_6 \\
# 当前: \textbf{0.2470}$^{**}$ & (0.1072) & \\
# 数 & : 1 (label) + 5 (5 coef + 5 SE 配对) + 1 + 1 = 12... 实际上12 个 & 对应13 列

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("tab2_main.tex: tabular 7 列 -> 13 列")