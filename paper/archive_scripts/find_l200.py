"""看 xelatex pass 2 log 中 line 200 附近"""
p = r"F:\三线建设\paper\logs\xelatex_pass2.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
# 找 "反流"
idx = s.find('反流')
if idx > 0:
    print(f"idx={idx}")
    print(s[idx-200:idx+200])
else:
    print("not found 反流")
# 找 line 200
m = s.find('l.200')
if m > 0:
    print(f"--- l.200 at {m}:")
    print(s[m:m+400])
