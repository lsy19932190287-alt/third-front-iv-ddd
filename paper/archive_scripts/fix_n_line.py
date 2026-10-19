"""修复:
1. tab2_main.tex: N 行 \\multicolumn{2}{c}{...} 之间缺 &
2. sec05 line 425: \\textit{...} 中的可能未转义
"""
import re

# === 1. tab2 N 行 ===
p = r"F:\三线建设\paper\tables\tab2_main.tex"
with open(p, 'rb') as f:
    raw = f.read()

# 检查 N 行内容
n_line_pattern = b'$N$ & '
m = re.search(b'\\$N\\$ & ([^\\\\]+)', raw)
if m:
    print(f"N 行内容: {m.group(0)[:200]}")
    # 在每个 \\multicolumn{2}{c}{246,240} 后加 &
    n_content = m.group(1)
    # 替换: \\multicolumn{2}{c}{246,240} \\multicolumn -> \\multicolumn{2}{c}{246,240} & \\multicolumn
    new_n = re.sub(rb'\\multicolumn\{2\}\{c\}\{246,240\} \\multicolumn',
                   rb'\\multicolumn{2}{c}{246,240} & \\multicolumn',
                   n_content)
    new_n = re.sub(rb'\\multicolumn\{2\}\{c\}\{246,240\} \\\\',
                   rb'\\multicolumn{2}{c}{246,240} \\\\',
                   new_n)
    new_full = b'$N$ & ' + new_n
    if new_full != m.group(0):
        raw2 = raw.replace(m.group(0), new_full)
        with open(p, 'wb') as f:
            f.write(raw2)
        print("✅ N 行修复完成")
    else:
        print("N 行无需修复")

# === 2. sec05 \\textit{...} 检查 ===
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    raw = f.read()

# 找 \\textit{...} 中含未转义 _
import re
# 找 \\textit{...} 块
m = re.search(rb'\\textit\{([^\}]+)\}', raw)
if m:
    content = m.group(1)
    print(f"\nsec05 \\textit 内容: {content[:200]}")
    # 找裸露的 _
    bad_underscore = re.findall(rb'(?<!\\)_', content)
    if bad_underscore:
        print(f"  找到 {len(bad_underscore)} 处裸露 _")
        # 修复: 转义所有非 \\的 _
        new_content = re.sub(rb'(?<!\\)_', b'\\\\_', content)
        if new_content != content:
            raw2 = raw.replace(m.group(0), b'\\textit{' + new_content + b'}')
            with open(p, 'wb') as f:
                f.write(raw2)
            print(f"  ✅ sec05 \\textit 转义修复")
    else:
        print("  无裸露 _")

# 找 sec05 中所有未转义的 _x (x 是字母)
m = re.findall(rb'(?<!\\)_[a-zA-Z\u4e00-\u9fff]', raw)
print(f"\nsec05 中裸露的 _{{字母/中文}}: {len(m)} 处")
if m[:5]:
    for x in m[:5]:
        pos = raw.find(x)
        print(f"  {x.decode('utf-8')}: ...{raw[max(0,pos-30):pos+30]}...")