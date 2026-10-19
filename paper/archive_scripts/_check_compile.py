"""查看 compile1.log 末尾 / 错误 / PDF 大小"""
import os

LOG = r'F:\三线建设\paper\compile1.log'
PDF = r'F:\三线建设\paper\main.pdf'

# 检查 PDF
if os.path.exists(PDF):
    size = os.path.getsize(PDF)
    print(f'✓ main.pdf 存在, 大小 = {size:,} bytes ({size/1024:.1f} KB)')
    # 时间戳
    import time
    mtime = os.path.getmtime(PDF)
    print(f'  修改时间 = {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))}')
else:
    print('✗ main.pdf 不存在!')

# 检查 log
if os.path.exists(LOG):
    with open(LOG, 'r', encoding='utf-8', errors='ignore') as f:
        log = f.read()
    print(f'\n--- compile1.log ({len(log)} chars) ---')
    # 找错误
    err_count = log.count('! ')
    err_lines = [l for l in log.split('\n') if l.startswith('!') or 'Error' in l or 'fatal' in l.lower()]
    print(f'! 行数: {err_count}')
    print(f'错误行 (前 20):')
    for l in err_lines[:20]:
        print(f'  {l}')
    # 末尾 30 行
    print('\n--- 末尾 30 行 ---')
    lines = log.split('\n')
    for l in lines[-30:]:
        print(l)
else:
    print(f'✗ {LOG} 不存在')