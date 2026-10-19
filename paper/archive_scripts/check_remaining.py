"""查 main.tex + sec05 实际未匹配段内容"""
# main.tex
p = r"F:\三线建设\paper\main.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
idx = s.find("三重交互")
if idx > 0:
    print("=== main.tex 三重交互附近 ===")
    print(s[idx-300:idx+500])
print()
print("=========================================")
# sec05
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
for kw in ["DDD 主回归", "1980 年代", "约 0.18", "约 0.24", "0.18--0.35"]:
    idx = s.find(kw)
    if idx > 0:
        print(f"=== {kw} (at {idx}) ===")
        print(s[idx-100:idx+250])
        print()