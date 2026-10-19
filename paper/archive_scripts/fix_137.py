"""修复 line 149-150 Runaway argument"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 找到 "提醒政策制定者:" 后面那个未闭合的 \textbf{
# 原文 (line 149-150):
#   提醒政策制定者: \textbf{战略腹地的存量人力
#   资本与技术资产, 是可以被市场化重新激活的"}。
# 修复: 移除行间断行 + 移除 " 是" 里的双引号
bad = r"""        负担\"的简化叙事, 提醒政策制定者: \textbf{战略腹地的存量人力
       资本与技术资产, 是可以被市场化重新激活的\"}。"""

good = r"""        负担的简化叙事, 提醒政策制定者: \textbf{战略腹地的存量人力资本与技术资产可以被市场化重新激活}。"""

if bad in s:
    s = s.replace(bad, good)
    print("OK 修复 line 149-150")
else:
    # 找另一格式
    import re
    s2 = re.sub(
        r'提醒政策制定者:\s*\\textbf\{战略腹地的存量人力\s*\n\s*资本与技术资产[^}]*\}。',
        r'提醒政策制定者: \\textbf{战略腹地的存量人力资本与技术资产可以被市场化重新激活}。',
        s
    )
    if s2 != s:
        s = s2
        print("OK regex 修复")
    else:
        print("WARN not found")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
