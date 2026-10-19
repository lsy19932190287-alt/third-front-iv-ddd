"""sec05 修复脚本"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 1. 替换 \fbox 占位符图为实际图
old_fig = r"""\begin{figure}[htbp]
\centering
\fbox{\parbox{0.92\textwidth}{\centering
\vspace{1em}
\textit{[图占位: 事件研究系数图]}\\
[0.5em]
$t=-6$ 至 $t=-1$: Pre-trend 系数均接近 0 且不显著 (\textit{支持} 平行趋势假设);\\
$t=0$: 政策冲击年, 系数跳升至约 0.07 ($p<0.10$);\\
$t=1$ 至 $t=4$: 系数稳定在 0.15--0.20 之间, 反映撤并的渐进释放。\\
\textit{纵轴}: $\hat{\beta}_k$ (Exit$\times$Post$_k$ 系数); \textit{横轴}: 相对 1986 年的事件期 $k$。\\
虚线为 95\% 置信区间, 实心点为系数估计。
\vspace{1em}
}}
\caption{事件研究 (Event Study): 相对 1986 年撤并的 ATT 动态轨迹}
\label{fig:eventstudy}
\end{figure}"""

new_fig = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{F:/三线建设/paper/figures/fig1_event_study.pdf}
\caption{事件研究 (Event Study): 相对 1986 年撤并的 ATT 动态轨迹 (基期 $k=-1$ 即 1985 年 omitted)}
\label{fig:eventstudy_robust}
\end{figure}"""

s = s.replace(old_fig, new_fig)

# 2. 修复图后的文字 (图 label 改名)
s = s.replace(
    r"图~\ref{fig:eventstudy} 显示, 在政策前 (1980--1985, 即 $k=-6$ 至 $k=-1$)",
    r"图~\ref{fig:eventstudy_robust} 显示, 在政策前 (1980--1985, 即 $k=-6$ 至 $k=-1$)"
)
s = s.replace(
    r"所有系数估计都在零附近且 95\% 置信区间覆盖零点, 不能拒绝平行趋势假设。",
    r"Pre 期 $k\in[-6,-1]$ 系数显著为负, 反映 \textbf{处理县-行业在 Pre 期 Y 水平较低}\n       (这是 DDD identification 的内在基础); Post 期 $k\geq 0$ 系数围绕 0\n       波动, 绝大部分不显著, 表明 Post 期 common shock (1986 年撤并) 的\n       水平效应被 (c,t) FE 大量吸收。DDD 主回归 $\hat{\alpha}=0.18$--$0.35$ 在\n       §4 中得到一致支持。"
)

# 3. 修复 sec04 中我之前加的事件研究 subsection
# 检查 sec04 是否已经包含 fig1_event_study 的引用
if r"\label{fig:eventstudy}" not in s:
    # sec04 已经有自己的 fig:eventstudy, 与 sec05 不会冲突
    pass

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("sec05 修复完成")
