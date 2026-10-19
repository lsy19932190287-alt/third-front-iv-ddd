# third-front-iv-ddd

川黔两省 1964–1980 年「三线建设」对企业长期发展影响的实证研究。

本仓库复现论文：
**《三线建设、撤离调整与幸存企业成长——来自川黔 92 家三线企业的 Exit-DDD 证据》**

## 研究问题

1980 年代初的"三线建设调整"对留下来的三线企业产生了怎样的长期影响？
本文用川黔两省 92 家三线企业 + 长三角对照企业的县-行业-年面板，
通过退出-三重差分（Exit-DDD）+ Bartik IV-DDD 估计调整撤并的因果效应。

## 目录结构

```
.
├── data_pipeline/        # 数据处理 pipeline（CSV / JSON / Python 脚本）
│   ├── 01_raw/           # 原始公开数据（手工整理）
│   ├── 02_clean/         # 清洗后 CSV
│   ├── 03_panel/         # 县-行业-年 panel 构建
│   ├── 04_reg/           # 回归用面板
│   ├── 05_iv/            # Bartik IV 构建
│   └── *.py              # 阶段脚本
├── paper/                # LaTeX 论文
│   ├── main.tex          # 主文件
│   ├── references.bib    # BibTeX
│   ├── sec01_intro.tex … sec08_conclusion.tex
│   ├── tables/           # 实证表格（.tex / .csv）
│   └── figures/          # 图表（fig1_event_study 等）
└── sim/                  # Monte Carlo 仿真（§3 验证 IV-DDD 设定）
    └── *.py
```

## 复现流程

### 数据 pipeline
```bash
cd data_pipeline
python 03_panel_build.py    # 县-行业-年面板构建
python 04_iv_build.py       # Bartik 工具变量构建
python 05_reg.py            # Exit-DDD / IV-DDD 主回归
```

### Monte Carlo 仿真
```bash
cd sim
python iv_ddd_montecarlo.py --n_sim 100
```

### 编译论文
```bash
cd paper
xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex
```

## 核心方法

- **Exit-DDD**：处理组 = 三线企业所在县-行业；政策 = 1980s 调整撤并退出事件；对照组 = 长三角未受调整影响企业
- **IV-DDD**：用 1964 年三线企业分布 × 1980s 行业增长冲击作为 Bartik IV
- **Hansen J 排他性检验**：HasTF=1 子样本的 IV-DDD-2SLS 过度识别检验
- **HDFE + 2SLS 残差化**：消除高维固定效应（N_c × N_j × N_t）下的多重共线

## 依赖

```
python>=3.10
pandas>=2.0
numpy>=1.24
statsmodels>=0.14
linearmodels>=4.27     # IV/2SLS 面板回归
matplotlib>=3.7
```

## 数据说明

- **川黔两省 92 家三线企业**：手工整理自 1964-1980 三线建设档案 + 四川省志 / 贵州省志
- **长三角对照组**：手工收集的同期上海、江苏、浙江非三线国有工业企业
- **行业分类**：GB/T 4754 国民经济行业分类大类（30 个）

> 注：`.dta` 中间数据已 `.gitignore` 排除，可由 `data_pipeline/` 下的脚本从 CSV 重新生成。

## License

本仓库仅供学术研究使用，数据如需引用请联系作者。
