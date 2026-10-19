import re
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('m.std_errors', 'm.bse')
with open(r'F:\三线建设\data_pipeline\B5b_simple_regressions.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Replaced all std_errors with bse')
