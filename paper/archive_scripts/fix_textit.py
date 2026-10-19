"""sec05 \\textit{} 跨行空行修复"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# 处理 \\textit{...} 中含空行的情况
# 用状态机扫描
new_s = []
i = 0
n = len(s)
n_fixed = 0
while i < n:
    # 检查是否遇到 \textit{
    if s[i:i+9] == '\\textit{':
        # 找到匹配的 }
        depth = 1
        j = i + 9
        while j < n and depth > 0:
            if s[j:j+2] == '\\{':
                j += 2
                continue
            if s[j:j+2] == '\\}':
                j += 2
                continue
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
            j += 1
        # 现在 s[i:j] 是完整的 \textit{...}
        block = s[i:j]
        # 检查 block 内部是否有空行
        if '\n\n' in block:
            cleaned = block.replace('\n\n', '\n')
            new_s.append(cleaned)
            n_fixed += block.count('\n\n')
            print(f"✅ sec05 \\textit{{}} 跨行空行清理: {block.count(chr(10)+chr(10))} 个")
        else:
            new_s.append(block)
        i = j
    else:
        new_s.append(s[i])
        i += 1

s2 = ''.join(new_s)
print(f"总清理空行: {n_fixed}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(s2)
print("✅ sec05 \\textit 处理完成")