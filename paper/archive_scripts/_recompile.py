"""用 subprocess 真正调 xelatex 验证改动"""
import subprocess
import os
import time

PAPER_DIR = r'F:\三线建设\paper'
XELATEX = r'F:\LaTeX\texmfs\install\miktex\bin\x64\xelatex.exe'

os.chdir(PAPER_DIR)

print('开始 xelatex 第一遍...')
t0 = time.time()
r1 = subprocess.run(
    [XELATEX, '-interaction=nonstopmode', 'main.tex'],
    capture_output=True, text=True, timeout=180,
    encoding='utf-8', errors='ignore'
)
print(f'  退出码: {r1.returncode}, 耗时: {time.time()-t0:.1f}s')

print('\n开始 xelatex 第二遍 (交叉引用)...')
t1 = time.time()
r2 = subprocess.run(
    [XELATEX, '-interaction=nonstopmode', 'main.tex'],
    capture_output=True, text=True, timeout=180,
    encoding='utf-8', errors='ignore'
)
print(f'  退出码: {r2.returncode}, 耗时: {time.time()-t1:.1f}s')

# 检查 PDF
PDF = os.path.join(PAPER_DIR, 'main.pdf')
if os.path.exists(PDF):
    size = os.path.getsize(PDF)
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(PDF)))
    print(f'\n✓ main.pdf: {size:,} bytes ({size/1024:.1f} KB), mtime={mtime}')

# 第二遍日志的错误行
err_lines = [l for l in r2.stdout.split('\n') if l.startswith('!')]
print(f'\n第二遍 ! 错误数: {len(err_lines)}')
for l in err_lines[:10]:
    print(f'  {l}')

# 末尾摘要
out_lines = r2.stdout.split('\n')
print(f'\n--- 第二遍末尾 15 行 ---')
for l in out_lines[-15:]:
    print(l)