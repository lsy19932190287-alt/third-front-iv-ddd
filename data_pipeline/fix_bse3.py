"""
修复 B5b_simple_regressions.py 中的 std_errors / bse 问题
"""
import re

with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在文件开头添加 _safe_se 函数
helper_func = '''
def _safe_se(model, var):
    """Safe SE extraction for both statsmodels and linearmodels"""
    if hasattr(model, "bse"):
        try:
            return model.bse[var]
        except:
            pass
    if hasattr(model, "std_errors"):
        try:
            return model.std_errors[var]
        except:
            pass
    return np.nan

'''

# 替换所有的 m.bse[] 和 m.std_errors[] 为 _safe_se()
content = re.sub(r'(\w+)\.bse\[(\w+)\]', r'_safe_se(\1, "\2")', content)
content = re.sub(r'(\w+)\.std_errors\[(\w+)\]', r'_safe_se(\1, "\2")', content)

# 2. 在 # ===== 工具函数 ===== 之后插入 _safe_se
content = content.replace(
    '# ===== 工具函数 =====\ndef sig(t):',
    '# ===== 工具函数 =====\n' + helper_func + 'def sig(t):'
)

with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成")

# Verify
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'r', encoding='utf-8') as f:
    new_content = f.read()
print(f"  .std_errors 出现次数: {new_content.count('.std_errors')}")
print(f"  .bse 出现次数: {new_content.count('.bse')}")
print(f"  _safe_se 出现次数: {new_content.count('_safe_se')}")
