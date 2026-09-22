#!/usr/bin/env python3
"""PONT-BERRY : une boucle orientée imprime-t-elle une phase ? — simu + QPU.
Réplique hardware de la question TEST-92 (holonomie) dans l'espace des
paramètres du qubit, où la courbure est exacte (phase géométrique).
- Circuit : H - boucle - H - mesure. Boucle(alpha) =
  Rz(a)Rx(b)Rz(-a)Rx(-b), b=pi/2 ; orientation inverse = dagger
  (ordre inversé, angles niés) : Rz(-a)Rx(-b)Rz(a)Rx(b).
- alpha dans {0, pi/4, pi/2, 3pi/4, pi} x 2 orientations = 10 circuits.
- Observable : P0(boucle), P0(dagger), asymétrie A = P0-P0† vs alpha
  (signature orientée de la courbure ; TEST-92 virtuel : A=0).
Shots 4000 (précision). 1 job. Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile

HERE = os.path.dirname(os.path.abspath(__file__))
ALPHAS = [0.0, float(np.pi / 4), float(np.pi / 2),
          float(3 * np.pi / 4), float(np.pi)]
BETA, SHOTS = float(np.pi / 2), 4000


def circ(a, dagger):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    if not dagger:
        qc.rz(a, 0); qc.rx(BETA, 0); qc.rz(-a, 0); qc.rx(-BETA, 0)
    else:
        qc.rz(-a, 0); qc.rx(-BETA, 0); qc.rz(a, 0); qc.rx(BETA, 0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def p0(counts):
    return counts.get("0", 0) / sum(counts.values())


def run_simulateur():
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    lignes = []
    for a in ALPHAS:
        p = p0(sim.run(transpile(circ(a, False), sim), shots=SHOTS)
               .result().get_counts())
        q = p0(sim.run(transpile(circ(a, True), sim), shots=SHOTS)
               .result().get_counts())
        lignes.append({"alpha": round(a, 4), "P0": round(p, 4),
                       "P0dag": round(q, 4), "A": round(p - q, 4)})
        print(f"[berry] simu a={a:.3f} : P0={p:.4f} P0dag={q:.4f} A={p-q:+.4f}",
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
    print(f"[berry] backend réel : {backend.name}", flush=True)
    pubs = []
    for a in ALPHAS:
        pubs.append(transpile(circ(a, False), backend))
        pubs.append(transpile(circ(a, True), backend))
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[berry] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[berry] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    lignes = []
    for i, a in enumerate(ALPHAS):
        p = p0(res[2 * i].data.c.get_counts())
        q = p0(res[2 * i + 1].data.c.get_counts())
        lignes.append({"alpha": round(a, 4), "P0": round(p, 4),
                       "P0dag": round(q, 4), "A": round(p - q, 4)})
        print(f"[berry] réel a={a:.3f} : P0={p:.4f} P0dag={q:.4f} A={p-q:+.4f}",
              flush=True)
    return lignes, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        lignes, job_id, backend = run_reel(sys.argv[2])
        out = os.path.join(HERE, "resultats_pontBerry_reel.json")
        json.dump({"job": job_id, "backend": backend, "lignes": lignes},
                  open(out, "w"), indent=1)
    else:
        lignes = run_simulateur()
        out = os.path.join(HERE, "resultats_pontBerry_simulateur.json")
        json.dump({"lignes": lignes}, open(out, "w"), indent=1)
    print(f"[berry] archivé : {out}")
