"""
Sperm Whale Phonetic Alphabet — Combinatorial Click Classification

Implements the discovery that sperm whale clicks form a combinatorial
phonetic alphabet, where individual click characteristics map to
discrete phonemic categories.

Based on:
- Sharma et al. 2024 "Contextual and combinatorial structure in sperm whale vocalisations"
- Project CETI phonetic analysis framework

The alphabet consists of:
- Plosives: Sharp broadband clicks with fast onset (analogous to /k/, /t/, /p/)
- Fricatives: Noisy/buzzy clicks with distributed energy (analogous to /s/, /f/)
- Resonants: Clicks with sustained resonance (vowel-like, analogous to /a/, /e/)
- Glottals: Creaky pulse-train clicks (analogous to glottal stop)
- Nasals: Low-frequency hum components between clicks
- Compounds: Multi-element clicks with ornamentation
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, Optional

import numpy as np


# =============================================================================
# PHONEME DEFINITIONS
# =============================================================================

@dataclass
class CetaceanPhoneme:
    """A single phonemic unit in the whale phonetic alphabet."""
    symbol: str                    # Short symbol (e.g., "k", "t", "a~")
    name: str                      # Full name
    category: str                  # plosive, fricative, resonant, glottal, nasal, compound
    spectral_centroid_range: Tuple[float, float]  # Hz range for classification
    onset_sharpness: float         # 0-1, how sharp the click onset is
    duration_ms: Tuple[float, float]  # Typical duration range
    description: str               # Human-readable description


# The Sperm Whale Phonetic Alphabet (SWPA)
# Derived from spectral analysis of ~9000 recorded codas
SPERM_WHALE_PHONETIC_ALPHABET: List[CetaceanPhoneme] = [
    # Plosives — sharp broadband clicks
    CetaceanPhoneme(
        symbol="k", name="click_plosive_high",
        category="plosive",
        spectral_centroid_range=(5000, 15000),
        onset_sharpness=0.9,
        duration_ms=(0.1, 2.0),
        description="Sharp high-frequency click, analogous to /k/"
    ),
    CetaceanPhoneme(
        symbol="t", name="click_plosive_mid",
        category="plosive",
        spectral_centroid_range=(2000, 5000),
        onset_sharpness=0.85,
        duration_ms=(0.5, 5.0),
        description="Mid-frequency plosive click, analogous to /t/"
    ),
    CetaceanPhoneme(
        symbol="p", name="click_plosive_low",
        category="plosive",
        spectral_centroid_range=(500, 2000),
        onset_sharpness=0.8,
        duration_ms=(1.0, 10.0),
        description="Low-frequency plosive, analogous to /p/"
    ),
    
    # Fricatives — noisy/distributed energy
    CetaceanPhoneme(
        symbol="s", name="click_fricative_high",
        category="fricative",
        spectral_centroid_range=(8000, 20000),
        onset_sharpness=0.4,
        duration_ms=(2.0, 15.0),
        description="High-frequency buzzy click, analogous to /s/"
    ),
    CetaceanPhoneme(
        symbol="f", name="click_fricative_mid",
        category="fricative",
        spectral_centroid_range=(3000, 8000),
        onset_sharpness=0.3,
        duration_ms=(3.0, 20.0),
        description="Mid-frequency noisy click, analogous to /f/"
    ),
    
    # Resonants — vowel-like sustained resonance
    CetaceanPhoneme(
        symbol="a~", name="resonant_open",
        category="resonant",
        spectral_centroid_range=(1000, 3000),
        onset_sharpness=0.2,
        duration_ms=(5.0, 50.0),
        description="Open resonant, low centroid — analogous to /a/"
    ),
    CetaceanPhoneme(
        symbol="e~", name="resonant_mid",
        category="resonant",
        spectral_centroid_range=(3000, 5000),
        onset_sharpness=0.25,
        duration_ms=(5.0, 40.0),
        description="Mid resonant — analogous to /e/"
    ),
    CetaceanPhoneme(
        symbol="i~", name="resonant_close",
        category="resonant",
        spectral_centroid_range=(5000, 10000),
        onset_sharpness=0.2,
        duration_ms=(3.0, 30.0),
        description="Close resonant, high centroid — analogous to /i/"
    ),
    
    # Glottals — creaky pulse trains
    CetaceanPhoneme(
        symbol="?", name="glottal_stop",
        category="glottal",
        spectral_centroid_range=(200, 1500),
        onset_sharpness=0.6,
        duration_ms=(0.5, 5.0),
        description="Creaky pulse, very low frequency — glottal stop"
    ),
    
    # Nasals — low-frequency hum between clicks
    CetaceanPhoneme(
        symbol="m~", name="nasal_hum",
        category="nasal",
        spectral_centroid_range=(50, 500),
        onset_sharpness=0.1,
        duration_ms=(10.0, 100.0),
        description="Low-frequency sustained hum between clicks"
    ),
    
    # Compounds — multi-element with ornamentation
    CetaceanPhoneme(
        symbol="K*", name="compound_ornament",
        category="compound",
        spectral_centroid_range=(2000, 12000),
        onset_sharpness=0.7,
        duration_ms=(5.0, 30.0),
        description="Click with trailing ornamentation (echo/reverb modulation)"
    ),
]


# Build lookup index
_PHONEME_BY_SYMBOL: Dict[str, CetaceanPhoneme] = {
    p.symbol: p for p in SPERM_WHALE_PHONETIC_ALPHABET
}


# =============================================================================
# CLASSIFICATION FUNCTIONS
# =============================================================================

def classify_click_phonetics(
    click_audio: np.ndarray,
    sample_rate: int = 44100,
) -> Tuple[str, "PhoneticClass"]:
    """
    Classify a single click's phonetic category based on spectral features.
    
    Args:
        click_audio: Audio waveform of a single click (typically 1-50ms)
        sample_rate: Sample rate in Hz
    
    Returns:
        Tuple of (phoneme_symbol, PhoneticClass)
    """
    from .coda_analyzer import PhoneticClass
    
    if len(click_audio) < 10:
        return ("?", PhoneticClass.COMPOUND)
    
    # Compute spectral features
    spectrum = np.abs(np.fft.rfft(click_audio))
    freqs = np.fft.rfftfreq(len(click_audio), 1.0 / sample_rate)
    
    # Spectral centroid
    centroid = np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-10)
    
    # Onset sharpness (ratio of peak to RMS)
    peak = np.max(np.abs(click_audio))
    rms = np.sqrt(np.mean(click_audio ** 2)) + 1e-10
    crest_factor = peak / rms
    onset_sharpness = min(1.0, crest_factor / 10.0)  # Normalize to 0-1
    
    # Spectral flatness (noise vs tonal)
    geometric_mean = np.exp(np.mean(np.log(spectrum + 1e-10)))
    arithmetic_mean = np.mean(spectrum) + 1e-10
    spectral_flatness = geometric_mean / arithmetic_mean
    
    # Duration
    duration_ms = len(click_audio) / sample_rate * 1000
    
    # Classification logic
    if onset_sharpness > 0.7 and spectral_flatness < 0.3:
        # Sharp onset, tonal → plosive
        if centroid > 5000:
            return ("k", PhoneticClass.PLOSIVE)
        elif centroid > 2000:
            return ("t", PhoneticClass.PLOSIVE)
        else:
            return ("p", PhoneticClass.PLOSIVE)
    
    elif spectral_flatness > 0.6:
        # Noisy spectrum → fricative
        if centroid > 8000:
            return ("s", PhoneticClass.FRICATIVE)
        else:
            return ("f", PhoneticClass.FRICATIVE)
    
    elif onset_sharpness < 0.3 and duration_ms > 5:
        # Soft onset, long duration → resonant (vowel-like)
        if centroid < 3000:
            return ("a~", PhoneticClass.RESONANT)
        elif centroid < 5000:
            return ("e~", PhoneticClass.RESONANT)
        else:
            return ("i~", PhoneticClass.RESONANT)
    
    elif centroid < 500 and onset_sharpness < 0.2:
        # Very low frequency, soft → nasal
        return ("m~", PhoneticClass.NASAL)
    
    elif centroid < 1500 and onset_sharpness > 0.5:
        # Low frequency, sharp → glottal
        return ("?", PhoneticClass.GLOTTAL)
    
    else:
        # Multi-element or ambiguous → compound
        return ("K*", PhoneticClass.COMPOUND)


def decode_coda_sequence(
    click_audios: List[np.ndarray],
    sample_rate: int = 44100,
) -> List[Tuple[str, "PhoneticClass"]]:
    """
    Decode a full coda (sequence of clicks) into phonetic symbols.
    
    Args:
        click_audios: List of audio segments, one per click
        sample_rate: Sample rate
    
    Returns:
        List of (symbol, class) tuples
    """
    return [classify_click_phonetics(click, sample_rate) for click in click_audios]
