"""修复 sec03 line 94 did_imputation 未转义"""
p = r"F:\三线建设\paper\sec03_empirical_strategy.tex"
with open(p, 'rb') as f:
    raw = f.read()

# 查找 "did_imputation" 出现位置
import re
matches = list(re.finditer(b'did_imputation', raw))
print(f"找到 {len(matches)} 处 did_imputation")
for m in matches:
    pos = m.start()
    print(f"  pos={pos}: ...{raw[max(0,pos-50):pos+50]}...")

# 替换裸露的 did_imputation 为 \\texttt{did\\_imputation}
# 但是如果已经是 \\texttt{did\\_imputation} 就跳过
# 简单方案: 把所有 did_imputation 替换为 did\\_imputation (在 LaTeX 中 \\texttt{...} 不必要, 只需要转义 _)

# 但要注意已经有些地方用了 \\texttt{did\\_imputation} 不应该被破坏
new_raw = re.sub(rb'(?<!\\)\bdid_imputation\b', b'did\\\\_imputation', raw)

# 检查替换数量
count = len(re.findall(b'did\\\\_imputation', new_raw)) - len(re.findall(b'did\\\\_imputation', raw))
print(f"新增转义: {count}")

if new_raw != raw:
    with open(p, 'wb') as f:
        f.write(new_raw)
    print("✅ 修复完成")
else:
    print("no change needed")