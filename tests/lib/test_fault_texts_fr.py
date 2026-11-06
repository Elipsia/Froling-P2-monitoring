"""Tests de la traduction française des messages d'erreur."""

import importlib.util
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).parent.parent.parent
    / "custom_components"
    / "froeling_s3100"
    / "fault_texts_fr.py"
)
_spec = importlib.util.spec_from_file_location("fault_texts_fr", _MODULE_PATH)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

translate_fault_text = _mod.translate_fault_text


def test_known_fault_texts_are_translated() -> None:
    assert (
        translate_fault_text("Kesseltemperatur zu gering")
        == "Température chaudière trop basse"
    )
    assert translate_fault_text("Zündung fehlgeschlagen") == "Échec de l'allumage"
    assert translate_fault_text("Asche entleeren") == "Vider le bac à cendres"


def test_matching_is_case_insensitive_and_ignores_separators() -> None:
    assert (
        translate_fault_text("KESSELTEMPERATUR ZU GERING")
        == "Température chaudière trop basse"
    )
    assert (
        translate_fault_text("Saugzuggebläse defekt")
        == "Ventilateur de tirage défectueux"
    )


def test_unknown_fault_text_is_flagged_but_kept() -> None:
    result = translate_fault_text("Turbinenwelle blockiert")
    assert "Turbinenwelle blockiert" in result
    assert result.startswith("Texte inconnu")


def test_none_and_empty_are_passed_through() -> None:
    assert translate_fault_text(None) is None
    assert translate_fault_text("") == ""


def test_abbreviated_texts_from_real_captures() -> None:
    assert (
        translate_fault_text("Kesseltemp.\nfehlerhaft")
        == "Sonde de température chaudière défectueuse"
    )
    assert (
        translate_fault_text("Sicherheitstemp.\n(STB) ausgelöst")
        == "Limiteur de température de sécurité déclenché (STB)"
    )
