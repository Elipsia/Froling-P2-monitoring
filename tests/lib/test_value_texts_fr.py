"""Tests de la traduction française des valeurs textuelles."""

import importlib.util
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).parent.parent.parent
    / "custom_components"
    / "froeling_s3100"
    / "value_texts_fr.py"
)
_spec = importlib.util.spec_from_file_location("value_texts_fr", _MODULE_PATH)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

translate_value_text = _mod.translate_value_text


def test_operating_modes_are_translated() -> None:
    assert translate_value_text("Winterbetrieb") == "Mode hiver"
    assert translate_value_text("Sommerbetrieb") == "Mode été"
    assert translate_value_text("Übergangsbetr.") == "Mode intermédiaire"
    assert translate_value_text("Scheitholzbetr") == "Mode bois"


def test_statuses_are_translated() -> None:
    assert translate_value_text("Betriebsbereit") == "Prêt"
    assert translate_value_text("Heizen") == "En chauffe"
    assert translate_value_text("Anheizen") == "Montée en température"
    assert translate_value_text("Feuer-Aus") == "Feu éteint"
    assert translate_value_text("Störung") == "Défaut"


def test_trailing_spaces_are_ignored() -> None:
    assert translate_value_text("Winterbetrieb ") == "Mode hiver"
    assert translate_value_text(" Reinigen    ") == "Nettoyage"


def test_unknown_values_are_passed_through() -> None:
    assert translate_value_text("Selbstreinigung") == "Selbstreinigung"


def test_none_and_empty_are_passed_through() -> None:
    assert translate_value_text(None) is None
    assert translate_value_text("") == ""
