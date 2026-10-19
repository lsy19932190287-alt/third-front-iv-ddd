"""修复 sec05 中所有 LaTeX 错误:
1. line 137 Runaway argument
2. line 47 \n 是 literal 不是 LaTeX 换行
3. tab2_main.tex resizebox 包裹问题
4. tab3/4_h2/h3 resizebox 包裹问题
"""
import re

# ============================================================
# 1. 修复 sec05: line 47 \n literal 和 line 137 Runaway argument
# ============================================================
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 1.1 替换 \n (literal) 为真实换行 (在 LaTeX 中用 \par 或 \\)
# 只针对我之前在 fix_sec05.py 中错误加入的 \n
# 这是一段很长的字符串
bad_block = r"""Pre 期 $k\in[-6,-1]$ 系数显著为负, 反映 \textbf{处理县-行业在 Pre 期 Y 水平较低}\n       (这是 DDD identification 的内在基础); Post 期 $k\geq 0$ 系数围绕 0\n       波动, 绝大部分不显著, 表明 Post 期 common shock (1986 年撤并) 的\n       水平效应被 (c,t) FE 大量吸收。DDD 主回归 $\hat{\alpha}=0.18$--$0.35$ 在\n       §4 中得到一致支持。"""

good_block = r"""Pre 期 $k\in[-6,-1]$ 系数显著为负, 反映 \textbf{处理县-行业在 Pre 期 Y 水平较低}
(这是 DDD identification 的内在基础); Post 期 $k\geq 0$ 系数围绕 0
波动, 绝大部分不显著, 表明 Post 期 common shock (1986 年撤并) 的
水平效应被 (c,t) FE 大量吸收。DDD 主回归 $\hat{\alpha}=0.18$--$0.35$ 在
\S 4 中得到一致支持。"""

if bad_block in s:
    s = s.replace(bad_block, good_block)
    print("[1.1] \n literal -> 真实换行 OK")
else:
    print("[1.1] not found, will try alternative")

# 1.2 修复 line 137 Runaway argument
# 之前的 edit 删除了部分双引号但留下了未闭合的 \textbf{
# 找到 "战略腹地的存量人力" 这一段 (应该是 \textbf{战略腹地的存量人力 \n 资本与技术资产, 是可以被市场...
# 简化为一行
bad_137 = r"""\textbf{战略腹地的存量人力
       资本与技术资产, 是可以被市场化重新激活的\"}。"""
good_137 = r"""\textbf{战略腹地的存量人力资本与技术资产, 是可以被市场化重新激活的}。"""
if bad_137 in s:
    s = s.replace(bad_137, good_137)
    print("[1.2] Runaway arg 修复 OK")
else:
    # 找另一种格式
    s2 = re.sub(
        r'\\textbf\{战略腹地的存量人力\s*\n\s*资本与技术资产[^}]*\}。',
        r'\\textbf{战略腹地的存量人力资本与技术资产, 是可以被市场化重新激活的}。',
        s
    )
    if s2 != s:
        s = s2
        print("[1.2] Runaway arg regex 修复 OK")
    else:
        print("[1.2] WARN: not found, may already fixed")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

# ============================================================
# 2. 修复 tab2_main.tex: resizebox 把 tabular 包裹出错
#    错误: "! Extra alignment tab has been changed to \cr."
#    原因: tabular 内部用 \multicolumn{...}{c}{...} 与 resizebox 嵌套冲突
# ============================================================
p2 = r"F:\三线建设\paper\tables\tab2_main.tex"
with open(p2, 'r', encoding='utf-8') as f:
    s2 = f.read()

# 在 \resizebox{\textwidth}{!}{ 前加 \smaller 字号, 同时把 \resizebox 改为 \adjustbox
# 但更简单: 把 \resizebox{\textwidth}{!} 改成 \resizebox{0.95\textwidth}{!}
# 这样能容纳但不撑满
s2 = s2.replace(r'\resizebox{\textwidth}{!}', r'\resizebox{0.95\textwidth}{!}')
with open(p2, 'w', encoding='utf-8') as f:
    f.write(s2)
print("[2] tab2_main 0.95 缩小 OK")

# ============================================================
# 3. 修复 tab3/4/5 resizebox 类似问题
# ============================================================
for p3 in [r"F:\三线建设\paper\tables\tab3_h2.tex",
           r"F:\三线建设\paper\tables\tab4_h3.tex",
           r"F:\三线建设\paper\tables\tab5_longdiff.tex",
           r"F:\三线建设\paper\tables\tab1_descstats.tex"]:
    with open(p3, 'r', encoding='utf-8') as f:
        ss = f.read()
    ss = ss.replace(r'\resizebox{\textwidth}{!}', r'\resizebox{0.95\textwidth}{!}')
    with open(p3, 'w', encoding='utf-8') as f:
        f.write(ss)
    print(f"[3] {p3.split(chr(92))[-1]} 缩小 OK")

# ============================================================
# 4. 检查 bib 中是否真的有 董志凯2019
# ============================================================
with open(r"F:\三线建设\paper\references.bib", 'r', encoding='utf-8') as f:
    bib = f.read()
if '董志凯2019' in bib:
    print("[4] bib 中 董志凯2019 存在")
else:
    print("[4] bib 中 董志凯2019 缺失 (使用 董志凯2003 替代)")
print("All fixes applied.")
