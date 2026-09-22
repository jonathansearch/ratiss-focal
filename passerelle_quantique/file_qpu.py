#!/usr/bin/env python3
"""FILE-QPU : (1) affiche la file de chaque QPU réel (pour choisir le moins
saturé), (2) récupère un job déjà envoyé par son ID et calcule les
fidélités PONT-77 si terminé.
Usage : python3 file_qpu.py TOKEN [JOB_ID] [ATTENTE_MIN]
Compte enregistré en /tmp uniquement (jamais persisté).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pont77_capture_reelle import fidelite, TIRAGES  # noqa: E402

from qiskit_ibm_runtime import QiskitRuntimeService

token = sys.argv[1]
job_id = sys.argv[2] if len(sys.argv) > 2 else None
attente = int(sys.argv[3]) if len(sys.argv) > 3 else 10

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform", token=token, instance="auto",
    filename="/tmp/qiskit-ibm.json", overwrite=True)
service = QiskitRuntimeService(channel="ibm_quantum_platform",
                               filename="/tmp/qiskit-ibm.json")

print("=== QPU réels : file d'attente ===", flush=True)
files = []
for b in sorted(service.backends(simulator=False, operational=True),
                key=lambda x: x.name):
    try:
        pending = b.status().pending_jobs
    except Exception:
        pending = "?"
    files.append((b.name, b.num_qubits, pending))
    print(f"  {b.name} : {b.num_qubits} qubits, en file={pending}", flush=True)
libres = [f for f in files if isinstance(f[2], int)]
if libres:
    top = min(libres, key=lambda f: f[2])
    print(f"=== moins saturé : {top[0]} ({top[2]} en file) ===", flush=True)

if not job_id:
    sys.exit(0)

job = service.job(job_id)
debut = time.time()
while str(job.status()) != "DONE":
    st = str(job.status())
    print(f"[file] job {job_id} : {st}", flush=True)
    if st in ("ERROR", "CANCELLED"):
        print(f"[file] job {st} — à renvoyer vers {top[0] if libres else '?'}",
              flush=True)
        sys.exit(1)
    if (time.time() - debut) / 60 > attente:
        print(f"[file] toujours {st} après {attente} min — relance-moi pour "
              f"récupérer (même JOB_ID).", flush=True)
        sys.exit(2)
    time.sleep(60)

res = job.result()
lignes = []
i = 0
for k in (0, 1, 2, 3, 4):
    fs = []
    for _ in range(TIRAGES):
        fs.append(fidelite(res[i].data.c.get_counts()))
        i += 1
    lignes.append({"k": k, "fidelite_moy": round(float(sum(fs) / len(fs)), 4),
                   "tirages": TIRAGES})
    print(f"[file] réel k={k} : F_moy={sum(fs) / len(fs):.4f}", flush=True)
out = os.path.join(HERE, "resultats_pont77_reel.json")
json.dump({"job": job_id, "backend": job.backend().name,
           "N": 6, "shots": 2000, "lignes": lignes}, open(out, "w"), indent=1)
print(f"[file] archivé : {out}")
