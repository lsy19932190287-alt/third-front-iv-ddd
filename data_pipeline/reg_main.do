/*========================================================================
   三线建设 Exit-DDD 顶刊研究 — Stata Do-file 模板
   §A.2 Monte Carlo & Empirical Replication Code

   严格按用户2026-10-19指令:
     · 基准与广延边际:  reghdfe y_ihs treat_post, absorb(c#t j#t c#j) vce(cluster c#j)
     · 高维泊松:        ppmlhdfe y_count treat_post, absorb(c#t j#t c#j) vce(cluster c#j) d
     · 工具变量:        ivreghdfe y_ihs (treat_post = z_post), absorb(c#t j#t c#j) cluster(c#j) first
     · 异质性稳健 DID:  csdid 或 did_imputation (Borusyak et al., 2024)

   配套命令 (运行前 install):
     ssc install reghdfe, replace
     ssc install ftools, replace
     ssc install ppmlhdfe, replace
     ssc install ivreghdfe, replace
     ssc install coefplot, replace
     ssc install eventstudyinteract, replace
     net install did_imputation, from("https://kolesarm.github.io/ado/") replace
     ssc install csdid, replace

   外部命令作者:
     · Correia, S., Guimarães, P., Zylkin, T. (2020). ppmlhdfe: Poisson pseudo-maximum
       likelihood regression with high-dimensional fixed effects. Stata Journal.
     · Borusyak, K., Jaravel, X., Spiess, J. (2024). Revisiting Event Study Designs:
       Robust Identification with did_imputation. RES Working Paper.
     · Callaway, B., Sant'Anna, P. (2021). Difference-in-differences with multiple time periods.
       Journal of Econometrics.
========================================================================*/

clear all
set more off
set matsize 11000
set seed 20261019

* ==========================================================================
* 0. 全局设置
* ==========================================================================
global root  "$path/三线建设_empirical"
global data  "$root/data/final"
global out   "$root/output/tables"
global figs  "$root/output/figures"

capture mkdir "$out"
capture mkdir "$figs"

* 加载最终主回归样本 (由 B-1 脚本产出)
use "$data/reg_sample.dta", clear

* 全局变量标识 (与 B-1 映射表对齐)
global county  "county_id"           // 川黔县 ~210
global industry "industry2"          // 二位数行业 30 类
global year    "year"

* 处理变量 (核心): D_cj × Post_t (县-行业-年 三维)
* 严格按 sim_dgp.py 定义: Exit_cj ∈ {0,1} (限 HasTF=1 子集), Post_t = 1{year>=1986}
global treat_post "exit_cj_x_post"
global exit      "exit_cj"
global post      "post"
global tf        "hasTF_cj_1980"

* IV (外生): Z_cj × Post_t
global iv       "z_cj_x_post"

* HSFE
global fe_all   "${county}#${year} ${industry}#${year} ${county}#${industry}"
global cj       "${county}#${industry}"
global ct       "${county}#${year}"
global jt       "${industry}#${year}"

* 控制变量 (按需)
global controls "lnpop_cj pre_gdp_c log_rail_dist"

* 描述统计输出
estpost summarize $treat_post $exit $post $tf lnpop_cj pre_gdp_c ///
                    $iv, detail
esttab using "$out/descstats.tex", replace ///
         cells("count mean sd min p25 p50 p75 max") ///
         title("Descriptive Statistics (Main Sample, 1980-2017)") ///
         label

* ==========================================================================
* Table 4: 基准回归 — Panel A: TWFE-IHS (基准/广延边际)
* ==========================================================================
* (1) 基准 OLS (IHS 变换), 仅加 (c,t)(j,t) 双 FE
reghdfe y_ihs $treat_post ///
        , absorb($ct $jt) vce(cluster $cj)

estadd yscalar, : .
estimates store m_ols_ihs_2fe

* (2) 完整 HDFE: (c,t)(j,t)(c,j) 三组 FE + controls
reghdfe y_ihs $treat_post $controls ///
        , absorb($fe_all) vce(cluster $cj)

estadd yscalar, : .
estimates store m_ols_ihs_full

* (3) [推荐主回归] 完整 HDFE, 无 controls (避免 bad control 偏误),
*     cluster at c×j (与 sim_dgp.py 对齐)
reghdfe y_ihs $treat_post ///
        , absorb($fe_all) vce(cluster $cj) noprint

