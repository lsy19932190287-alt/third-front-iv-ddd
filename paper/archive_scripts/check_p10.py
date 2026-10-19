p = r"F:\三线建设\paper\logs\xelatex_pass10.log"
with open(p, 'r', encoding='utf-8', errors='replace') as f:
    s = f.read()
print('Output:', 'Output written' in s)
print('Errors (!):', s.count('! '))
print('Warnings:', s.count('LaTeX Warning'))
print('Overfull:', s.count('Overfull'))
print('Pages:', [l for l in s.split('\n') if 'pages' in l][-1] if [l for l in s.split('\n') if 'pages' in l] else 'N/A')
