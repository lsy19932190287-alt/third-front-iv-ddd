"""把所有一次性 debug 脚本从 paper/ 移到 archive_scripts/"""
import os
import shutil

PAPER_DIR = r'F:\三线建设\paper'
ARCHIVE_DIR = os.path.join(PAPER_DIR, 'archive_scripts')

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 一次性 debug 脚本前缀/精确文件名 (这些都已经完成使命)
DEBUG_NAMES = [
    # 1) check_*.py — 各种 .tex 段落/标签/页码检查
    'check_137.py', 'check_cites.py', 'check_crlf.py', 'check_final.py',
    'check_labels.py', 'check_labels2.py', 'check_p10.py',
    'check_pass1.py', 'check_pass10.py', 'check_pass1_detail.py',
    'check_pass2.py', 'check_pass3.py', 'check_pass4.py', 'check_pass5.py',
    'check_pass6.py', 'check_pass7.py', 'check_pass8.py', 'check_pdf.py',
    'check_remaining.py', 'check_tab3.py', 'check_tab4.py', 'check_tab4_raw.py',
    # 2) dump_*.py — 输出 .log/.tex 片段
    'dump_errors.py', 'dump_pass2.py', 'dump_pass3.py',
    # 3) find_*.py — 文本定位
    'find_137.py', 'find_l200.py', 'find_textit.py', 'find_unmatched.py',
    # 4) fix_*.py — 一次性 fix 脚本 (29 个)
    'fix_137.py', 'fix_137_v2.py', 'fix_137_v3.py', 'fix_2019.py',
    'fix_3_hard_bugs.py', 'fix_amp.py', 'fix_amp2.py', 'fix_bib.py',
    'fix_bracket.py', 'fix_crlf.py', 'fix_crlf_v2.py', 'fix_did_imp.py',
    'fix_l200.py', 'fix_latex_errors.py', 'fix_multicol.py', 'fix_n_line.py',
    'fix_pass4.py', 'fix_quad.py', 'fix_sec05.py', 'fix_sec05_v2.py',
    'fix_starscript.py', 'fix_tables.py', 'fix_textit.py', 'fix_textit_v2.py',
    'fix_undef.py',
    # 5) peek_*.py — 文件片段读取
    'peek_lines.py', 'peek_lines2.py', 'peek_sec05.py', 'peek_sec05_425.py',
    'peek_tab2.py',
    # 6) raw_*.py — 原始文本处理
    'raw_fix.py',
    # 7) update_*.py — 单次更新脚本
    'update_remaining.py', 'update_sec04_text.py', 'update_sec05_main_text.py',
    # 8) final_update.py — 同上
    'final_update.py',
    # 9) verify_*.py — 单次验证
    'verify_final.py', 'verify_final_v2.py', 'verify_run1.py',
    # 10) clean_quotes.py / remove_resizebox.py — 一次性清理
    'clean_quotes.py', 'remove_resizebox.py',
]

moved = 0
not_found = []
for name in DEBUG_NAMES:
    src = os.path.join(PAPER_DIR, name)
    if os.path.exists(src):
        dst = os.path.join(ARCHIVE_DIR, name)
        # 如果目标已存在, 跳过 (避免覆盖)
        if os.path.exists(dst):
            print(f'  [skip] {name} (target exists in archive)')
            continue
        shutil.move(src, dst)
        moved += 1
    else:
        not_found.append(name)

print(f'\n✓ 已移动 {moved} 个一次性 debug 脚本 → archive_scripts/')
if not_found:
    print(f'  注意: 找不到 {len(not_found)} 个 (可能已被前次清理):')
    for n in not_found[:5]:
        print(f'    - {n}')
    if len(not_found) > 5:
        print(f'    ... 还有 {len(not_found)-5} 个')

# 列出 paper/ 剩余的 .py
print('\n--- paper/ 目录剩余 .py 脚本 ---')
remaining = sorted(f for f in os.listdir(PAPER_DIR) if f.endswith('.py'))
for f in remaining:
    print(f'  • {f}')
if not remaining:
    print('  (无 — 所有 .py 都已归档)')

print(f'\n--- archive_scripts/ 当前共 {len(os.listdir(ARCHIVE_DIR))} 个文件 ---')