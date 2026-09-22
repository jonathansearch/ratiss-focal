#!/usr/bin/env python3
"""PONT-77 : la capture partielle tue-t-elle la cohérence globale — sur de
VRAIS qubits (ou simulateur gratuit en attendant le compte).

Pont entre TEST-77 (virtuel : k_c=6/24 tue la sync Q) et hardware réel :
- N=6 qubits préparés en état GHZ (intrication globale = analogue de R=1).
- Capture : k qubits « avalés » = flips aléatoires X/Z (p=0.5, graine
  fixée 7700+k, comme TEST-77) appliqués avant mesure.
- Observable : fidélité de Hellinger entre la distribution mesurée et la
  distribution idéale (50/50 sur 000000/111111). k dans {0,1,2,3,4}.

Usage :
  python3 pont77_capture_reelle.py                -> simulateur Aer (gratuit)
  python3 pont77_capture_reelle.py --reel TOKEN   -> vrai QPU IBM (Open Plan)
Compatibilité Quantum Inspire (Tuna, gratuit) : même code Qiskit, changer
le backend (voir commentaire en bas).
Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import hellinger_fidelity

HERE = os.path.dirname(os.path.abspath(__file__))
N, SHOTS, TIRAGES = 6, 2000, 10
IDEAL = {"0" * N: 0.5, "1" * N: 0.5}


def circuit(k, tirage):
    rng = np.random.default_rng(7700 + 100 * k + tirage)
    qc = QuantumCircuit(N, N)
    qc.h(0)
    for i in range(1, N):
        qc.cx(0, i)
    for i in range(k):  # les k premiers qubits sont « avalés »
        if rng.random() < 0.5:
            qc.x(i)
        if rng.random() < 0.5:
            qc.z(i)
    qc.measure(range(N), range(N))
    return qc


def fidelite(counts):
    return float(hellinger_fidelity(counts, IDEAL))


def run_simulateur():
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    lignes = []
    for k in (0, 1, 2, 3, 4):
        fs = []
        for tirage in range(TIRAGES):
            counts = sim.run(transpile(circuit(k, tirage), sim),
                             shots=SHOTS).result().get_counts()
            fs.append(fidelite(counts))
        lignes.append({"k": k, "fidelite_moy": round(float(np.mean(fs)), 4),
                       "tirages": TIRAGES})
        print(f"[pont77] simulateur k={k} : F_moy={np.mean(fs):.4f}", flush=True)
    return lignes


def run_reel(token):
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    service = QiskitRuntimeService(channel="ibm_quantum", token=token)
    backend = service.least_busy(min_num_qubits=N, operational=True,
                                 simulator=False)
    print(f"[pont77] backend réel : {backend.name}", flush=True)
    lignes = []
    for k in (0, 1, 2, 3, 4):
        job = Sampler(backend).run([transpile(circuit(k), backend)],
                                   shots=SHOTS)
        counts = job.result()[0].data.c.get_counts()
        f = float(hellinger_fidelity(counts, IDEAL))
        lignes.append({"k": k, "fidelite": round(f, 4)})
        print(f"[pont77] réel k={k} : F={f:.4f}", flush=True)
    return lignes


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        lignes = run_reel(sys.argv[2])
        out = os.path.join(HERE, "resultats_pont77_reel.json")
    else:
        lignes = run_simulateur()
        out = os.path.join(HERE, "resultats_pont77_simulateur.json")
    json.dump({"N": N, "shots": SHOTS, "lignes": lignes},
              open(out, "w"), indent=1)
    print(f"[pont77] archivé : {out}")
    # Quantum Inspire (gratuit, Qiskit-compatible) : remplacer run_reel par :
    #   from quantuminspire.qiskit import QI
    #   QI.set_authentication(); backend = QI.get_backend('Tuna-17')
