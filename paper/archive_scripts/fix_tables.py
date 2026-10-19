"""修复表格超宽 (Overfull hbox): 给 tab1-5 加 \\resizebox{\\textwidth}{!}"""
import re, glob
TABLES = glob.glob(r"F:\三线建设\paper\tables\tab*.tex")

for p in TABLES:
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    # 跳过已经被 resizebox 包裹的
    if r'\resizebox' in s:
        print(f"  [跳过已包装] {p}")
        continue
    # 跳过 mc_sim_table_v4 (独立于 tab)
    # 在 \begin{tabular} 前加 \resizebox
    new_s = re.sub(
        r'(\\begin\{tabular\})',
        r'\\resizebox{\\textwidth}{!}{\1',
        s
    )
    # 匹配对应的 \end{tabular} 后加 }
    # 简单做法: 用一个 stack 计数
    if new_s == s:
        print(f"  [无 tabular 匹配] {p}")
        continue
    # 检查是否已经添加了 { (resizebox 需要关闭)
    # 数 \begin{tabular} 和 \end{tabular}
    n_begin = new_s.count(r'\resizebox{\textwidth}{!}{\begin{tabular}')
    n_end = new_s.count(r'\end{tabular}')
    if n_begin == n_end:
        # 在每个 \end{tabular} 后加 }
        new_s = re.sub(
            r'(\\end\{tabular\})',
            r'\1}',
            new_s
        )
    with open(p, 'w', encoding='utf-8') as f:
        f.write(new_s)
    print(f"  [已包装] {p}: {n_begin} 个 tabular")
