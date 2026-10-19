"""看 tab4 line 14 raw bytes"""
p = r"F:\三线建设\paper\tables\tab4_h3.tex"
with open(p, 'rb') as f:
    lines = f.readlines()
print(f"line 14 (raw bytes):")
print(repr(lines[13]))
print(f"\nline 13 (raw bytes):")
print(repr(lines[12]))
