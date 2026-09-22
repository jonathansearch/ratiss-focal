#!/usr/bin/env python3
"""PONT-60 : relaxation (T1) + flip piloté par phase — sur VRAIS qubits.

Ponts : (a) T1 avec RUQ (TEST-70/71 : t_half=11, tau=15.1 — la mémoire
focale oublie ; et la mémoire réelle ?) ; (b) flip piloté avec TEST-60
(V12 : impulsion de phase -> LOW/HIGH).
- T1 : X - délai(t) - mesure, t = 0..300 us (12 pts). Observable : P(1).
- FLIP : H - Rz(phi) - H - mesure, phi = 0..2pi (16 pts). Obs : P(0).
1 qubit, 28 circuits en 1 job. Shots 2000.
Usage : script seul -> Aer ; --reel TOKEN -> QPU (files via file_qpu.py).
Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile

HERE = os.path.dirname(os.path.abspath(__file__))
T1_US = [0, 10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500]
PHIS = [round(float(x), 4) for x in np.linspace(0, 2 * np.pi, 16)]
SHOTS = 2000


def circ_t1(t_us):
    qc = QuantumCircuit(1, 1)
    qc.x(0)
    if t_us > 0:
        qc.delay(t_us, 0, unit="us")
    qc.measure(0, 0)
    return qc


def circ_flip(phi):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.rz(phi, 0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def p1(counts):
    return counts.get("1", 0) / sum(counts.values())


def p0(counts):
    return counts.get("0", 0) / sum(counts.values())


def run_simulateur():
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    t1 = [p1(sim.run(transpile(circ_t1(t), sim), shots=SHOTS)
              .result().get_counts()) for t in T1_US]
    fl = [p0(sim.run(transpile(circ_flip(p), sim), shots=SHOTS)
              .result().get_counts()) for p in PHIS]
    return t1, fl


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
    print(f"[pont60] backend réel : {backend.name}", flush=True)
    pubs = [transpile(circ_t1(t), backend) for t in T1_US] + \
           [transpile(circ_flip(p), backend) for p in PHIS]
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[pont60] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[pont60] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    t1 = [p1(res[i].data.c.get_counts()) for i in range(len(T1_US))]
    fl = [p0(res[len(T1_US) + i].data.c.get_counts()) for i in range(len(PHIS))]
    return t1, fl, job.job_id(), backend.name


def ajuste_t1(t1):
    y = np.array(t1)
    x = np.array(T1_US)
    m = y > 0.02
    if m.sum() < 3:
        return None, None
    a, b = np.polyfit(x[m], np.log(y[m]), 1)
    if a >= 0:
        return None, None
    pred = np.exp(b) * np.exp(a * x[m])
    r2 = 1 - ((y[m] - pred) ** 2).sum() / ((y[m] - y[m].mean()) ** 2).sum()
    return round(float(-1 / a), 1), round(float(r2), 4)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        t1, fl, job_id, backend = run_reel(sys.argv[2])
        T1, R2 = ajuste_t1(t1)
        out = os.path.join(HERE, "resultats_pont60_reel.json")
        json.dump({"job": job_id, "backend": backend, "T1_us": T1,
                   "R2_T1": R2, "t1_us": T1_US,
                   "P1": [round(float(v), 4) for v in t1], "phis": PHIS,
                   "P0": [round(float(v), 4) for v in fl]},
                  open(out, "w"), indent=1)
        print(f"[pont60] réel T1={T1} us (R2={R2})", flush=True)
    else:
        t1, fl = run_simulateur()
        out = os.path.join(HERE, "resultats_pont60_simulateur.json")
        json.dump({"t1_us": T1_US, "P1": [round(float(v), 4) for v in t1],
                   "phis": PHIS, "P0": [round(float(v), 4) for v in fl]},
                  open(out, "w"), indent=1)
        print("[pont60] simulateur archivé", flush=True)
    print(f"[pont60] archivé : {out}")
