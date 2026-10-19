"""查 sec05 line 425 错误源 (\\textit 跨行)"""
import re
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 找 \textit 位置
positions = []
for m in re.finditer(r'\\textit\{', s):
    positions.append(m.start())
print(f"\\textit 位置: {positions}")

# 找第 425 行前后内容
lines = s.split('\n')
print(f"\nLine 419-426:")
for i in range(418, min(426, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()[:130]}")

# 检查 \textit{...} 块跨行情况 (直接搜)
for i, line in enumerate(lines, 1):
    if "textit{" in line:
        print(f"\nL{i}: {line.rstrip()[:130]}")
        # 找闭合
        depth = 1
        j = i - 1
        while j < len(lines) and depth > 0:
            for c in lines[j]:
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
            if depth > 0:
                j += 1
        print(f"  闭合在 L{j+1}: {lines[j].rstrip()[:130]}")