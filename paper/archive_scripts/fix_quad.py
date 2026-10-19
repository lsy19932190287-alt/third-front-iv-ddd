"""修复 main.tex 作者块中的 \\quad$% 错误"""
p = r"F:\三线建设\paper\main.tex"
with open(p, 'rb') as f:
    raw = f.read()
s = raw.decode('utf-8')

# 用 raw bytes 修复 (避免转义问题)
bad = b'\\quad$%\r\n  \xe9\x99\x88\xe6\x80\x9d\xe8\xbf\x9c'  # \\quad$%\n  陈思远
if bad in raw:
    new = b'\\quad\r\n  \xe9\x99\x88\xe6\x80\x9d\xe8\xbf\x9c'  # \\quad\n  陈思远
    raw2 = raw.replace(bad, new)
    with open(p, 'wb') as f:
        f.write(raw2)
    print(f"✅ 修复 \\quad$% 错误")
else:
    # try different line ending
    bad2 = b'\\quad$%\n  \xe9\x99\x88\xe6\x80\x9d\xe8\xbf\x9c'
    if bad2 in raw:
        raw2 = raw.replace(bad2, b'\\quad\n  \xe9\x99\x88\xe6\x80\x9d\xe8\xbf\x9c')
        with open(p, 'wb') as f:
            f.write(raw2)
        print(f"✅ 修复 (LF) \\quad$% 错误")
    else:
        print("WARN: bad not found, 检查实际内容")
        # 找 王雪 那行
        import re
        m = re.search(b'\xe7\x8e\x8b\xe9\x9b\xaa[^\\n]+', raw)
        if m:
            print(f"  found 王雪 line: {m.group(0)}")