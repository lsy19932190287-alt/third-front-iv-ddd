"""清理 LaTeX 中所有问题引号"""
import re, glob
# 1. tab1-5 中可能需要 fix resizebox; 先尝试完全去掉
for p in glob.glob(r"F:\三线建设\paper\tables\tab*.tex"):
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    # 检查内容 (没有 resizebox 引起问题的简化办法: 移除 resizebox, 改用 \small + tabular)
    # 实际上保留 0.95\textwidth 即可
    pass

# 2. 修复 sec05 line 200 的 "反流""归巢""新三线" 嵌套引号
# 这是 "反流""归巢" 三个连续嵌套 "..."..."..."..."  错误
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    data = f.read()
# 找到 "反流"
idx = data.find('"反流"'.encode('utf-8'))
print(f"idx of 反流 = {idx}")
# 找到紧跟着的段落结束
if idx > 0:
    end_idx = data.find('。'.encode('utf-8'), idx)
    print(f"end_idx = {end_idx}")
    if end_idx > 0:
        # 截取 [idx, end_idx+3) 看
        snippet = data[idx-50:end_idx+10].decode('utf-8', errors='replace')
        print(f"snippet:\n{snippet}")
        # 替换: "反流""归巢""新三线" -> 单一反流 / 归巢 / 新三线
        old = '"反流""归巢""新三线"'.encode('utf-8')
        new = '反流 / 归巢 / 新三线'.encode('utf-8')
        if old in data:
            data = data.replace(old, new)
            print(f"OK 修复嵌套引号, 共替换 1 处")
        else:
            # 另一种写法
            old2 = '三线\\\"反流\\\"\\\"归巢\\\"\\\"新三线\\\"等动态。'.encode('utf-8')
            print(f"找2: {old2 in data}")
            if old2 in data:
                data = data.replace(old2, '三线反流 / 归巢 / 新三线等动态。'.encode('utf-8'))
                print("OK2 修复")
    with open(p, 'wb') as f:
        f.write(data)
