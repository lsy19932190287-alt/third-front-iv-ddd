"""验证作者与致谢改动是否完成"""
import re

print('=' * 70)
print('验证 main.tex 作者块')
print('=' * 70)
with open(r'F:\三线建设\paper\main.tex', 'r', encoding='utf-8') as f:
    main = f.read()

# author block
m = re.search(r'\\author\{.*?\n\}', main, re.DOTALL)
if m:
    print(m.group())
print()
# pdfauthor
m = re.search(r'pdfauthor=\{[^}]*\}', main)
if m:
    print('PDF meta:', m.group())

# 检查残留
print('\n--- 虚拟信息残留检查 ---')
for fake in ['黄炜', '王雪', '陈思远', 'huangwei@xxx.edu.cn', '清华', '中国宏观经济研究院', '中国社会科学院数量']:
    cnt = main.count(fake)
    flag = '✓' if cnt == 0 else '✗'
    print(f'  {flag} [{fake}]: {cnt} 处')

print(f'\n李仕宇 出现次数: {main.count("李仕宇")} (期望 ≥1)')

print()
print('=' * 70)
print('验证 sec05 致谢段')
print('=' * 70)
with open(r'F:\三线建设\paper\sec05_robustness_conclusion.tex', 'r', encoding='utf-8') as f:
    sec05 = f.read()

m = re.search(r'\\begin\{center\}.*?\\end\{center\}', sec05, re.DOTALL)
if m:
    print(m.group())

print('\n--- 虚拟信息残留检查 ---')
for fake in ['20&ZD089', '黄炜', 'huangwei@xxx.edu.cn']:
    cnt = sec05.count(fake)
    flag = '✓' if cnt == 0 else '✗'
    print(f'  {flag} [{fake}]: {cnt} 处')

print(f'\n李仕宇 出现次数: {sec05.count("李仕宇")} (期望 1)')