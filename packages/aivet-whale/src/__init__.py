"""
aivet-whale: Sperm Whale Communication Primitive for Doolittle-OSS

Implements Project CETI / WhAM research findings:
- Combinatorial Phonetic Alphabet (156 coda classes, 11 spectral categories)
- Vowel-like resonant frequency modulation (e-coda / i-coda)
- Prosodic variation (rubato, tempo, ornamentation)
- Coarticulation tracking
- Welfare assessment from communication patterns

Usage:
    from aivet_whale import CetaceanAnalyzer, coda_to_biosignal
    
    analyzer = CetaceanAnalyzer(species="sperm_whale")
    codas = analyzer.analyze_audio(audio, sample_rate=44100)
"""

__version__ = "0.1.0"

from .coda_analyzer import (
    CetaceanAnalyzer,
    CodaPattern,
    CodaType,
    PhoneticClass,
    detect_codas_from_audio,
)
from .phonetic_alphabet import (
    SPERM_WHALE_PHONETIC_ALPHABET,
    CetaceanPhoneme,
    classify_click_phonetics,
    decode_coda_sequence,
)
from .vocal_modulation import (
    RubatoAnalyzer,
    TempoProfile,
    ProsodyFeatures,
    OrnamentationType,
    compute_prosody_features,
)
from .biosignal_adapter import (
    coda_to_biosignal,
    codas_to_biosignals,
    CetaceanSignalSource,
)

__all__ = [
    "CetaceanAnalyzer",
    "CodaPattern",
    "CodaType",
    "PhoneticClass",
    "detect_codas_from_audio",
    "SPERM_WHALE_PHONETIC_ALPHABET",
    "CetaceanPhoneme",
    "classify_click_phonetics",
    "decode_coda_sequence",
    "RubatoAnalyzer",
    "TempoProfile",
    "ProsodyFeatures",
    "OrnamentationType",
    "compute_prosody_features",
    "coda_to_biosignal",
    "codas_to_biosignals",
    "CetaceanSignalSource",
]
