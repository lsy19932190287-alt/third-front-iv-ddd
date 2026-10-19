"""修复 $^{*\\*\\*}$ 上标语法问题"""
import re, glob

for p in glob.glob(r"F:\三线建设\paper\tables\tab*.tex"):
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    new_s = s
    # 修复 $^{***}$ -> $^{{*}}$ （单个星号 * 转义）
    # 实际上更简洁: 改用 \star\star\star
    new_s = new_s.replace('$^{***}$', r'$^{{*}}$')  # 单星号保险
    new_s = new_s.replace('$^{**}$', r'$^{{*}}$')
    if new_s != s:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_s)
        print(f"  修复 {p.split(chr(92))[-1]}")
    else:
        pass

# 同样修复 sec*.tex
for p in glob.glob(r"F:\三线建设\paper\sec*.tex"):
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    new_s = s
    new_s = new_s.replace('$^{***}$', r'$^{{*}}$')
    new_s = new_s.replace('$^{**}$', r'$^{{*}}$')
    if new_s != s:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_s)
        print(f"  修复 {p.split(chr(92))[-1]}")
print("完成")
