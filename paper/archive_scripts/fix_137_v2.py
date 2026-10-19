"""用 raw bytes 修复 line 149-150 Runaway argument (CRLF)"""
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'rb') as f:
    data = f.read()

bad = b'提醒政策制定者: \\textbf{战略腹地的存量人力\r\r\n       资本与技术资产, 是可以被市场化重新激活的\\"}。'
good = b'提醒政策制定者: \\textbf{战略腹地的存量人力资本与技术资产可以被市场化重新激活}。'

if bad in data:
    data = data.replace(bad, good)
    with open(p, 'wb') as f:
        f.write(data)
    print("OK raw bytes 修复")
else:
    # 二次尝试: 不依赖 CRLF
    bad2 = b'提醒政策制定者: \\textbf{战略腹地的存量人力'
    idx = data.find(bad2)
    if idx >= 0:
        # 找到 } 。 结束
        end_idx = data.find(b'\xe3\x80\x82', idx)  # 找 。
        if end_idx > 0:
            # 截取这之间内容
            new_block = b'提醒政策制定者: \\textbf{战略腹地的存量人力资本与技术资产可以被市场化重新激活}\xe3\x80\x82'
            new_data = data[:idx] + new_block + data[end_idx + len(b'\xe3\x80\x82'):]
            with open(p, 'wb') as f:
                f.write(new_data)
            print(f"OK 截断法修复 ({end_idx - idx} bytes)")
        else:
            print("WARN end not found")
    else:
        print("WARN not found")
