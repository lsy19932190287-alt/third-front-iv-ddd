"""修复 tab3/4 line 14-15 的 multicolumn"""
p = r"F:\三线建设\paper\tables\tab3_h2.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
# 把 {[技校组 边际效应]} ... \textbf{0.5033} \\ 改为 multicolumn 跨 2 列
s = s.replace(
    '{[技校组 边际效应]} $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{tech}}$ & \\textbf{0.5033}$^{{*}}$ \\\\',
    '\\multicolumn{2}{l}{[技校组 边际效应] $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{tech}}$} & \\textbf{0.5033}$^{{*}}$ \\\\'
)
s = s.replace(
    '{[非技校组 边际效应]} $= \\hat{\\beta}_0$ & \\textbf{0.2231}$^{{*}}$ \\\\',
    '\\multicolumn{2}{l}{[非技校组 边际效应] $= \\hat{\\beta}_0$} & \\textbf{0.2231}$^{{*}}$ \\\\'
)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("OK tab3")

p = r"F:\三线建设\paper\tables\tab4_h3.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace(
    '{[GPTs 边际效应]} $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{gpt}}$ & \\textbf{0.2457}$^{}$ \\\\',
    '\\multicolumn{2}{l}{[GPTs 边际效应] $= \\hat{\\beta}_0 + \\hat{\\beta}_{\\mathrm{gpt}}$} & \\textbf{0.2457}$^{}$ \\\\'
)
s = s.replace(
    '{[非GPTs 边际效应]} $= \\hat{\\beta}_0$ & \\textbf{0.2337}$^{{*}}$ \\\\',
    '\\multicolumn{2}{l}{[非GPTs 边际效应] $= \\hat{\\beta}_0$} & \\textbf{0.2337}$^{{*}}$ \\\\'
)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("OK tab4")
