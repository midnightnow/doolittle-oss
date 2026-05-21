"""
BioSignal Adapter — Converts cetacean analysis results to Doolittle BioSignal format.

This module bridges the cetacean-specific analysis (CodaPattern) to the
universal Doolittle BioSignal schema, enabling fusion with other modalities
(e.g., aerial observation, satellite tracking, behavioral analysis).
"""

import time
import uuid
from enum import Enum
from typing import List, Dict, Any, Optional

from .coda_analyzer import CodaPattern, CodaType


# =============================================================================
# EXTENDED SIGNAL SOURCES FOR CETACEANS
# =============================================================================

class CetaceanSignalSource(str, Enum):
    """Signal sources specific to cetacean communication analysis."""
    AUDIO_WHALE_CODA = "audio_whale_coda"
    AUDIO_WHALE_PHONETICS = "audio_whale_phonetics"
    AUDIO_WHALE_VOWEL_MOD = "audio_whale_vowel_mod"
    AUDIO_WHALE_PROSODY = "audio_whale_prosody"
    AUDIO_WHALE_COMPOSITE = "audio_whale_composite"


# =============================================================================
# BIOSIGNAL CONVERSION
# =============================================================================

def coda_to_biosignal(
    coda: CodaPattern,
    patient_id: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convert a CodaPattern to a Doolittle-compatible BioSignal dictionary.
    
    This produces a signal that can be ingested by the Doolittle fusion engine
    alongside vision signals (e.g., surface behavior observation).
    
    Args:
        coda: Analyzed CodaPattern from CetaceanAnalyzer
        patient_id: Optional patient/individual ID (e.g., whale photo-ID)
        session_id: Optional recording session ID
    
    Returns:
        Dictionary conforming to BioSignal schema
    """
    # Determine triage-equivalent level based on communication patterns
    # (In cetacean context, "triage" maps to welfare/distress assessment)
    welfare_level = _assess_welfare_from_coda(coda)
    
    return {
        "signal_id": f"whale_{coda.coda_id}",
        "patient_id": patient_id or f"whale_{uuid.uuid4().hex[:8]}",
        "species": "sperm_whale",
        "modality": "audio",
        "source": CetaceanSignalSource.AUDIO_WHALE_COMPOSITE.value,
        "timestamp": time.time(),
        
        # Core signal values
        "normalized_value": coda.communication_complexity,
        "confidence": coda.confidence,
        
        # Cetacean-specific payload
        "raw_value": {
            "coda_type": coda.coda_type.value,
            "click_count": coda.click_count,
            "duration_sec": coda.duration_sec,
            "phonetic_sequence": coda.phonetic_sequence,
            "vowel_modulation_strength": coda.vowel_modulation_strength,
            "estimated_vowel": coda.estimated_vowel,
            "tempo_bpm": coda.tempo_bpm,
            "rubato": coda.rubato,
            "rhythm_regularity": coda.rhythm_regularity,
            "ornamentation_count": coda.ornamentation_count,
            "semantic_context": coda.semantic_context,
        },
        
        # Welfare assessment
        "triage_level": welfare_level,
        "reasoning": _generate_reasoning(coda),
        
        # Metadata
        "session_id": session_id,
        "metadata": {
            "model": "aivet-whale/cetacean_analyzer",
            "version": "0.1.0",
            "research_citations": [
                "Project CETI 2025",
                "Sharma et al. 2024",
                "Gero et al. 2016",
            ],
        },
    }


def codas_to_biosignals(
    codas: List[CodaPattern],
    patient_id: Optional[str] = None,
    session_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Convert a list of CodaPatterns to BioSignal dictionaries."""
    return [
        coda_to_biosignal(coda, patient_id, session_id)
        for coda in codas
    ]


# =============================================================================
# WELFARE ASSESSMENT
# =============================================================================

def _assess_welfare_from_coda(coda: CodaPattern) -> str:
    """
    Assess welfare/distress level from communication patterns.
    
    In cetacean research, communication patterns correlate with welfare:
    - Normal social communication → healthy/normal
    - Reduced communication complexity → possible isolation/stress
    - High rubato + acceleration → possible distress
    - Very regular identity codas → normal clan behavior
    
    Returns: "normal", "low", "moderate", "urgent", "critical"
    """
    # Distress indicators
    distress_score = 0.0
    
    # High rubato with acceleration suggests agitation
    if coda.rubato > 0.6 and coda.coda_type == CodaType.ACCELERATING:
        distress_score += 0.4
    
    # Very short codas (< 3 clicks) may indicate interrupted communication
    if coda.click_count < 3:
        distress_score += 0.2
    
    # Absence of vowel modulation in normally complex codas
    if coda.click_count > 5 and coda.vowel_modulation_strength < 0.1:
        distress_score += 0.2
    
    # Very high ornamentation may indicate alarm
    if coda.ornamentation_count > 4:
        distress_score += 0.3
    
    # Map to triage levels
    if distress_score >= 0.7:
        return "urgent"
    elif distress_score >= 0.5:
        return "moderate"
    elif distress_score >= 0.3:
        return "low"
    else:
        return "normal"


def _generate_reasoning(coda: CodaPattern) -> List[str]:
    """Generate human-readable reasoning for the assessment."""
    reasons = []
    
    if coda.semantic_context:
        reasons.append(f"Semantic context: {coda.semantic_context}")
    
    if coda.phonetic_sequence:
        reasons.append(f"Phonetic sequence: {' '.join(coda.phonetic_sequence[:5])}")
    
    if coda.vowel_modulation_strength > 0.5:
        reasons.append(f"Strong vowel modulation detected (strength={coda.vowel_modulation_strength:.2f})")
    
    if coda.rubato > 0.5:
        reasons.append(f"High rubato ({coda.rubato:.2f}) — expressive timing variation")
    
    if coda.ornamentation_count > 0:
        reasons.append(f"{coda.ornamentation_count} ornamental elements detected")
    
    reasons.append(f"Communication complexity: {coda.communication_complexity:.2f}")
    
    return reasons
