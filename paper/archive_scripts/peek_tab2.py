with open(r"F:\三线建设\paper\tables\tab2_main.tex", 'r', encoding='utf-8') as f:
    for i, l in enumerate(f.readlines(), 1):
        print(f"L{i}: {l.rstrip()}")