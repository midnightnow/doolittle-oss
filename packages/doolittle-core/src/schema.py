"""
Core schemas for the Doolittle ecosystem.

These types are shared across all packages to ensure consistent
data structures throughout the pipeline.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Import base types from the unified SDK
from vetsorcery_sdk.types import TriageLevel, ClinicalResult, Species as SDKSpecies

class Species(str, Enum):
    """Supported species for analysis."""
    CAT = "cat"
    DOG = "dog"
    RABBIT = "rabbit"
    HORSE = "horse"
    BIRD = "bird"
    UNKNOWN = "unknown"

class SignalSource(str, Enum):
    """Source of a biological signal."""
    VISION_GRIMACE = "vision_grimace"
    VISION_VITALS = "vision_vitals"
    VISION_POSE = "vision_pose"
    AUDIO_VOCAL = "audio_vocal"
    AUDIO_BREATHING = "audio_breathing"

class SignalModality(str, Enum):
    """Modality of the signal."""
    VISUAL = "visual"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"

class BioSignal(BaseModel):
    """
    Universal biological signal container.

    All primitives emit BioSignals that can be fused by the triage engine.
    """
    source: SignalSource
    species: Species
    raw_value: float | str | Dict[str, Any]
    normalized_value: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: float
    metadata: Dict[str, Any] = {}

    class Config:
        frozen = True

# PainAssessment is replaced by or extends ClinicalResult in actual use,
# but we keep it here as an intermediate Doolittle-specific object before 
# yielding the final ClinicalResult.
class PainAssessment(BaseModel):
    """Pain assessment result from any primitive or fusion."""
    pain_probability: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[SignalSource]
    modality: SignalModality
    timestamp: float

# TriageLevel is now imported directly from the SDK, so we do not redefine it here.

