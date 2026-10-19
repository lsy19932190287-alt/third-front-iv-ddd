"""最后修复 - 直接 str.replace"""
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 4 处 .std_errors 为 _safe_se 调用
replacements = [
    ('se1 = m_tech1.std_errors["treat_post"]', 'se1 = _safe_se(m_tech1, "treat_post")'),
    ('se0 = m_tech0.std_errors["treat_post"]', 'se0 = _safe_se(m_tech0, "treat_post")'),
    ('se1 = m_gpt1.std_errors["treat_post"]', 'se1 = _safe_se(m_gpt1, "treat_post")'),
    ('se0 = m_gpt0.std_errors["treat_post"]', 'se0 = _safe_se(m_gpt0, "treat_post")'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"  ✅ Replaced: {old[:50]}")
    else:
        print(f"  ⚠️ Not found: {old[:50]}")

with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone")
