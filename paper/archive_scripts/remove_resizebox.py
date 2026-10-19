"""移除所有 tab*.tex 中的 resizebox, 改用 \\small + \\setlength{\\tabcolsep}"""
import re, glob

for p in glob.glob(r"F:\三线建设\paper\tables\tab*.tex"):
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    # 移除 resizebox 包裹
    # Pattern: \resizebox{...}{!}{  ...  \end{tabular}}
    # 改为: \begin{table}[htbp] \centering \small ...  \end{tabular}
    new_s = re.sub(
        r'\\resizebox\{[^}]+\}\{[^}]+\}\{',
        '',
        s
    )
    # 把 \end{tabular}} 改为 \end{tabular}
    new_s = re.sub(
        r'\\end\{tabular\}\}',
        r'\\end{tabular}',
        new_s
    )
    if new_s != s:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_s)
        print(f"  移除 resizebox: {p.split(chr(92))[-1]}")
    else:
        print(f"  [无变化] {p.split(chr(92))[-1]}")
print("完成")
