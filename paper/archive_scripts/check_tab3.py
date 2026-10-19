"""看 tab3 line 15 raw bytes"""
p = r"F:\三线建设\paper\tables\tab3_h2.tex"
with open(p, 'rb') as f:
    data = f.read()
# 找 "N$ &"
idx = data.find(b'N$ &')
print(f"idx of N$ & = {idx}")
print(data[idx-10:idx+200].decode('utf-8', errors='replace'))