estadd yscalar, : .
estimates store m_ols_ihs_main

* 输出 Panel A
esttab m_ols_ihs_2fe m_ols_ihs_full m_ols_ihs_main ///
       using "$out/tab4_panelA_ihs.tex", replace ///
       keep($treat_post) ///
       b(%9.4f) se(%9.4f) ///
       star(* 0.10 ** 0.05 *** 0.01) ///
       stats(N r2_within, fmt(%9.0fc %9.4f) labels("Observations" "Within R²")) ///
       title("Panel A: TWFE on arcsinh(Y) --- 基准/广延边际") ///
       mtitles("(2 FE)" "(3 FE+ctrl)" "(3 FE main)") ///
       compress

* ==========================================================================
* Table 4 Panel B: TWFE-LPM (广延边际, 显示退出/进入决策)
* ==========================================================================
* 在广延边际上, P(Y>0) 是核心被解释变量, 处理效应反映"激活效应"
gen y_pos = (y_count > 0)

* (1) LPM 双 FE
reghdfe y_pos $treat_post ///
        , absorb($ct $jt) vce(cluster $cj)
estimates store m_lpm_2fe

* (2) LPM 完整 HDFE [推荐作为广延边际主回归]
reghdfe y_pos $treat_post ///
        , absorb($fe_all) vce(cluster $cj)
estimates store m_lpm_full

esttab m_lpm_2fe m_lpm_full ///
       using "$out/tab4_panelB_lpm.tex", replace ///
       keep($treat_post) ///
       b(%9.4f) se(%9.4f) ///
       star(* 0.10 ** 0.05 *** 0.01) ///
       stats(N r2_within, fmt(%9.0fc %9.4f) labels("Observations" "Within R²")) ///
       title("Panel B: TWFE LPM --- 广延边际 $\Pr(Y>0 \mid D)$") ///
       mtitles("(2 FE)" "(3 FE)") compress

* ==========================================================================
* Table 4 Panel C: 高维泊松 (PPML-HDFE, baseline 主回归)
* ==========================================================================
* Silva & Tenreyro (2006) 推荐用 PPML-HDFE 处理稀疏计数 + 异方差
* Correia, Guimarães, Zylkin (2020) ppmlhdfe 命令直接实现

* (1) 基本 PPML-HDFE (无 controls)
ppmlhdfe y_count $treat_post ///
          , absorb($fe_all) vce(cluster $cj) d
estimates store m_ppml_main

* (2) PPML + controls
ppmlhdfe y_count $treat_post $controls ///
          , absorb($fe_all) vce(cluster $cj) d
estimates store m_ppml_ctrl

* 输出 Panel C (报告弹性 + 标准误)
esttab m_ppml_main m_ppml_ctrl ///
       using "$out/tab4_panelC_ppml.tex", replace ///
       keep($treat_post) ///
       b(%9.4f) se(%9.4f) ///
       star(* 0.10 ** 0.05 *** 0.01) ///
       stats(N, fmt(%9.0fc)) ///
       title("Panel C: PPML-HDFE --- 高维泊松, 增量边际") ///
       mtitles("PPML-HDFE" "PPML+ctrl") ///
       note("'d' option displays in ppml default elasticity format. Cluster at c×j.") ///
       compress

* ==========================================================================
* Table 4 Panel D: IV-DDD via ivreghdfe
* ==========================================================================
* 严格按用户的"线性 IV-DDD"思路:
*   · 一阶段:    D_post = π·Z_post + HDFE + ν
*   · 二阶段:    y_ihs  = β·D̂_post + HDFE + ε
*   · Cluster at c×j  (与 Stata 默认一致)

* [D1] 仅 IV 识别, 无外生控制
* first 选项展示第一阶段 F 统计量
ivreghdfe y_ihs ($treat_post = $iv), ///
          absorb($fe_all) cluster($cj) first
estimates store m_iv_main

* [D2] IV + exogenous controls (pre-trends)
ivreghdfe y_ihs ($treat_post = $iv) $controls, ///
          absorb($fe_all) cluster($cj) first
estimates store m_iv_ctrl

* [D3] IV + 第二个 IV (微观厂址噪声) — overidentification test
*     Z_cj 第二成分: micro_noise_cj (与 Z_cj 互补), 用于 Sargan 检验
gen z_cj_post2 = z_cj_micro * $post
ivreghdfe y_ihs ($treat_post = $iv z_cj_post2) $controls, ///
          absorb($fe_all) cluster($cj) first
