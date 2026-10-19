with open(r"F:\三线建设\paper\sec05_robustness_conclusion.tex", 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[130:150], start=131):
    print(f'{i:3d}: {line.rstrip()}')
