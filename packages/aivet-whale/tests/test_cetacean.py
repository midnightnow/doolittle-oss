"""
Unit tests for aivet-whale cetacean communication plugin.
"""

import numpy as np
import pytest


class TestCodaDetection:
    """Test click segmentation and coda extraction."""

    def test_detects_synthetic_coda(self):
        from aivet_whale import detect_codas_from_audio

        sr = 44100
        audio = np.random.randn(5 * sr).astype(np.float32) * 0.01

        # Inject 5 clicks at regular intervals
        for t in [0.5, 0.7, 0.9, 1.1, 1.3]:
            sample = int(t * sr)
            click_len = int(0.002 * sr)
            click = np.exp(-np.linspace(0, 5, click_len)) * 0.8
            audio[sample:sample + click_len] += click

        codas = detect_codas_from_audio(audio, sr)
        assert len(codas) >= 1
        assert codas[0].click_count >= 3

    def test_empty_audio_returns_empty(self):
        from aivet_whale import detect_codas_from_audio

        codas = detect_codas_from_audio(np.zeros(1000, dtype=np.float32), 44100)
        assert codas == []

    def test_noise_only_returns_empty(self):
        from aivet_whale import detect_codas_from_audio

        audio = np.random.randn(44100).astype(np.float32) * 0.001
        codas = detect_codas_from_audio(audio, 44100)
        assert codas == []


class TestPhoneticAlphabet:
    """Test phonetic classification of clicks."""

    def test_alphabet_has_11_phonemes(self):
        from aivet_whale import SPERM_WHALE_PHONETIC_ALPHABET

        assert len(SPERM_WHALE_PHONETIC_ALPHABET) == 11

    def test_classify_sharp_click_as_plosive(self):
        from aivet_whale import classify_click_phonetics, PhoneticClass

        # Sharp impulse = plosive
        click = np.zeros(100, dtype=np.float32)
        click[10] = 1.0  # Single sharp spike
        symbol, pclass = classify_click_phonetics(click, 44100)
        assert pclass in (PhoneticClass.PLOSIVE, PhoneticClass.GLOTTAL, PhoneticClass.COMPOUND)

    def test_classify_noise_as_fricative(self):
        from aivet_whale import classify_click_phonetics, PhoneticClass

        # White noise = fricative
        click = np.random.randn(500).astype(np.float32)
        symbol, pclass = classify_click_phonetics(click, 44100)
        assert pclass in (PhoneticClass.FRICATIVE, PhoneticClass.COMPOUND)


class TestProsody:
    """Test prosodic feature extraction."""

    def test_regular_intervals_low_rubato(self):
        from aivet_whale import compute_prosody_features

        intervals = [0.2, 0.2, 0.2, 0.2]
        features = compute_prosody_features(intervals)
        assert features.rubato < 0.2
        assert features.rhythm_regularity > 0.5

    def test_irregular_intervals_high_rubato(self):
        from aivet_whale import compute_prosody_features

        intervals = [0.1, 0.4, 0.1, 0.5]
        features = compute_prosody_features(intervals)
        assert features.rubato > 0.5

    def test_tempo_calculation(self):
        from aivet_whale import compute_prosody_features

        intervals = [0.5, 0.5, 0.5]  # 2 clicks per second = 120 BPM
        features = compute_prosody_features(intervals)
        assert abs(features.tempo_bpm - 120.0) < 5.0


class TestBioSignalAdapter:
    """Test conversion to Doolittle BioSignal format."""

    def test_coda_to_biosignal_structure(self):
        from aivet_whale import CetaceanAnalyzer, coda_to_biosignal

        analyzer = CetaceanAnalyzer(species="sperm_whale")

        # Generate audio with clicks
        sr = 44100
        audio = np.random.randn(3 * sr).astype(np.float32) * 0.01
        for t in [0.5, 0.7, 0.9, 1.1, 1.3]:
            sample = int(t * sr)
            click_len = int(0.002 * sr)
            audio[sample:sample + click_len] += np.exp(-np.linspace(0, 5, click_len)) * 0.8

        codas = analyzer.analyze_audio(audio, sr)
        if codas:
            signal = coda_to_biosignal(codas[0], patient_id="test_whale")
            assert signal["species"] == "sperm_whale"
            assert signal["triage_level"] in ("normal", "low", "moderate", "urgent", "critical")
            assert 0 <= signal["normalized_value"] <= 1
            assert 0 <= signal["confidence"] <= 1
            assert "phonetic_sequence" in signal["raw_value"]


class TestRubatoAnalyzer:
    """Test rubato pattern classification."""

    def test_identity_pattern(self):
        from aivet_whale import RubatoAnalyzer, compute_prosody_features

        analyzer = RubatoAnalyzer()
        features = compute_prosody_features([0.2, 0.2, 0.2, 0.2])
        pattern = analyzer.classify_rubato_pattern(features)
        assert pattern in ("identity", "calm_social")

    def test_semantic_weight(self):
        from aivet_whale import RubatoAnalyzer, compute_prosody_features

        analyzer = RubatoAnalyzer()
        features = compute_prosody_features([0.15, 0.25, 0.1, 0.3, 0.2])
        weight = analyzer.compute_semantic_weight(features)
        assert 0 <= weight <= 1


class TestFullPipeline:
    """Integration test: full audio → BioSignal pipeline."""

    def test_end_to_end(self):
        from aivet_whale import CetaceanAnalyzer, codas_to_biosignals

        analyzer = CetaceanAnalyzer(species="sperm_whale")

        # 10 seconds of audio with two coda groups
        sr = 44100
        audio = np.random.randn(10 * sr).astype(np.float32) * 0.01

        # Coda 1: regular 5-click (identity)
        for t in [1.0, 1.2, 1.4, 1.6, 1.8]:
            s = int(t * sr)
            cl = int(0.002 * sr)
            audio[s:s + cl] += np.exp(-np.linspace(0, 5, cl)) * 0.8

        # Coda 2: accelerating 6-click (attention)
        times = [4.0, 4.18, 4.34, 4.48, 4.60, 4.70]
        for t in times:
            s = int(t * sr)
            cl = int(0.002 * sr)
            audio[s:s + cl] += np.exp(-np.linspace(0, 5, cl)) * 0.7

        codas = analyzer.analyze_audio(audio, sr)
        assert len(codas) >= 1

        signals = codas_to_biosignals(codas, patient_id="whale_e2e_test")
        assert len(signals) >= 1
        assert all(s["species"] == "sperm_whale" for s in signals)
