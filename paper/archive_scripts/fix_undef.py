"""修复 sec:mech / sec:concl / tab:longdiff undefined refs"""

# sec01: \\ref{sec:mech} -> \\ref{sec:conclusion}, \\ref{sec:concl} -> \\ref{sec:conclusion}
p = r"F:\三线建设\paper\sec01_intro.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace("\\ref{sec:mech}", "\\ref{sec:conclusion}")
s = s.replace("\\ref{sec:concl}", "\\ref{sec:conclusion}")
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("✅ sec01 修复 sec:mech/sec:concl -> sec:conclusion")

# sec05: \\ref{tab:longdiff} -> \\ref{tab:robust}
p = r"F:\三线建设\paper\sec05_robustness_conclusion.tex"
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace("\\ref{tab:longdiff}", "\\ref{tab:robust}")
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print("✅ sec05 修复 tab:longdiff -> tab:robust")