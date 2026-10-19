"""把 CRLF 转换为 LF, 让 LaTeX 正确识别 \\ 行结束"""
import glob

for p in glob.glob(r"F:\三线建设\paper\**\*.tex", recursive=True):
    with open(p, 'rb') as f:
        data = f.read()
    new_data = data.replace(b'\r\r\n', b'\n')
    if new_data != data:
        with open(p, 'wb') as f:
            f.write(new_data)
        print(f"  {p.split(chr(92))[-1]}: CRLF -> LF")
print("完成")
