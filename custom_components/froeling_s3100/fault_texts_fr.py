"""Traduction française des messages d'erreur envoyés par la Lambdatronic S3100.

La chaudière transmet ses textes d'erreur (bloc MT) en allemand, encodés en
CP850. Ce module fournit une table de correspondance vers le français pour
les messages connus des installations réelles. Les textes inconnus sont
retournés tels quels (avec un marqueur visuel), afin de ne jamais masquer
une information.
"""

from __future__ import annotations

import re

_PREFIX = "Texte inconnu ({original})"

_NORMALIZE_PATTERN = re.compile(r"[^a-zäöüß0-9]")

_FAULT_TEXTS_FR: dict[str, str] = {
    "kesseltemperatur zu gering": "Température chaudière trop basse",
    "kesseltemp. fehlerhaft": "Sonde de température chaudière défectueuse",
    "kesseltemp fehlerhaft": "Sonde de température chaudière défectueuse",
    "sicherheitstemp. (stb) ausgelöst": "Limiteur de température de sécurité déclenché (STB)",
    "kesseltemperatur zu hoch": "Température chaudière trop élevée",
    "kesselfühler defekt": "Sonde de chaudière défectueuse",
    "kesselfühler defekt": "Sonde de chaudière défectueuse",
    "abgastemperatur zu hoch": "Température des fumées trop élevée",
    "kesseltemp. zu lange tief": "Température chaudière trop basse depuis trop longtemps",
    "kesseltemp. zu lange hoch": "Température chaudière trop élevée depuis trop longtemps",
    "vorlauftemp. zu lange tief": "Température de départ trop basse depuis trop longtemps",
    "vorlauftemp. zu lange hoch": "Température de départ trop élevée depuis trop longtemps",
    "rücklauftemp. zu lange tief": "Température de retour trop basse depuis trop longtemps",
    "rücklauftemp. zu lange hoch": "Température de retour trop élevée depuis trop longtemps",
    "abgastemp. zu lange hoch": "Température des fumées trop élevée depuis trop longtemps",
    "abgasfühler defekt": "Sonde de fumées défectueuse",
    "abgasfühler defekt": "Sonde de fumées défectueuse",
    "zündung fehlgeschlagen": "Échec de l'allumage",
    "zündfehler": "Erreur d'allumage",
    "kein feuer": "Pas de feu",
    "feuer aus": "Feu éteint",
    "saugzuggebläse defekt": "Ventilateur de tirage défectueux",
    "saugzuggebläse aus": "Ventilateur de tirage à l'arrêt",
    "zuluftgebläse defekt": "Ventilateur d'air défectueux",
    "primärluftgebläse defekt": "Ventilateur d'air primaire défectueux",
    "förderschnecke blockiert": "Vis d'alimentation bloquée",
    "förderschnecke defekt": "Vis d'alimentation défectueuse",
    "einschub blockiert": "Vis d'alimentation bloquée",
    "einschubmotor defekt": "Moteur de la vis d'alimentation défectueux",
    "austragung blockiert": "Extraction des pellets bloquée",
    "austragungsschnecke blockiert": "Vis d'extraction bloquée",
    "pellets nachschub gestört": "Alimentation en pellets perturbée",
    "kein pelletsnachschub": "Pas d'alimentation en pellets",
    "lager leer": "Silo de pellets vide",
    "pelletslager leer": "Silo de pellets vide",
    "behälter leer": "Réservoir de pellets vide",
    "asche entleeren": "Vider le bac à cendres",
    "aschebehälter voll": "Bac à cendres plein",
    "rost blockiert": "Grille bloquée",
    "rostmotor defekt": "Moteur de grille défectueux",
    "reinigung": "Nettoyage en cours",
    "kein wasser": "Pas d'eau",
    "wassermangel": "Manque d'eau",
    "druck zu gering": "Pression trop basse",
    "sicherheitstemperaturbegrenzer ausgelöst": "Limiteur de température de sécurité déclenché",
    "stb ausgelöst": "Limiteur de température de sécurité déclenché (STB)",
    "untertemperatur": "Température trop basse",
    "pufferfühler defekt": "Sonde de ballon défectueuse",
    "pufferfühler defekt": "Sonde de ballon défectueuse",
    "boilerfühler defekt": "Sonde de ballon ECS défectueuse",
    "boilerfühler defekt": "Sonde de ballon ECS défectueuse",
    "vorlauffühler defekt": "Sonde de départ défectueuse",
    "vorlauffühler defekt": "Sonde de départ défectueuse",
    "raumfühler defekt": "Sonde de pièce défectueuse",
    "außenfühler defekt": "Sonde extérieure défectueuse",
    "außenfühler defekt": "Sonde extérieure défectueuse",
    "rücklauffühler defekt": "Sonde de retour défectueuse",
    "rücklauffühler defekt": "Sonde de retour défectueuse",
    "mischer defekt": "Mélangeur défectueux",
    "mischer läuft": "Mélangeur en course",
    "pumpe defekt": "Pompe défectueuse",
    "speicherladepumpe defekt": "Pompe de charge du ballon défectueuse",
    "kommunikationsfehler": "Erreur de communication",
    "bus fehler": "Erreur de bus",
    "speicher voll": "Ballon chargé",
    "kein brennerbetrieb": "Pas de fonctionnement du brûleur",
    "warten": "En attente",
    "störung": "Défaut",
    "service": "Maintenance requise",
}


def _normalize(text: str) -> str:
    return _NORMALIZE_PATTERN.sub("", text.lower())


_LOOKUP = {_normalize(k): v for k, v in _FAULT_TEXTS_FR.items()}


def translate_fault_text(text: str | None) -> str | None:
    """Renvoie la traduction française d'un texte d'erreur, ou le texte d'origine."""
    if not text:
        return text
    normalized = _normalize(text)
    if normalized in _LOOKUP:
        return _LOOKUP[normalized]
    for key, value in _LOOKUP.items():
        if key in normalized or normalized in key:
            return value
    return _PREFIX.format(original=text)
