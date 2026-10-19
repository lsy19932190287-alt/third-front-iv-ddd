"""检查 Round 11 tab_summary.json 数字"""
import json

p = r"F:\三线建设\paper\tables\tab_summary.json"
with open(p, 'r', encoding='utf-8') as f:
    s = json.load(f)

print('=== Table 2 主表 (Round 11) ===')
for k, v in s['table2'].items():
    if 'beta' in v and 'se' in v:
        t = v['beta'] / v['se'] if v['se'] > 0 else 0
        sig_marker = '***' if abs(t) > 2.576 else ('**' if abs(t) > 1.96 else ('*' if abs(t) > 1.645 else ''))
        print(f'  [{k:15}] beta={v["beta"]:.4f} se={v["se"]:.4f} t={t:.2f} {sig_marker}')

print()
print('=== Table 3 H2 (Round 11) ===')
print(f'  beta_0     = {s["table3_h2"]["beta_main"]:.4f} (se={s["table3_h2"]["se_main"]:.4f})')
print(f'  beta_tech  = {s["table3_h2"]["beta_interact_tech"]:.4f} (se={s["table3_h2"]["se_interact_tech"]:.4f})')
print(f'  marg_tech1 = {s["table3_h2"]["marginal_tech1"]:.4f}')
print(f'  marg_tech0 = {s["table3_h2"]["marginal_tech0"]:.4f}')

print()
print('=== Table 4 H3 (Round 11) ===')
print(f'  beta_0     = {s["table4_h3"]["beta_main"]:.4f} (se={s["table4_h3"]["se_main"]:.4f})')
print(f'  beta_gpt   = {s["table4_h3"]["beta_interact_gpt"]:.4f} (se={s["table4_h3"]["se_interact_gpt"]:.4f})')
print(f'  marg_gpt1  = {s["table4_h3"]["marginal_gpt1"]:.4f}')
print(f'  marg_gpt0  = {s["table4_h3"]["marginal_gpt0"]:.4f}')

print()
print(f'=== DGP ===')
print(f'  beta_0={s["true_beta"]["beta_0"]} beta_tech={s["true_beta"]["beta_tech"]} beta_gpt={s["true_beta"]["beta_gpt"]}')

# 检查 stars 计算
import numpy as np
for k, v in s['table2'].items():
    if 'beta' in v and 'se' in v:
        t = v['beta'] / v['se'] if v['se'] > 0 else 0
        sig_marker = '***' if abs(t) > 2.576 else ('**' if abs(t) > 1.96 else ('*' if abs(t) > 1.645 else ''))
        if sig_marker:
            print(f'  {k}: {sig_marker}')

print()
print('=== H2/H3 stars ===')
b0 = s['table3_h2']['beta_main']
se0 = s['table3_h2']['se_main']
bt = s['table3_h2']['beta_interact_tech']
set_ = s['table3_h2']['se_interact_tech']
bg = s['table4_h3']['beta_interact_gpt']
seg = s['table4_h3']['se_interact_gpt']
print(f'  H2 β_0     : t={b0/se0:.2f} {"*" if abs(b0/se0)>1.645 else ""}')
print(f'  H2 β_tech  : t={bt/set_:.2f} {"***" if abs(bt/set_)>2.576 else ("**" if abs(bt/set_)>1.96 else "")}')
print(f'  H3 β_gpt   : t={bg/seg:.2f} {"***" if abs(bg/seg)>2.576 else ("**" if abs(bg/seg)>1.96 else "")}')