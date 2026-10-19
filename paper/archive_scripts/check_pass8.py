"""看 xelatex pass 8 log 末尾"""
p = r"F:\三线建设\paper\logs\xelatex_pass8.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
lines = s.split('\n')
for line in lines[-50:]:
    print(line)
