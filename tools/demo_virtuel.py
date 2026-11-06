"""Démo : test 100 % virtuel, sans chaudière ni matériel."""
import asyncio
import importlib.util
from pathlib import Path

from froeling_s3100.client import EventType, S3100Client
from froeling_s3100.simulator import Recording, SimulatedController

spec = importlib.util.spec_from_file_location(
    "ftf", "custom_components/froeling_s3100/fault_texts_fr.py")
ftf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ftf)

async def main():
    capture = Path("tests/fixtures/s3100_capture.jsonl")
    sim = SimulatedController(Recording.from_jsonl(capture))
    await sim.start("127.0.0.1", 0)
    print(f"[SIMULATEUR] Lambdatronic S3100 virtuelle en écoute sur 127.0.0.1:{sim.port}")

    client = S3100Client("127.0.0.1", sim.port)
    faults = []
    client.subscribe(lambda e: faults.append(e.data) if e.type == EventType.FAULT else None)
    await client.start()
    await client.wait_ready(30)
    for _ in range(200):
        if client.values:
            break
        await asyncio.sleep(0.05)

    print("[CONNEXION] Login accepté, catalogue chargé depuis la capture réelle\n")
    print("=== MESURES REÇUES (rejouées depuis une vraie chaudière) ===")
    for key, value in sorted(client.values.items()):
        print(f"  {key:<28} = {value}")

    print("\n=== INJECTION D'UNE ERREUR (trame M3, comme un vrai défaut) ===")
    def bcd(v): return ((v // 10) << 4) | (v % 10)
    # error_id=1 (Kesseltemp. fehlerhaft), flags, état, puis date/heure en BCD
    sim.inject_fault(bytes([1, 0, 0, bcd(30), bcd(14), bcd(21), bcd(6), bcd(11), 0, bcd(25)]))
    await asyncio.sleep(1.0)
    for f in faults:
        print(f"  Erreur reçue  : {f.text!r}")
        print(f"  Traduite      : {ftf.translate_fault_text(f.text)!r}")

    await client.stop()
    await sim.stop()
    print("\n[OK] Test virtuel complet, aucune chaudière n'a été touchée.")

asyncio.run(main())
