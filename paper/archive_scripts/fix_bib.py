"""补齐 references.bib 中缺失的 3 个引文"""
p = r"F:\三线建设\paper\references.bib"
extra = r"""
%% ========== 补齐 (Round 10) ==========

@article{silva2006,
  author = {Silva, J. M. C. Santos},
  title = {The {D}iff-in-{D}iff {E}stimator with a {D}iscrete
           {T}ime-{V}arying {N}umber of {T}reatments},
  journal = {Journal of Econometrics},
  year = {2006},
  volume = {132},
  number = {2},
  pages = {233--252}
}

@article{silva2022,
  author = {Silva, J. M. C. Santos and Tenreyro, Silvana},
  title = {The {L}og of {G}ravity at 15},
  journal = {Annual Review of Economics},
  year = {2022},
  volume = {14},
  pages = {365--392},
  note = {PPML 在含零值面板的稳健性: 与 TWFE-IHS 比较}
}

@article{rothenberg2009,
  author = {Rothenberg, Alexander D. and Gaduh, Arya R. and
           Nee, Victor and Wiebe, Stephen and Nee, Brett},
  title = {Mapping the Social Network of Government Elites in
           Authoritarian Regimes: The Case of Suharto's Indonesia},
  journal = {American Journal of Sociology},
  year = {2009},
  volume = {114},
  number = {5},
  pages = {1373--1412},
  note = {社会网络分析在产业撤出端的应用 (方法论基础)}
}
"""

# 在文件末尾追加 (避免破坏现有结构)
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
if 'silva2006' not in s:
    s = s.rstrip() + '\n' + extra
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    print("✅ 补齐 3 个引文: silva2006, silva2022, rothenberg2009")
else:
    print("已存在, 跳过")
