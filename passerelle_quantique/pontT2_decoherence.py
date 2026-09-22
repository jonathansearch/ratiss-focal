#!/usr/bin/env python3
"""PONT-T2 : décohérence Ramsey (T2*) — simulation bruitée puis validation.
Pont avec RUQ (mémoire qui oublie) et PONT-60 (T1=285.4 us mesuré).
- Circuit : H - délai(t) - H - mesure ; t = 0..250 us (14 pts).
- Simulation : modèle P0=0.5+0.5*exp(-t/T2hyp) + bruit binomial
  (T2hyp=180 us, graines fixées — calibre la chaîne d'ajustement ;
  le bruit thermique Aer ne mord pas sur les délais, constaté plat).
- Validation : même circuits sur QPU réel, ajustement exp -> T2*.
1 qubit, 14 circuits en 1 job. Shots 2000.
Usage : script seul -> simu bruitée ; --reel TOKEN -> QPU.
Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile

HERE = os.path.dirname(os.path.abspath(__file__))
DELAIS = [0, 5, 10, 20, 30, 50, 75, 100, 125, 150, 175, 200, 225, 250]
SHOTS = 2000
T1_CAL, T2_HYP = 285.4, 180.0


def circ(t_us):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    if t_us > 0:
        qc.delay(t_us, 0, unit="us")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def p0(counts):
    return counts.get("0", 0) / sum(counts.values())


def ajuste(delais, p0s):
    # P0(t) = 0.5 + 0.5*exp(-t/T2*) -> fit sur y = 2*P0-1
    y = np.array([2 * v - 1 for v in p0s])
    x = np.array(delais, float)
    m = y > 0.02
    if m.sum() < 3:
        return None, None
    a, b = np.polyfit(x[m], np.log(y[m]), 1)
    if a >= 0:
        return None, None
    pred = np.exp(b) * np.exp(a * x[m])
    r2 = 1 - ((y[m] - pred) ** 2).sum() / ((y[m] - y[m].mean()) ** 2).sum()
    return round(float(-1 / a), 1), round(float(r2), 4)


def run_simulateur():
    # Simu honnête : le bruit thermique Aer ne s'attache pas aux délais
    # (P0 restait plat à 1.0). On calibre la chaîne d'ajustement avec le
    # modèle exponentiel + bruit de tirage binomial (graines fixées).
    rng = np.random.default_rng(7200)
    ps = []
    for t in DELAIS:
        p = 0.5 + 0.5 * np.exp(-t / T2_HYP)
        ps.append(float(rng.binomial(SHOTS, p) / SHOTS))
    return ps


def run_reel(token):
    import time
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    QiskitRuntimeService.save_account(
        channel="ibm_quantum_platform", token=token, instance="auto",
        filename="/tmp/qiskit-ibm.json", overwrite=True)
    service = QiskitRuntimeService(channel="ibm_quantum_platform",
                                   filename="/tmp/qiskit-ibm.json")
    files = []
    for b in service.backends(simulator=False, operational=True):
        try:
            files.append((b.status().pending_jobs, b))
        except Exception:
            pass
    backend = sorted(files, key=lambda f: f[0])[0][1]
    print(f"[pontT2] backend réel : {backend.name}", flush=True)
    pubs = [transpile(circ(t), backend) for t in DELAIS]
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[pontT2] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[pontT2] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    ps = [p0(res[i].data.c.get_counts()) for i in range(len(DELAIS))]
    return ps, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        ps, job_id, backend = run_reel(sys.argv[2])
        T2, R2 = ajuste(DELAIS, ps)
        out = os.path.join(HERE, "resultats_pontT2_reel.json")
        json.dump({"job": job_id, "backend": backend, "T2star_us": T2,
                   "R2": R2, "delais_us": DELAIS,
                   "P0": [round(float(v), 4) for v in ps]},
                  open(out, "w"), indent=1)
        print(f"[pontT2] réel T2*={T2} us (R2={R2})", flush=True)
    else:
        ps = run_simulateur()
        T2, R2 = ajuste(DELAIS, ps)
        out = os.path.join(HERE, "resultats_pontT2_simulateur.json")
        json.dump({"T1_cal_us": T1_CAL, "T2_hyp_us": T2_HYP,
                   "T2star_simu_us": T2, "R2": R2, "delais_us": DELAIS,
                   "P0": [round(float(v), 4) for v in ps]},
                  open(out, "w"), indent=1)
        print(f"[pontT2] simu bruitée T2*={T2} us (R2={R2})", flush=True)
    print(f"[pontT2] archivé : {out}")
