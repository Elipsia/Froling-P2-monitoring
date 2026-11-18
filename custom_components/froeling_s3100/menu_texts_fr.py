"""Traduction française des textes de menu (paramètres) de la Lambdatronic S3100.

La chaudière annonce ses menus et paramètres en allemand (trames MD/ME : « Heizzeiten »,
« Heizkreis 1 », ...). Ce module fournit la correspondance vers le français pour les
textes connus, y compris les variantes avec coupure de ligne envoyées par le
régulateur (« Beginn der 1.Puf ferladung »). Les textes inconnus sont retournés
tels quels afin de ne jamais masquer une information.
"""

from __future__ import annotations

import re

_NORMALIZE_PATTERN = re.compile(r"[^a-zäöüß0-9]")

_MENU_TEXTS_FR: dict[str, str] = {
    "Abgastemp. Feuer-AUS": "Température fumées à l'extinction du feu",
    "Ausschalten über Soll.Temp.+": "Arrêt au-dessus de la consigne +",
    "Ausschalten über max. Sollt.+": "Arrêt au-dessus de la consigne max. +",
    "Außentemperatur Heizgrenze": "Température extérieure limite de chauffe",
    "Außent.Heizgr. Absenkbetr": "Temp. ext. limite de chauffe (mode réduit)",
    "Beginn der 1. Aufladung": "Début 1ʳᵉ charge",
    "Beginn der 1.Puf ferladung": "Début 1ʳᵉ charge ballon",
    "Beginn der 2. Aufladung": "Début 2ᵉ charge",
    "Beginn der 2.Puf ferladung": "Début 2ᵉ charge ballon",
    "Betriebsart:": "Mode de fonctionnement :",
    "Boiler": "Ballon ECS",
    "Boilerpumpe Min.Drehz.": "Vitesse min. pompe ECS",
    "Die Kesseltemp. soll sein": "Consigne température chaudière",
    "Die Pumpen laufen ab": "Départ des pompes à",
    "EINSTELLEN": "RÉGLAGES",
    "Ende der 1. Aufladung": "Fin 1ʳᵉ charge",
    "Ende der 1.Puf ferladung": "Fin 1ʳᵉ charge ballon",
    "Ende der 2. Aufladung": "Fin 2ᵉ charge",
    "Ende der 2.Puf ferladung": "Fin 2ᵉ charge ballon",
    "GewünschteBoiler temperatur": "Température ECS souhaitée",
    "Heizkurve": "Courbe de chauffe",
    "Heizzeiten": "Programmes horaires",
    "Kesseltemp": "Température chaudière",
    "Legionellen Auf- heiztag": "Jour de chauffe anti-légionelles",
    "Legionellen Aufheizung65°": "Chauffe anti-légionelles 65 °C",
    "Maximale Abgastemperatur": "Température fumées maximale",
    "Maximale Anheizzeit": "Durée max. de montée en température",
    "Mindestrücklauftemperatur": "Température de retour minimale",
    "Minimale Abgastemperatur": "Température fumées minimale",
    "MoDiMiDoFrSaSo": "Lun-Mar-Mer-Jeu-Ven-Sam-Dim",
    "Nachladen wenn Boiler unter": "Recharge si ballon sous",
    "P.Luft 0% (Klappenspannung)": "Tension volet air primaire 0 %",
    "P.Luft 100% (Klappenspannung)": "Tension volet air primaire 100 %",
    "S.Luft 0% (Klappenspannung)": "Tension volet air secondaire 0 %",
    "S.Luft 100% (Klappenspannung)": "Tension volet air secondaire 100 %",
    "Puffer": "Ballon tampon",
    "Puffer oben Min.Temp": "Température min. haut de ballon",
    "Pufferpumpe min. Drehz.": "Vitesse min. pompe ballon",
    "Puffertemp.Heiz- kreisfreig": "Temp. ballon de libération des circuits",
    "RBG 3100 Zuord.:": "Affectation RBG 3100 :",
    "Raumtemperatur Sollwert": "Consigne température pièce",
    "Raumtemp.Sollw. Absenkbetr": "Consigne température pièce (mode réduit)",
    "Restsauerstoff Feuer-AUS": "Oxygène résiduel à l'extinction du feu",
    "Restsauerstoffgehalt Soll": "Consigne oxygène résiduel",
    "Restsauerstoff- gehaltSoll": "Consigne oxygène résiduel",
    "Rückl. Sollw": "Consigne de retour",
    "Rücklaufanhebepumpe Min.Drehz.": "Vitesse min. pompe de relance de retour",
    "Vorlauftemp. Absenk.um": "Abaissement de la température de départ",
    "Vorlauftemp. bei außen +10°C": "Temp. de départ pour +10 °C ext.",
    "Vorlauftemp. bei außen -10°C": "Temp. de départ pour -10 °C ext.",
    "Wochenprogramm": "Programme hebdomadaire",
    "nur 1x am Tag aufheizen": "Chauffe 1× par jour seulement",
}

# Textes avec numéro (Heizkreis 2, Heizzeit 3, Heizphase 1 Beginn, ...)
_MENU_PATTERNS_FR: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^heizkreis(\d+)$"), "Circuit de chauffage {n}"),
    (re.compile(r"^heizkreis(\d+)frostschutztemperatur$"), "Température antigel circuit {n}"),
    (re.compile(r"^heizkreis(\d+)mischerlaufzeit$"), "Durée de course du mélangeur circuit {n}"),
    (re.compile(r"^heizkreis(\d+)vorlauftempmaximalwert$"), "Température de départ max. circuit {n}"),
    (re.compile(r"^heizzeit(\d+)$"), "Programme horaire {n}"),
    (re.compile(r"^heizphase(\d+)beginn$"), "Début phase de chauffe {n}"),
    (re.compile(r"^heizphase(\d+)ende$"), "Fin phase de chauffe {n}"),
]

_MENU_TEXTS_FR_NORM = {
    _NORMALIZE_PATTERN.sub("", key.lower()): value for key, value in _MENU_TEXTS_FR.items()
}


def translate_menu_text(text: str) -> str:
    """Traduit un texte de menu allemand en français, tel quel si inconnu."""
    key = _NORMALIZE_PATTERN.sub("", text.lower())
    if key in _MENU_TEXTS_FR_NORM:
        return _MENU_TEXTS_FR_NORM[key]
    for pattern, template in _MENU_PATTERNS_FR:
        if match := pattern.match(key):
            return template.format(n=match.group(1))
    return text
