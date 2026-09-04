import pytest

from depth_gap_gain.interventions import expected_module_sources, validate_wiring


def test_s16_wiring():
    wiring = expected_module_sources(16)
    assert wiring["llm.layers.11"] == "Base"
    assert wiring["llm.layers.12"] == "Full-SFT"
    assert wiring["llm.embed_tokens"] == "Base"
    assert wiring["audio_heads"] == "Base"
    validate_wiring(wiring, 16)


def test_wiring_fails_closed_on_embedding_drift():
    wiring = expected_module_sources(28)
    wiring["llm.embed_tokens"] = "Full-SFT"
    with pytest.raises(ValueError):
        validate_wiring(wiring, 28)
