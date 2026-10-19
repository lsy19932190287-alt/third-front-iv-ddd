"""修复 line 200: 三线\\\"反流\\\"\\\"归巢\\\"\\\"新三线\\\"等动态"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    data = f.read()

# 找 "三线反流" 在文件中的位置
target = '三线\\"反流\\"\\"归巢\\"\\"新三线\\"等动态。'.encode('utf-8')
print(f"target in data: {target in data}")
if target in data:
    replacement = '三线反流 / 归巢 / 新三线等动态。'.encode('utf-8')
    data = data.replace(target, replacement)
    print("OK 替换成功")
    with open(p, 'wb') as f:
        f.write(data)
else:
    # 看实际内容
    idx = data.find('反流'.encode('utf-8'))
    if idx > 0:
        print(f"反流 in data at {idx}")
        print(data[idx-50:idx+200].decode('utf-8', errors='replace'))
