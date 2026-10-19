"""
最终修复 IVResults 的 SE 提取
"""
import re
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'r', encoding='utf-8') as f:
    content = f.read()

# IVResults 用 std_errors (Series), 不是 bse
# 在 _safe_se 中, 我们已经覆盖了. 但 IVResults 的 std_errors 是 Series
# Test:
old = '''def _safe_se(model, var):
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
    return np.nan'''

new = '''def _safe_se(model, var):
    """Safe SE extraction for both statsmodels and linearmodels"""
    if hasattr(model, "bse"):
        try:
            v = model.bse[var]
            if hasattr(v, "__getitem__") and not isinstance(v, (int, float)):
                return float(v)
            return v
        except:
            pass
    if hasattr(model, "std_errors"):
        try:
            v = model.std_errors[var]
            if hasattr(v, "__getitem__") and not isinstance(v, (int, float)):
                return float(v)
            return v
        except:
            pass
    if hasattr(model, "stderr"):
        try:
            v = model.stderr[var]
            if hasattr(v, "__getitem__") and not isinstance(v, (int, float)):
                return float(v)
            return v
        except:
            pass
    return np.nan'''

if old in content:
    content = content.replace(old, new)
    print("✅ Replaced _safe_se")
else:
    print("⚠️ Old _safe_se not found")

with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'w', encoding='utf-8') as f:
    f.write(content)
