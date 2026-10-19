"""直接看 line 149-150 的 raw bytes"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    data = f.read()

# 找到 简化叙事
idx = data.find("简化叙事".encode('utf-8'))
print(f"找到 '简化叙事' at byte {idx}")
# 显示 idx 周围 200 字节
print(data[idx:idx+300].decode('utf-8', errors='replace'))
