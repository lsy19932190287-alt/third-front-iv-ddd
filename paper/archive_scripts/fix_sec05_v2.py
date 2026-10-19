"""修复 sec05:
1. 移除重复的 placeholder figure (因 sec04 已有 fig:eventstudy 真图)
2. 将 \\ref{fig:eventstudy_robust} -> \\ref{fig:eventstudy} (sec04 的真图)
"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 1. 把"图占位"替换的 figure 块删除 (从 \\begin{figure}[htbp] 到 \\end{figure})
import re
# 先看 sec05 的 placeholder figure 范围
idx_start = s.find("\\begin{figure}[htbp]\n\\centering\n\\fbox{\\parbox{0.92\\textwidth}{\\centering\n\\vspace{1em}\n\\textit{[图占位: 事件研究系数图]}")
if idx_start == -1:
    # try a less strict pattern
    idx_start = s.find("\\begin{figure}[htbp]\n\\centering\n\\fbox{\\parbox{0.92\\textwidth}{\\centering\n\\vspace{1em}")
print(f"placeholder figure idx_start = {idx_start}")
if idx_start >= 0:
    # 找到 \\end{figure}
    idx_end = s.find("\\end{figure}", idx_start) + len("\\end{figure}")
    print(f"idx_end = {idx_end}, length = {idx_end - idx_start}")
    # 删除这段 figure (含前后空行)
    s_new = s[:idx_start] + s[idx_end:]
    # 把紧跟的 \n\n 压缩成一个 \n
    s_new = s_new.replace("事件研究 (Event Study): 相对 1986 年撤并的 ATT 动态轨迹") if False else s_new  # not used
    print(f"删除了 {idx_end - idx_start} 字符")
    s = s_new

# 2. 替换 \\ref{fig:eventstudy_robust} -> \\ref{fig:eventstudy}
s = s.replace("\\ref{fig:eventstudy_robust}", "\\ref{fig:eventstudy}")

# 3. 删除描述 placeholder figure 内容的段落 (it was: "图~\\ref{fig:eventstudy} 显示, 在政策前...")
# 但因为现在 sec04 已经有这个图, 删掉文字段
# 注意: sec05 紧跟的"图~\\ref{fig:eventstudy} 显示, ..."文字段应该改为引用 sec04 的图
# 检查是否需要 - 现在的文字段引用的是 sec04 的图 (label=fig:eventstudy)
# 这是 OK 的, 不需要修改

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

print("sec05 修复完成")
print()
print("=== 修改后 sec05 行数 ===")
import subprocess
result = subprocess.run(['findstr', '/N', '$', p], capture_output=True, text=True, encoding='utf-8', errors='replace')
if result.stdout:
    for line in result.stdout.strip().split('\n')[-15:]:
        print(line)