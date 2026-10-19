import os
p = r"F:\三线建设\paper\main.pdf"
if os.path.exists(p):
    print(f"main.pdf: {os.path.getsize(p):,} bytes")
else:
    print("main.pdf: NOT EXISTS")
    # 看 xdv
    xdv = r"F:\三线建设\paper\main.xdv"
    if os.path.exists(xdv):
        print(f"main.xdv: {os.path.getsize(xdv):,} bytes")
