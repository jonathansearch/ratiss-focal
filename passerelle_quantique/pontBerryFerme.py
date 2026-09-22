#!/usr/bin/env python3
"""PONT-BERRY-FERMÉ v2 : cycle VRAIMENT fermé ± sur qubit (réplique TEST-93).
v1 : Ry(t)Rz(phi)Ry(-t) ne se refermait pas (S plat à 0.5, assumé).
v2 : boucle méridien-équateur-méridien : N -> A [Ry(t)], A -> B [Rz(phi)],
B -> N [rotation t autour de l'axe équatorial alpha=phi+pi/2] : retour
EXACT à |0> (fuite vérifiée numériquement, ~0). Phase gamma = -/+phi/2.
Interférométrie : contrôle en superposition, 3 unitaires contrôlées,
H (+ S optionnel), mesure. phi dans {0, pi/2, pi, 3pi/2, 2pi}.
2 orientations x 2 lectures = 20 circuits, 1 job.
Idéal : sans S : P0 = cos²(phi/4) (pair) ; avec S : P0±=(1±sin(phi/2))/2.
Shots 4000. Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate

HERE = os.path.dirname(os.path.abspath(__file__))
PHIS = [0.0, float(np.pi / 2), float(np.pi),
        float(3 * np.pi / 2), float(2 * np.pi)]
TH, SHOTS = float(np.pi / 2), 4000


def mats(phi):
    t = TH
    U_out = np.array([[np.cos(t / 2), -np.sin(t / 2)],
                      [np.sin(t / 2), np.cos(t / 2)]])
    U_lat = np.array([[np.exp(-1j * phi / 2), 0],
                      [0, np.exp(1j * phi / 2)]])
    nx, ny = -np.sin(phi), np.cos(phi)
    sx = np.array([[0, 1], [1, 0]])
    sy = np.array([[0, -1j], [1j, 0]])
    U_ret = (np.cos(t / 2) * np.eye(2)
             + 1j * np.sin(t / 2) * (nx * sx + ny * sy))
    return [U_out, U_lat, U_ret]


def fermeture(phi):
    U_out, U_lat, U_ret = mats(phi)
    v = (U_ret @ U_lat @ U_out)[:, 0]
    return float(abs(v[1]) ** 2), float(np.angle(v[0]))


def circ(phi, dagger, avec_s):
    pieces = mats(phi)
    if dagger:
        pieces = [p.conj().T for p in reversed(pieces)]
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    for U in pieces:
        qc.append(UnitaryGate(U).control(1), [0, 1])
    if avec_s:
        qc.s(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def p0(counts):
    return counts.get("0", 0) / sum(counts.values())


def run_simulateur():
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    lignes = []
    for phi in PHIS:
        leak, gamma = fermeture(phi)
        row = {"phi": round(phi, 4), "fuite": round(leak, 6),
               "gamma": round(gamma, 4)}
        for dag in (False, True):
            for s in (False, True):
                c = sim.run(transpile(circ(phi, dag, s), sim),
                            shots=SHOTS).result().get_counts()
                row[f"{'dag' if dag else 'loop'}_{'S' if s else 'H'}"] = \
                    round(p0(c), 4)
        lignes.append(row)
        print(f"[bf] simu phi={phi:.3f} fuite={leak:.2e} gamma={gamma:+.3f} "
              f"H={row['loop_H']}/{row['dag_H']} "
              f"S={row['loop_S']}/{row['dag_S']}", flush=True)
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
    print(f"[bf] backend réel : {backend.name}", flush=True)
    pubs = []
    for phi in PHIS:
        for dag in (False, True):
            for s in (False, True):
                pubs.append(transpile(circ(phi, dag, s), backend))
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[bf] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[bf] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    lignes = []
    for i, phi in enumerate(PHIS):
        row = {"phi": round(phi, 4)}
        for j, (dag, s) in enumerate([(False, False), (False, True),
                                      (True, False), (True, True)]):
            c = res[4 * i + j].data.c.get_counts()
            row[f"{'dag' if dag else 'loop'}_{'S' if s else 'H'}"] = \
                round(p0(c), 4)
        lignes.append(row)
        print(f"[bf] réel phi={phi:.3f} : H={row['loop_H']}/{row['dag_H']} "
              f"S={row['loop_S']}/{row['dag_S']}", flush=True)
    return lignes, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        lignes, job_id, backend = run_reel(sys.argv[2])
        out = os.path.join(HERE, "resultats_pontBerryFerme_reel.json")
        json.dump({"job": job_id, "backend": backend, "lignes": lignes},
                  open(out, "w"), indent=1)
    else:
        lignes = run_simulateur()
        out = os.path.join(HERE, "resultats_pontBerryFerme_simulateur.json")
        json.dump({"lignes": lignes}, open(out, "w"), indent=1)
    print(f"[bf] archivé : {out}")
