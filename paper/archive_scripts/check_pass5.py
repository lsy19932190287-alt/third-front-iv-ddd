"""看 xelatex pass 5 log 末尾错误"""
p = r"F:\三线建设\paper\logs\xelatex_pass5.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
lines = s.split('\n')
for line in lines[-60:]:
    print(line)
