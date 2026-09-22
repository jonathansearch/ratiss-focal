#!/usr/bin/env python3
"""PONT-72 : écho de Hahn (la structure fait récupérer) — simu puis QPU.
Pont avec TEST-72 (H2 : R chute puis RÉCUPÈRE via graphe fixe).
- Série Ramsey (sans structure) : H - t - H. Référence (T2* ~ 70 us).
- Série Écho (avec refocalisation = analogue du graphe) :
  H - t/2 - X - t/2 - H. Observable : P0(t) -> T2_echo.
- Prédiction lue : T2_echo > T2* (l'impulsion centralisée récupère).
14 délais x 2 séries = 28 circuits, 1 job. Shots 2000.
Simu : expo + binomial (T2*_hyp=70 mesuré, T2echo_hyp=200).
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
HYP_PLAIN, HYP_ECHO = 70.0, 200.0


def circ_plain(t_us):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    if t_us > 0:
        qc.delay(t_us, 0, unit="us")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def circ_echo(t_us):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    if t_us > 0:
        qc.delay(t_us / 2, 0, unit="us")
        qc.x(0)
        qc.delay(t_us / 2, 0, unit="us")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def p0(counts):
    return counts.get("0", 0) / sum(counts.values())


def ajuste(delais, p0s):
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
    rng = np.random.default_rng(7200)
    out = {}
    for nom, hyp in (("plain", HYP_PLAIN), ("echo", HYP_ECHO)):
        ps = [float(rng.binomial(SHOTS, 0.5 + 0.5 * np.exp(-t / hyp)) / SHOTS)
              for t in DELAIS]
        T2, R2 = ajuste(DELAIS, ps)
        out[nom] = (ps, T2, R2)
        print(f"[pont72] simu {nom} : T2={T2} (R2={R2})", flush=True)
    return out


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
    print(f"[pont72] backend réel : {backend.name}", flush=True)
    pubs = [transpile(circ_plain(t), backend) for t in DELAIS] + \
           [transpile(circ_echo(t), backend) for t in DELAIS]
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[pont72] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[pont72] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    out = {}
    for k, nom in enumerate(("plain", "echo")):
        ps = [p0(res[k * len(DELAIS) + i].data.c.get_counts())
              for i in range(len(DELAIS))]
        T2, R2 = ajuste(DELAIS, ps)
        out[nom] = (ps, T2, R2)
        print(f"[pont72] réel {nom} : T2={T2} (R2={R2})", flush=True)
    return out, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        out, job_id, backend = run_reel(sys.argv[2])
        res = {"job": job_id, "backend": backend, "delais_us": DELAIS}
        for nom in ("plain", "echo"):
            ps, T2, R2 = out[nom]
            res[nom] = {"T2_us": T2, "R2": R2,
                        "P0": [round(float(v), 4) for v in ps]}
        json.dump(res, open(os.path.join(HERE, "resultats_pont72_reel.json"),
                            "w"), indent=1)
        print(f"[pont72] archivé réel : {job_id}", flush=True)
    else:
        out = run_simulateur()
        res = {"delais_us": DELAIS}
        for nom in ("plain", "echo"):
            ps, T2, R2 = out[nom]
            res[nom] = {"T2_us": T2, "R2": R2,
                        "P0": [round(float(v), 4) for v in ps]}
        json.dump(res, open(os.path.join(HERE, "resultats_pont72_simulateur.json"),
                            "w"), indent=1)
        print("[pont72] archivé simu", flush=True)
