"""提取 main.tex 中所有引用 keys"""
import re, glob
keys = set()
for f in glob.glob('sec*.tex') + ['main.tex']:
    try:
        s = open(f, encoding='utf-8').read()
        # 匹配 \cite{...} 或 \citet{...} 或 \citep{...}
        for m in re.finditer(r'\\cite[a-z]*\{([^}]+)\}', s):
            for k in m.group(1).split(','):
                keys.add(k.strip())
    except Exception as e:
        print(f, e)
print('引用的 keys:', len(keys))
for k in sorted(keys):
    print(' ', k)
