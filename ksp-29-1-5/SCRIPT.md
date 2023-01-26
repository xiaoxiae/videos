---
title: <title>
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

---
INTRODUCTION
---

\marginpar{\texttt{Intro}}
Lučištníci stojící v řadě mají vyhlédnuté své cíle.
Každý z nich míří lukem na nějaké místo, do kterého by rád vyslal svůj šíp, ale je nebezpečné, aby všichni stříleli najednou.
Měli by proto střílet pouze ti, jejichž dráhy palby se nekříží.

Tohle jsou některé přípustné kombinace lučištníků, kde se dráhy palby nekříží, a tohle nějaké nepřípustné.

Vaším cílem je vymyslet algoritmus, který ze všech lučištníků vybere co největší skupinu, jejíž dráhy střelby se nekříží -- jak na to?

To nejpřímočařejší řešení (vyzkoušení všech možností) je nepřekvapivě dost pomalé -- skupin je celkově $2^n$ (každý lučištník může nebo nemusí střílet), což je i pro malá $n$ příliš mnoho.

K rychlejšímu řešení provedeme jednoduché pozorování: nejlepší možné řešení končící daným lučištníkem je rozšířením nejlepšího řešení nějakého jeho předchůdce.
Pokud tedy máme nejlepší řešení pro všechny předchůdce již spočítané, k rozšíření pro dalšího lučištníka je stačí všechna vyzkoušet a zvolit to nejlepší.

Začneme-li tedy od začátku, tak pro každou šipku stačí projít všechny jí předcházející, kterých je celkově $0$ + $1$ + $2$ + $3$ až + $n - 1$.
Součet této řady je řádově $n^2$, což je výrazně lepší než $2^n$, ale řešení stále není optimální.
Jak ho můžeme zrychlit?

TODO: optimální řešení
