"""Tests for the measurement-name lookup table."""

from __future__ import annotations

from custom_components.froeling_s3100.measurements import lookup


def test_fill_level_aliases() -> None:
    """The pellet fill level is announced under several German spellings."""
    for name in ("Füllstand", "Fuellstand", "Füllst.", "Fuellst", "Füllst"):
        info, placeholders = lookup(name)
        assert info is not None, name
        assert info.translation_key == "fill_level"
        assert placeholders == {}


def test_known_measurement() -> None:
    info, placeholders = lookup("Kesseltemp")
    assert info is not None
    assert info.translation_key == "boiler_temperature"
    assert placeholders == {}


def test_supply_air_fan() -> None:
    info, _ = lookup("Zuluftgebl")
    assert info is not None
    assert info.translation_key == "supply_air_fan"


def test_numbered_measurement() -> None:
    info, placeholders = lookup("Vorlauft.2")
    assert info is not None
    assert info.translation_key == "flow_temperature"
    assert placeholders == {"number": "2"}


def test_unknown_name_passes_through() -> None:
    info, placeholders = lookup("UneInconnue")
    assert info is None
    assert placeholders == {}
