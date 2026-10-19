with open(r"F:\三线建设\paper\sec05_robustness_conclusion.tex", 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(415, min(425, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")