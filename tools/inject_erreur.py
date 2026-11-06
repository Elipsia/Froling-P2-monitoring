"""Injecte une erreur (trame M3) dans un simulateur S3100 en cours d'exécution.

Usage :
    python tools/inject_erreur.py --host 127.0.0.1 --port 4196 --erreur 1

Se connecte au simulateur en parallèle de la session Home Assistant : le
simulateur diffuse l'erreur à tous les clients connectés, ce qui déclenche
l'événement d'erreur et l'automatisation de notification.

Codes d'erreur connus dans la capture de référence :
    0 = Sicherheitstemp. (STB) ausgelöst  (limiteur de sécurité déclenché)
    1 = Kesseltemp. fehlerhaft            (sonde chaudière défectueuse)
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime

from froeling_s3100.protocol import encode_frame


def _to_bcd(value: int) -> int:
    return ((value // 10) << 4) | (value % 10)


async def inject(host: str, port: int, error_id: int) -> None:
    reader, writer = await asyncio.open_connection(host, port)
    moment = datetime.now()
    payload = bytes(
        [
            error_id,
            0x00,
            0x00,
            _to_bcd(moment.second),
            _to_bcd(moment.minute),
            _to_bcd(moment.hour),
            _to_bcd(moment.day),
            _to_bcd(moment.month),
            moment.isoweekday(),
            _to_bcd(moment.year % 100),
        ]
    )
    writer.write(encode_frame(b"RX", payload))
    await writer.drain()
    await asyncio.sleep(1.0)
    writer.close()
    await writer.wait_closed()


def main() -> None:
    parser = argparse.ArgumentParser(description="Injecte une erreur M3 dans le simulateur S3100")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4196)
    parser.add_argument("--erreur", dest="error_id", type=int, default=1, help="ID du texte d'erreur (0 ou 1 dans la capture)")
    args = parser.parse_args()
    asyncio.run(inject(args.host, args.port, args.error_id))
    print(f"Erreur {args.error_id} injectée sur {args.host}:{args.port}")


if __name__ == "__main__":
    main()
