#!/usr/bin/env python3
"""PONT-76 : le sanctuaire partagé s'érode-t-il graduellement sous bruit
local ? — sur VRAIS qubits (ou simulateur).

Pont avec TEST-76 (virtuel : U partagé ÉRODÉ 10/30 sous trou local) :
- 2 qubits en état de Bell Phi+ (corrélation partagée = analogue de U).
- Bruit local : sur le qubit 1 seul, flip X avec proba p
  (spaghettification d'un seul côté). p dans {0, .1, .2, .3, .4, .5}.
- Observable : P(mêmes) = (00+11)/shots, moyenne sur 10 tirages
  (graines fixées 7600+100*i_p+tirage). Idéal : 1-p (érosion linéaire).

Usage :
  python3 pont76_sanctuaire_reel.py              -> simulateur Aer
  python3 pont76_sanctuaire_reel.py --reel TOKEN -> 1 seul job QPU réel
Vérifier les files AVANT (file_qpu.py TOKEN). Compte en /tmp seul.
Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile

HERE = os.path.dirname(os.path.abspath(__file__))
PS = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
SHOTS, TIRAGES = 2000, 10


def circuit(p, ip, tirage):
    rng = np.random.default_rng(7600 + 100 * ip + tirage)
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    if rng.random() < p:  # spaghettification locale, qubit 1 seul
        qc.x(1)
    qc.measure([0, 1], [0, 1])
    return qc


def pmemes(counts):
    tot = sum(counts.values())
    return (counts.get("00", 0) + counts.get("11", 0)) / tot


def run_simulateur():
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    lignes = []
    for ip, p in enumerate(PS):
        vs = []
        for tirage in range(TIRAGES):
            counts = sim.run(transpile(circuit(p, ip, tirage), sim),
                             shots=SHOTS).result().get_counts()
            vs.append(pmemes(counts))
        lignes.append({"p": p, "moy": round(float(np.mean(vs)), 4),
                       "std": round(float(np.std(vs)), 4)})
        print(f"[pont76] simulateur p={p} : {np.mean(vs):.4f} ± {np.std(vs):.4f}",
              flush=True)
    return lignes


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
    print(f"[pont76] backend réel : {backend.name}", flush=True)
    pubs = [transpile(circuit(p, ip, t), backend)
            for ip, p in enumerate(PS) for t in range(TIRAGES)]
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[pont76] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[pont76] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    lignes = []
    i = 0
    for p in PS:
        vs = []
        for _ in range(TIRAGES):
            vs.append(pmemes(res[i].data.c.get_counts()))
            i += 1
        lignes.append({"p": p, "moy": round(float(np.mean(vs)), 4),
                       "std": round(float(np.std(vs)), 4)})
        print(f"[pont76] réel p={p} : {np.mean(vs):.4f} ± {np.std(vs):.4f}",
              flush=True)
    return lignes, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        lignes, job_id, backend = run_reel(sys.argv[2])
        out = os.path.join(HERE, "resultats_pont76_reel.json")
        json.dump({"job": job_id, "backend": backend, "N": 2,
                   "shots": SHOTS, "lignes": lignes}, open(out, "w"), indent=1)
    else:
        lignes = run_simulateur()
        out = os.path.join(HERE, "resultats_pont76_simulateur.json")
        json.dump({"N": 2, "shots": SHOTS, "lignes": lignes},
                  open(out, "w"), indent=1)
    print(f"[pont76] archivé : {out}")
