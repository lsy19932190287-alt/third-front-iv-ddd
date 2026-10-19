import re
p = r"F:\三线建设\paper\tables\tab3_h2.tex"
with open(p, 'rb') as f:
    data = f.read()
m = re.search(b'\\\\\\\\\\r', data)
print(f'\\\\\\\\\\r found at {m.start() if m else -1}')
m2 = re.search(b'\\\\\\\\\\n', data)
print(f'\\\\\\\\\\n found at {m2.start() if m2 else -1}')
idx = data.find(b'N$ &')
print(data[idx-10:idx+50])
