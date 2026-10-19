"""把 \\\\\\r\\n 替换为 \\\\\\n (让 LaTeX 正确识别 \\ 行结束)"""
import re, glob

for p in glob.glob(r"F:\三线建设\paper\**\*.tex", recursive=True):
    with open(p, 'rb') as f:
        data = f.read()
    # 替换 \\\r\n -> \\\n  (只在 \\ 后面紧跟 \r\n 时)
    new_data = re.sub(b'\\\\\\\\\\r\\n', b'\\\\\\\\\\n', data)
    if new_data != data:
        with open(p, 'wb') as f:
            f.write(new_data)
        print(f"  {p.split(chr(92))[-1]}: fix \\\\\\r\\n")
print("完成")
