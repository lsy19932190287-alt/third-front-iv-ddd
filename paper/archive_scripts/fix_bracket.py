"""修复 [非GPTs 边际效应] 中 [ 字符"""
p = r"F:\三线建设\paper\tables\tab4_h3.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
# 把 [非GPTs 边际效应] 改成 {[非GPTs 边际效应]}
s = s.replace('[非GPTs 边际效应]', '{[非GPTs 边际效应]}')
s = s.replace('[GPTs 边际效应]', '{[GPTs 边际效应]}')
# 同时修复 \\textbf{0.2337} 后接 \\\\\\ (双斜杠) 错误
# 但只一行, 不动
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("OK tab4_h3.tex")

p = r"F:\三线建设\paper\tables\tab3_h2.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace('[非技校组 边际效应]', '{[非技校组 边际效应]}')
s = s.replace('[技校组 边际效应]', '{[技校组 边际效应]}')
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("OK tab3_h2.tex")