estimates store m_iv_overid

* 输出 Panel D
esttab m_iv_main m_iv_ctrl m_iv_overid ///
       using "$out/tab4_panelD_iv.tex", replace ///
       keep($treat_post) ///
       b(%9.4f) se(%9.4f) ///
       star(* 0.10 ** 0.05 *** 0.01) ///
       stats(N, fmt(%9.0fc)) ///
       title("Panel D: 2SLS IV-DDD --- 内生性修正") ///
       mtitles("IV only" "IV+ctrl" "IV+overid") ///
       note("Cluster at c×j. 'first' shows first-stage F stat. 第三列加入第二 IV 做过度识别检验.") ///
       compress

* ==========================================================================
* Table 4 Panel E: 长差分 IV (Lafortune-Rotemberg 估计量备份)
* ==========================================================================
* 直接用1980-1985 vs 2012-2017两端长差分, 避免中段噪声
*   ΔY = β·ΔExit + ΔFE + u
* 其中 HasTF 为外生IV → 这就是 Rothenberg 经典 "long diff" 策略

preserve
    collapse (firstnm) y_count_85 = y_count y_count_12 = y_count ///
             (firstnm) exit_85 = $exit exit_12 = $exit ///
             (firstnm) tf_85 = $tf z_cj_85 = z_cj ///
             (firstnm) county_id industry2, ///
             by($county $industry)

    * 长差分构造
    gen d_y     = y_count_12 - y_count_85
    gen d_exit  = exit_12   - exit_85

    * 长差分工具变量 (1980年的微观地形)
    gen d_iv    = z_cj_85
    keep if tf_85 == 1

    * 2SLS: ΔY = β·ΔExit on county FE (no longer t-varying since pooled)
    ivreghdfe d_y (d_exit = d_iv), absorb($county $industry) cluster($cj)
    estimates store m_longdiff_iv
restore

* ==========================================================================
* Table 5: 异质性稳健 DID (csdid / did_imputation)
* ==========================================================================
* 用户点名"异质性稳健 DID (csdid 或 did_imputation, Borusyak et al., 2024)"
* 因为三线调整撤并是滚动发生 (不同县撤并年份不同), 用经典 TWFE 会出现
* Goodman-Bacon (2021) 类型的偏误.

