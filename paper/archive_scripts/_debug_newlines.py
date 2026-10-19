"""调试: 检查 sec05 文件的换行符"""
with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'rb') as f:
    raw = f.read()

# 找 \n\n\begin{center} 周围
idx = raw.find(b'\\begin{center}')
print(f'\\begin{{center}} at offset: {idx}')
if idx >= 0:
    # 看周围 200 字节
    snippet = raw[max(0,idx-30):idx+250]
    print(f'\nRaw bytes around \\begin{{center}}:')
    print(repr(snippet))

# 检查换行符
n_crlf = raw.count(b'\r\n')
n_lf = raw.count(b'\n')
print(f'\n\\r\\n count: {n_crlf}')
print(f'\\n count: {n_lf} (含 CRLF)')
print(f'lf-only count: {n_lf - n_crlf}')