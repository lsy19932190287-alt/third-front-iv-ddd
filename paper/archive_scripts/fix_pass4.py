"""修复 tab3/4 中 [非GPTs 边际效应] 列错位 + sec05 line 209 嵌套引号"""
import re, glob

# 1. tab3/tab4 line 14: 看 [非GPTs 边际效应] 上下文
for p in [r"F:\三线建设\paper\tables\tab3_h2.tex",
          r"F:\三线建设\paper\tables\tab4_h3.tex"]:
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    # 在 `\textbf{0.1490}` 之前应有 `&`
    # 找 [非GPTs 边际效应] (tab4) 或 [非技校组 边际效应] (tab3)
    if '[非GPTs 边际效应]' in s:
        # 在 [非GPTs 边际效应] 后应有 &
        # Pattern: [非GPTs 边际效应]                  $= \hat{\beta}_0$ 缺 &
        s = s.replace(
            '[非GPTs 边际效应]\n                  $= \\hat{\\beta}_0$',
            '[非GPTs 边际效应] & $= \\hat{\\beta}_0$'
        )
        s = s.replace(
            '[GPTs 边际效应]\n                  $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{gpt}}$',
            '[GPTs 边际效应] & $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{gpt}}$'
        )
    if '[非技校组 边际效应]' in s:
        s = s.replace(
            '[非技校组 边际效应]\n                  $= \\hat{\\beta}_0$',
            '[非技校组 边际效应] & $= \\hat{\\beta}_0$'
        )
        s = s.replace(
            '[技校组 边际效应]\n                  $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{tech}}$',
            '[技校组 边际效应] & $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{tech}}$'
        )
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"修复 {p.split(chr(92))[-1]}")

# 2. sec05 line 209: 嵌套引号
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    data = f.read()
target = '\\\"新三线\\\"\\\"战略腹地\\\"'.encode('utf-8')
print(f"target in data: {target in data}")
if target in data:
    data = data.replace(target, '新三线 / 战略腹地'.encode('utf-8'))
    with open(p, 'wb') as f:
        f.write(data)
    print("OK 修复 sec05 line 209")
