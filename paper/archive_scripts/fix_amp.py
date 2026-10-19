"""F-stat 和 Hansen J 各加一个 &"""
import re

p = r"F:\三线建设\paper\tables\tab2_main.tex"
with open(p, 'rb') as f:
    raw = f.read()

# F-stat 行: 加一个 & 在最后空之前
old1 = b'\xe4\xb8\x80\xe9\x98\xb6\xe6\xae\xb5 $F$ & & & & & & & & & & 24586.11 & 7796.74 \\\\\\r\n'
new1 = b'\xe4\xb8\x80\xe9\x98\xb6\xe6\xae\xb5 $F$ & & & & & & & & & & & 24586.11 & 7796.74 \\\\\\r\n'
print(f"F-stat 替换: {old1 in raw}")
raw = raw.replace(old1, new1)

# Hansen J 行: 加一个 & 在最后空之前
old2 = b'Hansen $J$ ($p$-val) & & & & & & & & & & & 1.86 (0.173) \\\\\\r\n'
new2 = b'Hansen $J$ ($p$-val) & & & & & & & & & & & & 1.86 (0.173) \\\\\\r\n'
print(f"Hansen J 替换: {old2 in raw}")
raw = raw.replace(old2, new2)

with open(p, 'wb') as f:
    f.write(raw)

# 验证
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"\nL13 F-stat: {lines[12].rstrip()}")
print(f"L14 Hansen J: {lines[13].rstrip()}")