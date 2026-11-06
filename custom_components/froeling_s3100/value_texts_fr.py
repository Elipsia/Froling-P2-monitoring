"""Traduction française des valeurs textuelles envoyées par la Lambdatronic S3100.

La chaudière transmet ses états et modes de fonctionnement en allemand
(trames MB : « Winterbetrieb », « Heizen », « Störung », ...). Ce module
fournit la correspondance vers le français pour les textes connus. Les
valeurs inconnues sont retournées telles quelles afin de ne jamais
masquer une information.

La traduction se fait uniquement à l'affichage : les valeurs brutes
restent en allemand à l'intérieur de l'intégration (les capteurs dérivés
comme « Feu actif » ou « Défaut » s'appuient sur les textes allemands).
"""

from __future__ import annotations

import re

_NORMALIZE_PATTERN = re.compile(r"[^a-zäöüß0-9]")

_VALUE_TEXTS_FR: dict[str, str] = {
    "betriebsbereit": "Prêt",
    "anheizen": "Montée en température",
    "heizen": "En chauffe",
    "feuerhaltung": "Maintien du feu",
    "zünden": "Allumage",
    "vorwärmphase": "Préchauffage",
    "störung": "Défaut",
    "feuer aus": "Feu éteint",
    "feuer-aus": "Feu éteint",
    "kein feuer": "Pas de feu",
    "aus": "Arrêt",
    "ein": "En marche",
    "hand": "Manuel",
    "automatik": "Automatique",
    "winterbetrieb": "Mode hiver",
    "sommerbetrieb": "Mode été",
    "übergangsbetr": "Mode intermédiaire",
    "übergangsbetrieb": "Mode intermédiaire",
    "scheitholzbetr": "Mode bois",
    "scheitholzbetrieb": "Mode bois",
    "stückholzbetrieb": "Mode bois",
    "reinigen": "Nettoyage",
    "extraheizen": "Chauffe renforcée",
    "notbetrieb": "Mode dégradé",
    "kessel aus": "Chaudière arrêtée",
    "kessel an": "Chaudière en marche",
    "puffer laden": "Charge du ballon",
    "boiler laden": "Charge de l'ECS",
    "warten": "En attente",
    "kein betrieb": "À l'arrêt",
    "abschalten": "Extinction",
    "abkühlen": "Refroidissement",
    "ruhezustand": "Repos",
    "vorrang kessel": "Priorité chaudière",
    "vorrang boiler": "Priorité ECS",
    "min. kesseltemp.": "Température chaudière minimale",
}


def _normalize(text: str) -> str:
    return _NORMALIZE_PATTERN.sub("", text.lower())


_LOOKUP = {_normalize(k): v for k, v in _VALUE_TEXTS_FR.items()}


def translate_value_text(value: str | None) -> str | None:
    """Renvoie la traduction française d'une valeur, ou la valeur d'origine."""
    if not value:
        return value
    normalized = _normalize(value)
    if normalized in _LOOKUP:
        return _LOOKUP[normalized]
    for key, translation in _LOOKUP.items():
        if len(key) >= 6 and key in normalized:
            return translation
    return value