* ----- Approach 1: did_imputation (Borusyak, Jaravel, Spiess 2024) -----
* 把 Exit_cj × Post 当作单个静态处理, 让 TWFE 提供 imputation weights
* 标准语法 (Borusyak et al. 2024 RES):
*   1) 构造个体 ID (县×行业) egen cj_id = group(county_id industry2)
*   2) 构造首次撤并年份 (从未撤并的样本必须设为缺失值 .) gen ei = exit_year if exit == 1
*   3) 主体回归: did_imputation y_ihs cj_id year ei, fe(county_id#year industry2#year cj_id) cluster(cj_id)

* 准备 did_imputation 所需变量
* 县×行业 ID
capture drop cj_id
egen cj_id = group($county $industry)
* 首次撤并年份 (从未撤并的样本设为缺失, 且必须是 cj_id 内不随时间变化的恒量)
capture drop ei
bysort cj_id ($year): gen ei = $year if $treat_post == 1
bysort cj_id: egen ei_first = min(ei)
replace ei = ei_first
drop ei_first

* 静态 ATT 估计: fe (unit + time FE, 不含线性趋势)
did_imputation y_ihs cj_id $year ei, /// fe($county##$year $industry##$year cj_id) cluster($cj) horizons(0/15) pretrends(6) minn(0)
estimates store m_did_impute_fe

* 静态 ATT 估计: fe_t (unit FE + 单元特定线性时间趋势)
* 注: Borusyak et al. (2024) did_imputation 官方语法不支持 trends() 选项;
*     改用 reghdfe 加手动构造的 (cj_id × year) 线性趋势项
reghdfe y_ihs i.cj_id#c.year, /// absorb($county##$year $industry##$year cj_id) cluster($cj) keep(1.cj_id#c.year) noprint
estimates store m_did_impute_fet

* 静态 ATT 估计: did_imputation (Borusyak 推荐无偏估计量, 含动态效应)
* 注: did_imputation 官方语法不支持 eventstudy 选项, 但 horizons(0/15) pretrends(6) 会自动输出动态系数
did_imputation y_ihs cj_id $year ei, /// fe($county##$year $industry##$year cj_id) cluster($cj) horizons(0/15) pretrends(6) minn(0) savefirst($out/did_impute_first)
estimates store m_did_impute_event

* ----- Approach 2: csdid (Callaway & Sant'Anna 2021) -----
* 视不同 (c,j) 的首次撤并年份为分组, 估计 ATT(g,t)
* 注: csdid 要求数据预处理 — 安装 callaway-santanna
*ssc install csdid, replace

* 若为单次统一处理 (Post=1986), csdid 退化为 2x2 DID with cohort=g
csdid y_count, ivar($county##$industry) time($year) ///
       gvar($post) agg(event) notyet ///
       cluster($cj)
estimates store m_csdid_event

esttab m_did_impute_fe m_did_impute_fet m_csdid_event ///
       using "$out/tab5_robust_did.tex", replace ///
       b(%9.4f) se(%9.4f) ///
       star(* 0.10 ** 0.05 *** 0.01) ///
       stats(N, fmt(%9.0fc)) ///
       title("Table 5: 异质性稳健 DID 估计量 (Borusyak \& Callaway B-S)") ///
       mtitles("did_imp FE" "did_imp FEt" "csdid event") ///
       note("did_imputation estimators: fe (仅横截面), fe_t (横截面+时间 trend). csdid 用首次撤并为 cohort, ATT 估计.") ///
       compress

* ==========================================================================
* Figure 4: Event Study Plot (coefplot)
* ==========================================================================
* 用 ivreghdfe + leads/lags 或 eventstudyinteract 估计动态效应

* ---- A. Standard TWFE event study (含偏误, 仅作 sanity check) ----
* 围绕 Post=1986 取 ±10 年 leads/lags
gen event_time = $year - 1986
forvalues k = -10(1)10 {
    capture drop l`k'
    gen l`k' = (event_time == `k')
    local lead_lag_`k' "l`k'"
}
* 漏掉基期 (-1)
drop l_1 /* syntax fix: drop pre-defined */
local ll "l-10 l-9 l-8 l-7 l-6 l-5 l-4 l-3 l-2 l0 l1 l2 l3 l4 l5 l6 l7 l8 l9 l10"

reghdfe y_count `ll' ///
        , absorb($fe_all) vce(cluster $cj) noprint
* 注意: 基期 = t=-1 被 omit

coefplot, keep(l-10 l-9 l-8 l-7 l-6 l-5 l-4 l-3 l-2 l0 l1 l2 l3 l4 l5 l6 l7 l8 l9 l10) ///
         coeflabels(l-10 = "-10" l-9 = "-9" l-8 = "-8" l-7 = "-7" ///
                    l-6 = "-6" l-5 = "-5" l-4 = "-4" l-3 = "-3" ///
                    l-2 = "-2" l0 = "0" l1 = "1" l2 = "2" ///
                    l3 = "3" l4 = "4" l5 = "5" l6 = "6" ///
                    l7 = "7" l8 = "8" l9 = "9" l10 = "10") ///
         vertical ///
         yline(0) ///
         title("Figure 4a: Standard TWFE Event Study (含负权重偏误, sanity only)") ///
         xtitle("Event time (Years from Post=1986)") ///
         ytitle("Coefficient on $treat_post") ///
         ci(95)

graph export "$figs/fig4a_twfe_event.pdf", replace

* ---- B. did_imputation event study (Borusyak 推荐, 无偏) ----
* 用已经构造的 cj_id 和 ei 变量
* 注: did_imputation 官方语法不支持 eventstudy 选项, 写 horizons(0/15) pretrends(6) 即可自动输出动态系数
did_imputation y_ihs cj_id $year ei, fe($county##$year $industry##$year cj_id) cluster($cj) ///
                pretrends(6) horizons(0/15) minn(0)

eventstudy_plot, stub_lead(event_t_m) stub_post(event_t_p) ///
                together ///
                ra(0.05) ci(95) ///
                title("Figure 4b: did_imputation Event Study (Borusyak 推荐)") ///
                xtitle("Event time (Years from Post=1986)") ///
                ytitle("ATT(g,t)")

graph export "$figs/fig4b_did_impute_event.pdf", replace

* ---- C. ivreghdfe event study (主回归, 含 IV-DDD 动态) -----
iv_event y_ihs $iv, ///
          absorb($fe_all) cluster($cj) ///
          pre(10) post(15) ///
          generate
* 注: iv_event 命令需要安装. 用户可改用 eventstudyinteract.

* ==========================================================================
* Table 6: Robustness Suite (按用户惯例 §6)
* ==========================================================================

* ---- R1: 排除重庆直辖 (1997) 前后 3 年窗口 ----
preserve
    drop if inrange($year, 1994, 2000)
    reghdfe y_ihs $treat_post, absorb($fe_all) vce(cluster $cj)
    estimates store m_rob_noChongqing
restore

* ---- R2: 仅保留撤并前 5 年 + 后 10 年样本, 排除 1978-1980 早期稀疏 ----
preserve
    keep if inrange($year, 1975, 2005)
    reghdfe y_ihs $treat_post, absorb($fe_all) vce(cluster $cj)
    estimates store m_rob_window
restore

* ---- R3: 用注册资本 regfee 当 outcome (用户建议) ----
reghdfe ln_regfee $treat_post, absorb($fe_all) vce(cluster $cj)
estimates store m_rob_regcap

* ---- R4: 限定 HSFE 集 - 去掉 (c,j) FE, 仅 (c,t)+(j,t) ----
reghdfe y_ihs $treat_post, absorb($ct $jt) vce(cluster $cj)
estimates store m_rob_2fe

* ---- R5: 替代 cluster: cluster(c) 单层 ----
reghdfe y_ihs $treat_post, absorb($fe_all) vce(cluster $county)
estimates store m_rob_cluster_c

* ---- R6: 三位编码行业 (调整 GB/T 4754-2011, 留作 future work) ----
*  (需先用 B-1 脚本中的 GB/T 4754 跨期映射)

esttab m_ols_ihs_main m_rob_noChongqing m_rob_window ///
       m_rob_regcap m_rob_2fe m_rob_cluster_c ///
       using "$out/tab6_robust.tex", replace ///
       keep($treat_post) ///
       b(%9.4f) se(%9.4f) ///
       star(* 0.10 ** 0.05 *** 0.01) ///
       stats(N, fmt(%9.0fc)) ///
       title("Table 6: Robustness Suite --- 主回归 (\textbf{Panel A}) + 稳健性 (\textbf{Panels B-G})") ///
       mtitles("Main" "No Chongqing" "Window" "Regcap" "2FE" "Cluster c") ///
       compress

* ==========================================================================
* §3 Monte Carlo Simulation 复现 (用户 §3.4 仿真表)
* ==========================================================================
* 调用外部 Python 脚本 (v3 sim_runner.py), 在 Stata 中读入结果
shell python "F:/三线建设/sim/sim_runner.py" --n-reps 100 ///
       --seed 20261019 --endog 0.5 ///
       --out "F:/三线建设/sim/tables/mc_sim_results.json"

frame copy default sim_frame, replace
frame change sim_frame
import json "F:/三线建设/sim/tables/mc_sim_results.json", ///
         cases(lower)

* 报告仿真结果
list metrics, clean
frame change default

* ==========================================================================
* §附录 B: 数据诊断检验
* ==========================================================================

* 平行趋势检验 (DID 关键前提)
reghdfe y_ihs l-10 l-9 l-8 l-7 l-6 l-5 l-4 l-3 l-2 l0 l1 l2 l3 l4 l5 l6 l7 l8 l9 l10 ///
        , absorb($fe_all) vce(cluster $cj) noprint

test l-10 l-9 l-8 l-7 l-6 l-5 l-4 l-3 l-2   // 联合 F 检验: 处理前是否显著 ≠ 0
display "Pre-trends F-test p-value: " r(p)

* Placebo test: 假处理=1975, 真实=1986
gen placebo_post = ($year >= 1975 & $year < 1986)
gen placebo_treat = $exit * placebo_post
reghdfe y_ihs placebo_treat ///
        if inrange($year, 1970, 1985), ///
        absorb($fe_all) vce(cluster $cj)
* 若 placebo_treat 系数显著 ≠ 0, 说明存在 prior trends 的识别问题

* ==========================================================================
* 结束
* ==========================================================================
display "============================================================="
display "Table 4 & 5 完毕. 输出到 $out/ 和 $figs/"
display "============================================================="
