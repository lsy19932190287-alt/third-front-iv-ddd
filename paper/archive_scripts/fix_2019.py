"""把 sec03 中 \\citet{董志凯2019} 改为 董志凯2003 (bib 只有 2003)"""
import re, glob
for f in glob.glob(r"F:\三线建设\paper\sec*.tex"):
    with open(f, 'r', encoding='utf-8') as fp:
        s = fp.read()
    if '董志凯2019' in s:
        s = s.replace('董志凯2019', '董志凯2003')
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(s)
        print(f"修复 {f}: 董志凯2019 -> 2003")
    else:
        pass
print("完成")
