"""直接替换 raw bytes (用 chr() 避免 ASCII 错误)"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    data = f.read()

# 找到 "提醒政策制定者:" 的位置
marker = "提醒政策制定者:".encode('utf-8')
idx = data.find(marker)
print(f"idx = {idx}")
if idx < 0:
    print("ERROR not found")
else:
    # 找第一个 " 。" (UTF-8: e3 80 82) 在 idx 之后
    end_marker = '。'.encode('utf-8')
    end_idx = data.find(end_marker, idx)
    print(f"end_idx = {end_idx} (delta = {end_idx - idx})")
    if end_idx > 0:
        # 替换 [idx, end_idx + len(end_marker)) 这段
        new_text = '提醒政策制定者: \\textbf{战略腹地的存量人力资本与技术资产可以被市场化重新激活}。'.encode('utf-8')
        new_data = data[:idx] + new_text + data[end_idx + len(end_marker):]
        with open(p, 'wb') as f:
            f.write(new_data)
        print(f"OK 替换完成, 共删除 {end_idx - idx + len(end_marker)} 字节")
