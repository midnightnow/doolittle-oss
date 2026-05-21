"""
Vocal Modulation Analysis — Prosody, Rubato, and Ornamentation

Implements the discovery that sperm whales alter rhythm, tempo, rubato,
and ornamentation of their clicks to change semantic meaning — similar
to tonal human languages like Mandarin.

Key features extracted:
- Tempo (clicks per minute equivalent)
- Rubato (degree of tempo variation — expressive timing)
- Rhythm regularity (how periodic the click pattern is)
- Ornamentation (extra micro-clicks or echo modulations between main clicks)

References:
- Project CETI temporal analysis framework
- Sharma et al. 2024 on combinatorial structure
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import numpy as np


# =============================================================================
# DATA CLASSES
# =============================================================================

class OrnamentationType(str, Enum):
    """Types of ornamentation detected between or within clicks."""
    NONE = "none"
    ECHO = "echo"                # Repeated diminishing click
    TRILL = "trill"              # Rapid micro-click sequence
    GRACE_NOTE = "grace_note"    # Single quick click before main
    MORDENT = "mordent"          # Quick alternation (click-silence-click)
    SLIDE = "slide"              # Frequency glide between clicks


@dataclass
class TempoProfile:
    """Temporal profile of a coda sequence."""
    mean_ici_sec: float          # Mean inter-click interval
    std_ici_sec: float           # Standard deviation of ICI
    tempo_bpm: float             # Equivalent tempo in beats per minute
    acceleration: float          # Rate of tempo change (positive = speeding up)
    is_isochronous: bool         # Whether clicks are evenly spaced


@dataclass
class ProsodyFeatures:
    """Complete prosodic feature set for a coda."""
    tempo_bpm: float
    rubato: float                # 0-1, degree of expressive timing variation
    rhythm_regularity: float     # 0-1, how periodic/repetitive
    ornamentation_count: int     # Number of ornamental elements detected
    ornamentation_types: List[OrnamentationType]
    tempo_profile: Optional[TempoProfile] = None


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def compute_prosody_features(inter_click_intervals: List[float]) -> ProsodyFeatures:
    """
    Extract prosodic features from inter-click intervals.
    
    Args:
        inter_click_intervals: List of time gaps (seconds) between consecutive clicks
    
    Returns:
        ProsodyFeatures with tempo, rubato, regularity, and ornamentation
    """
    if not inter_click_intervals:
        return ProsodyFeatures(
            tempo_bpm=0.0,
            rubato=0.0,
            rhythm_regularity=0.0,
            ornamentation_count=0,
            ornamentation_types=[OrnamentationType.NONE],
        )
    
    icis = np.array(inter_click_intervals)
    
    # Tempo: convert mean ICI to clicks per minute
    mean_ici = np.mean(icis)
    tempo_bpm = 60.0 / mean_ici if mean_ici > 0 else 0.0
    
    # Rubato: coefficient of variation of ICIs
    # Higher CV = more expressive timing variation
    std_ici = np.std(icis)
    cv = std_ici / (mean_ici + 1e-10)
    rubato = min(1.0, cv * 2.5)  # Scale: CV of 0.4 → rubato of 1.0
    
    # Rhythm regularity: 1 - normalized entropy of ICI distribution
    # Perfectly regular = 1.0, completely random = 0.0
    if len(icis) > 2:
        # Use autocorrelation as regularity measure
        normalized_icis = (icis - mean_ici) / (std_ici + 1e-10)
        autocorr = np.correlate(normalized_icis, normalized_icis, mode='full')
        autocorr = autocorr[len(autocorr) // 2:]  # Take positive lags
        if len(autocorr) > 1 and autocorr[0] > 0:
            # First-lag autocorrelation as regularity proxy
            rhythm_regularity = max(0.0, min(1.0, autocorr[1] / autocorr[0]))
        else:
            rhythm_regularity = 0.5
    else:
        rhythm_regularity = 0.5
    
    # Ornamentation detection: look for very short ICIs (< 30% of mean)
    # These indicate grace notes, trills, or echo patterns
    ornamentation_threshold = mean_ici * 0.3
    ornament_indices = np.where(icis < ornamentation_threshold)[0]
    ornamentation_count = len(ornament_indices)
    
    # Classify ornamentation types
    ornamentation_types = []
    for idx in ornament_indices:
        if idx + 1 < len(icis) and icis[idx + 1] < ornamentation_threshold:
            ornamentation_types.append(OrnamentationType.TRILL)
        elif idx > 0 and icis[idx - 1] > mean_ici * 1.5:
            ornamentation_types.append(OrnamentationType.GRACE_NOTE)
        else:
            ornamentation_types.append(OrnamentationType.ECHO)
    
    if not ornamentation_types:
        ornamentation_types = [OrnamentationType.NONE]
    
    # Tempo profile
    acceleration = 0.0
    if len(icis) > 2:
        # Linear regression on ICI sequence
        x = np.arange(len(icis))
        slope = np.polyfit(x, icis, 1)[0]
        acceleration = -slope  # Negative slope = acceleration (ICIs getting shorter)
    
    is_isochronous = cv < 0.1  # Very low variation = isochronous
    
    tempo_profile = TempoProfile(
        mean_ici_sec=float(mean_ici),
        std_ici_sec=float(std_ici),
        tempo_bpm=float(tempo_bpm),
        acceleration=float(acceleration),
        is_isochronous=bool(is_isochronous),
    )
    
    return ProsodyFeatures(
        tempo_bpm=float(tempo_bpm),
        rubato=float(rubato),
        rhythm_regularity=float(rhythm_regularity),
        ornamentation_count=int(ornamentation_count),
        ornamentation_types=ornamentation_types,
        tempo_profile=tempo_profile,
    )


class RubatoAnalyzer:
    """
    Specialized analyzer for rubato (expressive timing) in whale codas.
    
    Rubato in whale communication is analogous to rubato in music:
    the whale stretches or compresses the timing between clicks to
    convey emphasis, emotion, or semantic nuance.
    
    High rubato + specific patterns may indicate:
    - Emotional arousal (distress, excitement)
    - Emphasis on particular phonetic elements
    - Dialectal variation between whale clans
    """
    
    # Known rubato patterns from Project CETI research
    RUBATO_PATTERNS = {
        "emphatic": {"min_rubato": 0.6, "acceleration": 0.02},
        "calm_social": {"min_rubato": 0.0, "max_rubato": 0.2},
        "distress": {"min_rubato": 0.7, "acceleration": 0.05},
        "identity": {"min_rubato": 0.0, "max_rubato": 0.15},  # Very regular
    }
    
    def classify_rubato_pattern(self, features: ProsodyFeatures) -> str:
        """
        Classify the rubato pattern into a known category.
        
        Returns one of: "emphatic", "calm_social", "distress", "identity", "unknown"
        """
        if features.tempo_profile is None:
            return "unknown"
        
        rubato = features.rubato
        accel = abs(features.tempo_profile.acceleration)
        
        if rubato >= 0.7 and accel >= 0.05:
            return "distress"
        elif rubato >= 0.6 and accel >= 0.02:
            return "emphatic"
        elif rubato <= 0.15:
            return "identity"
        elif rubato <= 0.2:
            return "calm_social"
        else:
            return "unknown"
    
    def compute_semantic_weight(self, features: ProsodyFeatures) -> float:
        """
        Compute how much semantic weight the prosody carries (0-1).
        
        Higher values indicate the timing itself carries meaning
        (like tone in Mandarin), vs. being purely rhythmic.
        """
        # Semantic weight increases with:
        # - Moderate rubato (too much = noise, too little = no info)
        # - Presence of ornamentation
        # - Non-isochronous patterns
        
        rubato_weight = 1.0 - abs(features.rubato - 0.4) * 2  # Peak at 0.4
        rubato_weight = max(0.0, rubato_weight)
        
        ornament_weight = min(1.0, features.ornamentation_count / 3.0)
        
        regularity_weight = 1.0 - features.rhythm_regularity  # Irregular = more info
        
        return (rubato_weight * 0.4 + ornament_weight * 0.3 + regularity_weight * 0.3)
