"""手动修复 sec05 L419-L425 \\textit{} 块空行"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 找 \\textit{ 的位置
idx_start = s.find("\\textit{")
print(f"start: {idx_start}")
idx_end = s.find("}", idx_start + 9)
print(f"end: {idx_end}")

# 提取 block
block = s[idx_start:idx_end+1]
print(f"block length: {len(block)}")
print(f"block has \\n\\n: {chr(10)+chr(10) in block}")
n_blanks = block.count(chr(10)+chr(10))
print(f"block \\n\\n count: {n_blanks}")

# 清理空行
cleaned = block.replace(chr(10)+chr(10), chr(10))
new_s = s[:idx_start] + cleaned + s[idx_end+1:]
with open(p, 'w', encoding='utf-8') as f:
    f.write(new_s)
print(f"✅ 清理 {n_blanks} 个空行")