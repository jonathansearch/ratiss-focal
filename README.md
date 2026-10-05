<div align="center">

<img src="images/logo-ratiss-labs.png" width="220" alt="RATISS Labs"/>

# 🎯 RATISS-FOCAL — Informational Focusing

**Does coherence emerge from information? This project says: do not speculate; measure.**

[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-94-teal.svg)](PROTOCOLES.md)
[![Versions](https://img.shields.io/badge/unifications-v1%E2%80%93v13-teal.svg)](UNIFICATION.md)
[![Stack](https://img.shields.io/badge/stack-numpy%20%2B%20ripser-teal.svg)](organes/)
[![Neurons](https://img.shields.io/badge/neurons-zero-orange.svg)](organes/)

*By **RATISS Labs** — Jonathan Evina · MIT License · public reproducibility intended*

</div>

<img src="images/hero-focal.jpg" width="100%" alt="Focusing: from diffuse to coherent point"/>

> **Abstract (EN).** *Does coherence emerge from information? RATISS-FOCAL is an open experimental program (69 pre-registered computational tests plus 15 open explorations, 13 unification releases) probing whether coherent structure can arise from pure information — with zero neurons. Three sectors are characterised: **G** (informational gravity: plastic, scarring, saturating on an absolute core of 0.083), **Q** (quantum memory: an anti-persistent continuum, phase-steerable), and **U** (primitive entanglement: a sanctuary robust to discrete shocks, eroding past ambient noise σc = 0.06, irreversibly). Every equation ships with its test. Failures are published, never hidden. MIT.*

> **Count note:** the source README uses several totals: the badge says 94 tests; the abstract says 69 pre-registered tests plus 15 open explorations; an earlier section refers to 63 tests; later phases include TEST-64 through TEST-94. The source numbers are retained as reported and should be reconciled before publication.
>
> **Evidence note:** most results below are outputs of the project's computational model. The source calls some sections “real data”; that wording is not taken here to mean physical measurements. Hardware results are separately identified as source-reported QPU bridges and should be checked against their job records.

---

## 📖 Contents

1. [The question](#-the-question)
2. [The three pillars: G, Q, U](#-the-three-pillars-g-q-u)
3. [Major results (model outputs and reported hardware results)](#-major-results-model-outputs-and-reported-hardware-results)
4. [Method: preregistered rigor](#-method-preregistered-rigor)
5. [Repository architecture](#-repository-architecture)
6. [Quick start](#-quick-start)
7. [Map of the versions](#-map-of-the-versions)
8. [Research directions](#-research-directions)
9. [Reading order](#-reading-order)
10. [Phase 17: explorations](#-phase-17-explorations-probe-uktz-ruq-test-6472)
11. [Phase 18: V13 singularity](#-phase-18-v13-singularity-test-7378)
12. [Phase 19: QM–GR coexistence](#-phase-19-qmgr-coexistence-test-7989)
13. [Phase 20: LINK — search for the fold](#-phase-20-link-search-for-the-fold-test-9093--closed-berry-loop)
14. [Phase 21: QM–GR synthesis](#phase-21-qmgr-synthesis-test-94)
15. [Citation, author, and license](#-citation-author-and-license)

---

## ❓ The question

> **Does coherence emerge from information?**

Not from matter. Not from neural computation. From **information itself**: points, links, and concentrations observed through a topological microscope (persistent homology), without a single neuron.

The project proposes that if coherent structure **appears, persists, and resists destruction** in this minimal setting, coherence may be a property of information rather than an accident of complexity. This is a research hypothesis, not an established result about information or consciousness.

The repository says the question was posed repeatedly, with criteria written **before** each measurement and both positive and negative responses published. Its counts differ across sections; see the count note above.

## 🔱 The three pillars: G, Q, U

<img src="images/concept-gqu.jpg" width="100%" alt="G erodes, Q oscillates, U persists"/>

| Sector | Model description | Behaviour reported by the project |
|---|---|---|
| **G** — informational gravity | Contraction `α` of a point torus | **Plastic and mortal:** collapses at the first shock (0.345→0.097), decays slowly (`τ ≈ 400` steps), and is reported to saturate at an absolute core of 0.083. It retains scars. |
| **Q** — quantum memory (Kuramoto ring) | Synchronisation of 24 oscillators | **Anti-persistent “weathervane”:** no attractors; continuum [0.76, 0.91]; symmetric counter-flip at each shock; reportedly controllable at `P = 1.0` by an injected absolute phase. The shock “blanches” it (entropy reset), after which it regenerates in the model. |
| **U** — primitive entanglement | Invisible line: non-geometric coincidences | **Conditional sanctuary:** reportedly unchanged under 7 cumulative shocks (28/30, Δ = 0) while G falls by 72%, but sensitive to ambient noise at `σc = 0.06` (sigmoid `R² = 0.964`), with a partial floor of ~30% and irreversible erosion. The project interprets it as reading noise *texture*, not only its magnitude. |

**In one sentence (project metaphor):** G is the mortal substrate, Q the regenerative memory, and U the persistent thread — while the environment remains below `σc`.

## 📊 Major results (model outputs and reported hardware results)

The source says the figures below are generated from the repository's result JSON files using `images/make_figs.py`.

### 1. The U sanctuary has a threshold: `σc = 0.06`

<img src="images/plot_sanctuaire.png" width="100%" alt="S_U(sigma): plateau followed by sigmoid erosion, threshold 0.06"/>

- **TEST-49:** 28/30 unchanged across 7 cumulative shock levels (Δ = 0) → described as an absolute sanctuary against trauma.
- **TEST-58:** scan `σ ∈ [0.01, 0.10]` → sigmoid `R² = 0.964`, `σc = 0.06`, plateau 29/30→21/30.
- **TEST-61:** no disappearance up to `σ = 0.30` (floor ~30% vs. ~16% control), but erosion is reported as **irreversible**.
- **TEST-62:** at identical `σ`, HIGH structure carries U at +2/+4 → interpreted as **U reading noise texture**.

### 2. G saturates at an absolute core: `0.083`

<img src="images/plot_escalier_H3.png" width="100%" alt="G staircase: drop then H3 saturation, absolute core 0.083"/>

- **TEST-48:** 6 cumulative shocks → saturating H3, `R² = 0.978`, `Gmin(N) = 0.083 + 0.26·e^(−3N)` (source-reported model fit).
- The source says the first shock causes most of the collapse; later shocks vary within `[0.06, 0.11]`.
- H1 (linear) and H2 (exponential) were **rejected** by the repository's tests; no collapse to zero was observed in that model.

### 3. Q's flip follows phase: `P = 1.0`

<img src="images/plot_flip_phase.png" width="100%" alt="Control map: injected phase controls HIGH/LOW at P=1.0"/>

- **TEST-60:** `φ_inj ∈ [0, π]` → LOW; `φ ∈ {5π/4, 3π/2}` → HIGH; **`P = 1.0` in both pre-shock branches** (described as controllable, 14/16).
- `7π/4` is described as a transition zone (ambiguous 50%): the control boundary is visible.
- The project says anti-persistence has a control input: the **absolute phase** (symmetry broken by spatial anchors).

### 4. Q has no attractors: bistability rejected

<img src="images/plot_continuum_Q.png" width="100%" alt="Q-final histogram, n=40: continuum without a gap"/>

- **TEST-50** (`n = 6`) suggested bistability at 0.78/0.87 → **TEST-52** (`n = 40`) rejects it: continuum `[0.76, 0.91]`, maximum gap 0.018 (described as monostable).
- **TEST-53:** `P_switch = 1.0` at only `0.25×` standard intensity → described as a basin without depth.
- **TEST-56:** symmetric flip (HIGH→0.77, LOW→0.84) → no drift and no `Q̄` equilibrium.
- *Lesson in the source: replicate before naming.*

### Other reported model laws

| Project law/model | Test | Reported result |
|---|---|---|
| `G(α, σ, N) = exp(−0.29 − 7.16α − 6.59σ + 0.0012N)` floor | TEST-40 | `R² = 0.920` |
| Double-exponential G reconstruction, `τ_slow ≈ 400` steps, true floor 0.095 | TEST-46 | `R² = 0.902` |
| Double-exponential Q synchronisation (`k₁ = 0.098` fast, `k₂ = 0.001` slow) | TEST-36 | `R² = 0.968` |
| Structured Q volatility (slope −0.72, `ac1` 0.63) | TEST-37 | Reported as signal, not noise |
| Proximity–condensation (`ρc = 8.01` extracted, not assumed) | TEST-27 | Synchronisation 0.98 vs. 0.11 |
| Post-collapse resilience (links: `R = 1.023` absolute) | TEST-28/25 | Described as actual purification |

## 🔬 Method: preregistered rigor (as described by the project)

The source says the distinction is not that the repository is necessarily right, but that its tests are designed to make post-hoc adjustment visible:

1. **Criterion written before measurement.** Every TEST declares its success rule in its docstring *before* execution; the threshold is not adjusted afterward.
2. **Falsifiability required.** Each test documents at least two possible outcomes (e.g., SANCTUARY / SATELLITE / COLLAPSED). A test that cannot fail is disallowed.
3. **Failures published.** Partial scores such as 1/3 and 2/3 are retained. Rejected hypotheses (bistability, entropy bias, catastrophic rupture, low-pass filter, H1/H2, etc.) are listed in `tickets/CONSOLIDATION_V1-V12.md`; the source says not to reopen them without new evidence.
4. **No metric fishing.** Protocol changes (M1→M26) are declared, dated, and justified; the source says criteria are never rewritten just to pass (see TEST-61: MIXED result retained).
5. **Zero neurons.** `numpy + ripser` are listed as sufficient. If coherence emerges in this model, it does not depend on deep learning.
6. **Public reproducibility as credibility.** MIT license, data + code + log, and fixed random seeds throughout (as stated in the source).

## 🗂️ Repository architecture

<img src="images/schema-pipeline.svg" width="100%" alt="Pipeline: container, capacitor, carriers, universes A/B, measurement thread, G/Q/U sectors"/>

```
ratiss-focal/
├── README.md                  ← current overview
├── FORMALISATION.tex          ← canonical document (each equation linked to its TEST)
├── THEORIE-UNIFIEE.md         ← consolidated theory A→K
├── UNIFICATION.md             ← register of versions (v1→v12, scores)
├── PROTOCOLES.md              ← TEST procedures, criteria, and results (source says 63)
├── JOURNAL.md                 ← dated log, including reported errors
├── QUESTIONS-OUVERTES.md      ← closed and open questions (V13 directions subject to approval)
├── ROADMAP.md                 ← phases (V12 closure: strategic pause, in source)
├── SPEC-EXP-FOCAL-01.md       ← initial experiment protocol
├── GLOSSAIRE.md               ← lab vocabulary
├── LICENSE                    ← MIT
├── experiences/               ← exp01_*.py … exp63_*.py (executed code, fixed seeds)
│   └── resultats/             ← expNN.json (raw data for each test)
├── organes/                   ← container, carriers, measurements (numpy + ripser)
├── univers/                   ← A.json, B.json, unifie.json … unifie_v12.json
├── resultats/                 ← public mirror of JSON files (remote repository root)
├── tickets/                   ← structural questions (open/closed + rationale)
└── images/                    ← logo, hero, diagrams, figures (`make_figs.py`)
```

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/jonathansearch/ratiss-focal.git
cd ratiss-focal

# 2. Dependencies (lightweight: no GPU, API key, or accelerator)
pip install numpy ripser matplotlib

# 3. Reproduce one test (e.g. U sanctuary threshold, ~1 minute)
cd experiences && python3 exp58_courbe_U.py

# 4. Reproduce a full version (e.g. V12, ~10 minutes)
python3 exp60_forcage_flip.py && python3 exp61_rupture_U.py \
  && python3 exp62_flip_erosion.py && python3 exp63_unification_v12.py

# 5. Regenerate the README figures
cd ../images && python3 make_figs.py
```

> ⚠️ **Known runtimes in the source:** TEST-46/48 (1,000 G steps × shocks) ≈ 5 min/shock; TEST-57 (`n = 200`) ≈ 3 min. Everything else reportedly runs in seconds. Fixed seeds are said to make results bit-reproducible on the same machine and minor dependency versions.

## 🗺️ Version map

| Version | Tests | Score | Contribution listed in source |
|---|---|---:|---|
| v1–v4 | 01–29 | Foundations | Container, carriers, sibling universes A/B, two laws (V4: 2/2) |
| v5 | 30–35 | **3/5** | Partial unification, Q residual honestly identified |
| v6 | 36–39 | **3/3** | Q revealed: double exponential, structured volatility, robust line |
| v7 | 40–43 | **3/3** | G core: logF law, coupled collapse, plastic shock |
| v8 | 44–47 | **2/3** | Q blanching (low-pass hypothesis rejected), U sanctuary, true floor 0.095 |
| v9 | 48–51 | **3/3** | Absolute core 0.083 (H3), U across 7 shocks, Q “bistability” |
| v10 | 52–55 | **1/3** | Bistability rejected (continuum, n=40), fragile basin, correlated Q/U Δ=3 |
| v11 | 56–59 | **2/3** | Symmetric flip (M25), rebellious distribution, **σc = 0.06** (sigmoid) |
| v12 | 60–63 | **1/3** | **Controllable flip, P=1.0** (M26), irreversible U floor, texture coupling |
| **⛔ closure** | — | — | Consolidation, tickets closed, strategic pause (Phase 16, as stated) |

Details: [`UNIFICATION.md`](UNIFICATION.md) · Protocols: [`PROTOCOLES.md`](PROTOCOLES.md) · Closure summary: [`tickets/CONSOLIDATION_V1-V12.md`](tickets/CONSOLIDATION_V1-V12.md)

## 🌅 Research directions described in the source

**Fundamental research**
- A **minimal model of persistence**: what in an information system survives destruction, and under which quantified conditions (`σc`, absolute core, irreversibility)?
- A **probe of information quality**: `σc` and noise texture as environmental metrics potentially transferable to signal/noise systems.
- A possible bridge to **consciousness theory** (the sanctuary ticket is marked closed): persistence of the Thread (U) vs. regeneration of memory (Q) vs. mortality of the substrate (G), on a formal basis. This is a proposed analogy, not evidence about consciousness.

**Applied research (Phase 17, subject to approval in source)**
- Controllable anti-persistent memories (phase-driven flip: deterministic writing without an attractor).
- Entanglement channels decoupled from geometry (an “invisible line”: sharing without contact).
- Preregistered robustness criteria that may be applied to AI-system evaluation.

**Epistemology**
- The source argues that publishing refutations (six abandoned hypotheses, versions with 1/3 scores) produces a stronger theory than confirmation-seeking.
- `JOURNAL.md` is described as showing doubt, errors (metric-fishing nearly occurred in TEST-61), and corrections as material for scientific trust.

## 📚 Reading order

1. [`FORMALISATION.tex`](FORMALISATION.tex) — canonical document (compile with `pdflatex` or Overleaf).
2. [`UNIFICATION.md`](UNIFICATION.md) — the versions in about 10 minutes.
3. [`PROTOCOLES.md`](PROTOCOLES.md) — tests one by one (the source says 63 in this document).
4. [`THEORIE-UNIFIEE.md`](THEORIE-UNIFIEE.md) + [`SPEC-EXP-FOCAL-01.md`](SPEC-EXP-FOCAL-01.md) — foundations.
5. [`JOURNAL.md`](JOURNAL.md) — the source's account, including nights with 1/3 scores.
6. [`QUESTIONS-OUVERTES.md`](QUESTIONS-OUVERTES.md) + [`tickets/`](tickets/) — the boundary.
7. [`ROADMAP.md`](ROADMAP.md) — past and future work (subject to approval in source).

## 🛰️ Phase 17: explorations — probe, UKTZ, RUQ (TEST-64→72)

After closing V12, the lab describes opening a second front: **placing agents inside the universe** and observing what happens — open explorations, preregistered observables, and reported verdicts.

### Endogenous probe (TEST-64→66): learning to sense

An infodynamic agent (Lempel–Ziv + volatility, internal thresholds, no neurons, no human labels) samples `syncQ/Φ/P_sig` bit by bit across calm vs. shock regimes. The source reports **three acknowledged false negatives**, but says bursts were measured under shock (11–13 flags). Its stated lesson: *novelty is relative to the memory horizon of the observer.*

<img src="images/plot_sonde_v3.png" width="100%" alt="Probe v3: bursts during shock, but calm drift is also noisy"/>

### UKTZ: three swarms, proximity interaction (TEST-67→69)

12 “neurons” were forced to move, with 300 separate steps and 300 grouped steps. The source reports:

- **S (semantic):** codes 0.44→0.97 — interpreted as proximity creating language.
- **T (topological, fixed graph):** `R` 0.72→0.69 — interpreted as structure determining the outcome.
- **RUQ-1** (phase + charge construction): `R` 0.30→0.98, `var(q)` divided by 9 — interpreted as grouping triggering a transition: *unity creates being*.

<img src="images/plot_neurons_uktz.png" width="100%" alt="UKTZ: semantic convergence, topological indifference, RUQ-1 transition"/>

### RUQ: does unity survive separation? (TEST-70→72)

- **TEST-70 (RUQ-1):** fused `R=0.985` → separated `R=0.31`, `t_half=11` steps → **H1 reversible**. The source metaphor says local unity fades like a dream, without a scar.

<img src="images/plot_RUQ70.png" width="100%" alt="RUQ-1: dissolution in 11 steps, H1 reversible"/>

- **TEST-71 (RUQ-2 + feedback):** `R` 0.98→0.26, `τ=15.1` → also **H1**. The local loop reportedly does not suffice; only a `θ-q` correlation (−0.57) remains: *a scar, not a thread*.

<img src="images/plot_RUQ71.png" width="100%" alt="RUQ-2: reversible despite feedback, correlational trace"/>

- **TEST-72 (RUQ-3 + fixed graph):** `R` 0.99→drop to 0.05→**recovery to 0.73** → **H2 hysteresis**. The source says the graph resynchronises the dispersed swarm: the first partial unity reported to survive separation.

<img src="images/plot_RUQ72.png" width="100%" alt="RUQ-3: drop then recovery through a fixed graph, H2 hysteresis"/>

### 🔚 Exploration summary (project interpretation)

> **The local system forgets (RUQ-1, 11 steps), the loop leaves a scar (RUQ-2, correlation −0.57), and the graph remembers (RUQ-3, H2).** The source proposes that unity surviving distance requires invariant topology — a first formal step toward its “Mind/Thread (U)” model. Further work is left to the project lead.

## 🕳️ Phase 18: V13 SINGULARITY (TEST-73→78) — score 2/5

The source describes a point-like focal “killer” (`MU=0.02D`, `σ=0.05D`) used to map gravity, relativity, and the resistance of U and Q. Its summary says: **the focal hole is not a Newtonian shadow, but a screened exponential well.** The measurements here are model outputs.

- **TEST-73:** divergent central well (`a=4.3`), profile `C·exp(−r/l)`, `R²=0.98`; `A/(r+eps)` rejected (`R²=0.88`) → H0 accepted + depression ring (“Mexican hat”).
- **TEST-74:** exponential wins **12/12** (`R²=0.998`); range `l` independent of mass (`p≈0`) → interpreted as finite-range gravity set by diffusion. ✅
- **TEST-75:** free clocks under shock remain **flat** (`τ_in=29.2` vs. `τ_out=31.4`); no time dilation detected. ❌
- **TEST-76:** U sanctuary in a local hole is **eroded** (10/30 vs. 4/30); the source says U absorbs the shock but loses half its fidelity. ❌
- **TEST-77:** Q capture: `k_c=6/24`; swallowing one quarter of the ring stops synchronisation. ✅

<img src="images/plot_V13.png" width="100%" alt="V13: exponential well, flat clocks, Q capture at k_c=6"/>

> **Added to the project canon (§10.octies), according to the source:** screened exponential law + Q capture. Newtonian behaviour, time dilation, and U immunity were rejected or partial, but still published.

## 🔭 Phase 19: QM–GR coexistence described (TEST-79→89)

The source says the instruction for this phase was **no verdict**: observe how virtual quantum mechanics (Q, phases, graph memory) coexists with relativity (wells, horizons, slowdown) without collapsing, and describe it.

- **TEST-79/80:** a well twists Q phase (twist 0→1); two wells with strong mismatch imprint twist −2; `R` declines gradually (0.85→0.32).
- **TEST-81:** exponential potential creates an S-shaped lens (±47°); central passage is straight, no capture.
- **TEST-82:** absorbing horizon (`th=0` pinned) → a **shadow appears** (contrast 0.66, saturated) where the “killer” created a well.
- **TEST-83:** RUQ-3 memory declines in curved space (0.73→0.25); grouped convergence remains intact.
- **TEST-84:** **monotonic redshift** — ring frequency rises from −0.53 to +0.01 with increasing distance from the well.
- **TEST-85:** three wells → twist is zero everywhere; the “twist = number of wells” lead stops at two (the source asks whether symmetry at three cancels torsion).
- **TEST-86/87** (Falstad twins, independent wave engine): absorbing disc → shadow 0.90/0.53/0.75; slow region → focus ×1.9.
- **TEST-88/89** (Wokwi twins, firmware prepared): twist predicts `R` 0.91→0.41; redshift predicts −0.77→−0.11. Phone guide: `outils_en_ligne/OUTILS-EN-LIGNE.md`.

<img src="images/plot_QM_GR.png" width="100%" alt="QM–GR: twists, lens, shadow, memory, redshift"/>
<img src="images/plot_T85.png" width="100%" alt="TEST-85: three wells, zero twist"/>

> The source describes these findings, without judging them. See §20 in `UNIFICATION`. It points to real-hardware IBM QPU bridges in `PASSERELLE-REEL.md` (`PONT-77`, `PONT-76`, `PONT-60`, `PONT-T2`), described as measured there.

## 🪭 Phase 20: LINK — search for the fold (TEST-90→93 + CLOSED-BERRY)

The stated goal is not forced unification, but to search for a **coherent connection point** between QM and relativity, however small, without rigid true/false verdicts.

- **TEST-90:** twist map (two wells, distance × force) → granular landscape (−2…+2), no clean fold lines.
- **TEST-91:** G0 up/down loop → **loop exists** (area 0.064, difference 0.17); the source interprets this as curvature writing a memory that the return path does not recover.
- **TEST-92:** rotating well ±1 turn → positive and negative turns produce the same result (+9 rad): symmetric drag, no geometric phase.
- **PONT-BERRY** (`ibm_fez`): ± loop on a qubit → U-shaped fringe vs. size (1.0→0.49→1.0, real ≈ simulation), but asymmetry ~0; the source says the loop is not closed (`U≠I`) and records this as a limitation.
- **TEST-93:** closed ± `(G0,c)` cycle → `Δ=−0.221 rad`; parameters close, but the state does not return (`R_diff 0.25`).
- **BERRY-FERMÉ** (`ibm_marrakesh`): closed ± loop (leakage ~1e−33, `γ=−φ/2`) → S-basis readout: **0.966 vs. 0.028 at `φ=π`** (real ≈ simulation). The source concludes: **orientation matters — the oriented fold is measured.** Verify the QPU job and artifact before citing this as hardware evidence.

<img src="images/plot_PLI.png" width="100%" alt="Search for the fold: granularity, loop, drag"/>
<img src="passerelle_quantique/plot_pontBerryFerme.png" width="100%" alt="Closed Berry loop: orientation matters (0.97 vs. 0.03)"/>

> The source says the oriented fold is isolated where the loop truly closes; hysteresis (open state) and Berry phase (closed state) are two faces of the fold.

## Phase 21: QM–GR synthesis (TEST-94)

The source presents a first model calculation requiring both scales: a superposition at two heights (internal spread `sw`, QM pillar) × local clocks in the well (redshift, GR pillar). It reports `τ=√2/(sw·|Δf|)` to about 8% over 18 cases; `τ=∞` when either pillar is removed (30 controls). These are model results, not a physical measurement of gravitational decoherence.

<img src="images/plot_DECO94.png" width="100%" alt="Gravitational decoherence: both QM and GR required"/>

## 📝 Citation, author, and license

```bibtex
@software{ratiss_focal_2026,
  author  = {Jonathan Evina and RATISS Labs},
  title   = {RATISS-FOCAL: informational focusing without neurons —
             69 pre-registered tests, 13 unification releases},
  year    = {2026},
  url     = {https://github.com/jonathansearch/ratiss-focal},
  license = {MIT}
}
```

<div align="center">

**RATISS Labs** — *The mind does not process everything; it processes coherence.* 🌌

By **Jonathan Evina** · September 2026 · **MIT License** (see [LICENSE](LICENSE)) — an open theory, intended for public reproducibility and external evaluation.

<img src="images/logo-ratiss-labs.png" width="120" alt="RATISS Labs"/>

</div>
