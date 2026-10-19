"""终极验证"""
import re, os

# 最新 log
for logf in ["xelatex_run3.log", "xelatex_run1.log", "xelatex_finalA.log"]:
    p = os.path.join(r"F:\三线建设\paper\logs", logf)
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            s = f.read()
        err_count = len(re.findall(r'^! ', s, re.MULTILINE))
        undef = s.count('undefined')
        out = re.search(r'Output written on (\S+) \((\d+) pages', s)
        if out:
            out_str = f"{out.group(1)} ({out.group(2)} pages)"
        else:
            out_str = "N/A"
        print(f"\n{logf}: Errors={err_count}, Undef={undef}, Output={out_str}")
        errors = re.findall(r'^! [^\n]+', s, re.MULTILINE)
        if errors:
            print("  First errors:")
            for e in errors[:5]:
                print(f"    {e[:120]}")

print()
pdf = r"F:\三线建设\paper\main.pdf"
if os.path.exists(pdf):
    print(f"main.pdf: {os.path.getsize(pdf):,} bytes ({os.path.getsize(pdf)/1024:.1f} KB)")
    print(f"main.pdf 修改时间: {time.ctime(os.path.getmtime(pdf))}")