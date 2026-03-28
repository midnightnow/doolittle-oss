"""
The main AiVet pipeline orchestrator.

Coordinates vision, audio, and fusion primitives to produce
unified triage assessments using SDK types.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import numpy as np

from vetsorcery_sdk.types import ClinicalResult, TriageLevel

@dataclass
class PipelineContext:
    """Shared context for a triage session."""
    session_id: str
    species: str
    patient_id: Optional[str] = None
    metadata: Dict[str, Any] = None

class AiVetPipeline:
    """
    Main orchestrator for the AiVet system.

    Coordinates:
    - Vision primitives (grimace, vitals)
    - Audio primitives (vocalization)
    - Fusion engine (Bayesian combination)
    - Output formatting into ClinicalResult
    """

    def __init__(self, context: PipelineContext):
        self.context = context
        # Lazy-load primitives to reduce startup time
        self._grimace = None
        self._vocal = None
        self._fusion = None

    def process_frame(
        self,
        image: Optional[np.ndarray] = None,
        audio: Optional[np.ndarray] = None,
    ) -> ClinicalResult:
        """
        Process a single frame (image + optional audio).

        Returns a unified ClinicalResult.
        """
        results = {}

        # Run vision if image provided
        if image is not None:
            results["vision"] = self._process_vision(image)

        # Run audio if audio provided
        if audio is not None:
            results["audio"] = self._process_audio(audio)

        # Fuse if we have any signals
        if results:
            triage_data = self._fuse_signals(results)
            
            # Map internal triage dict to standard ClinicalResult
            return ClinicalResult(
                pain_probability=triage_data.get("pain_probability", 0.0),
                triage_level=triage_data.get("triage_level", TriageLevel.ROUTINE),
                confidence=triage_data.get("confidence", 0.0),
                recommendations=triage_data.get("recommendations", [])
            )

        # Fallback if nothing to process
        return ClinicalResult(
            pain_probability=0.0,
            triage_level=TriageLevel.ROUTINE,
            confidence=0.0,
            recommendations=["No input provided."]
        )

    def _process_vision(self, image: np.ndarray) -> Dict[str, Any]:
        """Process visual input."""
        return {"status": "not_implemented", "pain_probability": 0.5, "confidence": 0.5}

    def _process_audio(self, audio: np.ndarray) -> Dict[str, Any]:
        """Process audio input."""
        return {"status": "not_implemented"}

    def _fuse_signals(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """Fuse all signals into unified assessment."""
        # Simple mock logic for demonstration
        vision_prob = signals.get("vision", {}).get("pain_probability", 0.0)
        triage = TriageLevel.ROUTINE
        if vision_prob > 0.7:
            triage = TriageLevel.URGENT
        elif vision_prob > 0.4:
            triage = TriageLevel.SOON
            
        return {
            "pain_probability": vision_prob,
            "triage_level": triage,
            "confidence": 0.8,
            "recommendations": ["Generated via unified Doolittle-OSS"]
        }
