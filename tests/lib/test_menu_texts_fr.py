"""Tests de la traduction française des textes de menu (paramètres)."""

import importlib.util
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).parent.parent.parent
    / "custom_components"
    / "froeling_s3100"
    / "menu_texts_fr.py"
)
_spec = importlib.util.spec_from_file_location("menu_texts_fr", _MODULE_PATH)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

translate_menu_text = _mod.translate_menu_text


def test_menu_sections_are_translated() -> None:
    assert translate_menu_text("Kesseltemp") == "Température chaudière"
    assert translate_menu_text("Heizzeiten") == "Programmes horaires"
    assert translate_menu_text("Wochenprogramm") == "Programme hebdomadaire"
    assert translate_menu_text("Puffer") == "Ballon tampon"
    assert translate_menu_text("Boiler") == "Ballon ECS"
    assert translate_menu_text("Heizkurve") == "Courbe de chauffe"
    assert translate_menu_text("EINSTELLEN") == "RÉGLAGES"


def test_numbered_entries_are_translated() -> None:
    assert translate_menu_text("Heizkreis 2") == "Circuit de chauffage 2"
    assert translate_menu_text("Heizzeit 3") == "Programme horaire 3"
    assert translate_menu_text("Heizphase 2 Beginn") == "Début phase de chauffe 2"
    assert translate_menu_text("Heizphase 1 Ende") == "Fin phase de chauffe 1"
    assert (
        translate_menu_text("Heizkreis 1 Frostschutztemperatur")
        == "Température antigel circuit 1"
    )


def test_line_broken_texts_are_translated() -> None:
    # le régulateur coupe parfois les textes longs sur deux lignes
    assert translate_menu_text("Beginn der 1.Puf ferladung") == "Début 1ʳᵉ charge ballon"
    assert translate_menu_text("Restsauerstoff- gehaltSoll") == "Consigne oxygène résiduel"
    assert translate_menu_text("Legionellen Aufheizung65°") == "Chauffe anti-légionelles 65 °C"


def test_unknown_text_passes_through() -> None:
    assert translate_menu_text("Nouveau texte inconnu") == "Nouveau texte inconnu"
