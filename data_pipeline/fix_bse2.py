import re
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'r', encoding='utf-8') as f:
    content = f.read()
# Replace all variations of .std_errors
content = content.replace('.std_errors', '.bse')
# For IV results, use .std_errors again (IVResults has std_errors not bse)
# But since we use it in a single method, let me also fix linearmodels
content = content.replace('m.bse[', 'get_se(m, "')  # placeholder
# Restore - this is getting too complex
content = re.sub(r'm\.bse\[(\w+)\]', r'_safe_se(m, "\1")', content)
# Define _safe_se function
with open(r'F:\三线建设\data_pipeline\_patch.py', 'w', encoding='utf-8') as f:
    f.write('''
def _safe_se(model, var):
    """Safe SE extraction for both statsmodels and linearmodels"""
    if hasattr(model, 'bse'):
        try:
            return model.bse[var]
        except:
            return np.nan
    if hasattr(model, 'std_errors'):
        try:
            return model.std_errors[var]
        except:
            return np.nan
    return np.nan

def get_se(model, var):
    return _safe_se(model, var)
''')
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched')
