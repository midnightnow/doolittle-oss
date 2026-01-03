"""
Core schemas for the Doolittle ecosystem.

These types are shared across all packages to ensure consistent
data structures throughout the pipeline.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

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

class PainAssessment(BaseModel):
    """Pain assessment result from any primitive or fusion."""
    pain_probability: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[SignalSource]
    modality: SignalModality
    timestamp: float

class TriageLevel(str, Enum):
    """Clinical triage urgency levels."""
    ROUTINE = "routine"
    LOW = "low"
    MODERATE = "moderate"
    URGENT = "urgent"
    EMERGENCY = "emergency"
