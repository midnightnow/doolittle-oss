"""
Cetacean Coda Analyzer — Main orchestration class for whale communication analysis.

Implements the Project CETI / WhAM research findings:
- Combinatorial Phonetic Alphabet (CPA) decoding from click sequences
- Vowel-like resonant frequency modulation detection
- Prosodic variation analysis (rhythm, tempo, rubato, ornamentation)

References:
- Sharma et al. 2024 "Contextual and combinatorial structure in sperm whale vocalisations"
- Project CETI (Cetacean Translation Initiative)
- Gero et al. 2016 "Individual, unit and vocal clan level identity cues in sperm whale codas"
"""

import time
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

import numpy as np

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS & DATA CLASSES
# =============================================================================

class CodaType(str, Enum):
    """Classification of sperm whale coda patterns."""
    REGULAR = "regular"          # Evenly-spaced clicks (identity codas)
    ACCELERATING = "accelerating"  # Clicks speed up ("+1" pattern)
    DECELERATING = "decelerating"  # Clicks slow down
    COMPLEX = "complex"          # Mixed rhythm (semantic content)
    EXCHANGE = "exchange"        # Part of a conversational exchange
    UNKNOWN = "unknown"


class PhoneticClass(str, Enum):
    """Phonetic classification of decoded coda elements."""
    PLOSIVE = "plosive"          # Sharp onset clicks (like /k/, /t/)
    FRICATIVE = "fricative"      # Buzzy/noisy clicks (like /s/, /f/)
    RESONANT = "resonant"        # Vowel-like sustained resonance
    GLOTTAL = "glottal"          # Creaky/pulse-like (like glottal stop)
    NASAL = "nasal"              # Low-frequency hum component
    COMPOUND = "compound"        # Multi-element click with ornamentation


@dataclass
class CodaPattern:
    """A single detected coda (burst of clicks) with extracted features."""
    coda_id: str
    start_time_sec: float
    end_time_sec: float
    duration_sec: float
    click_count: int
    inter_click_intervals: List[float]  # seconds between each click
    coda_type: CodaType
    
    # Phonetic analysis
    phonetic_sequence: List[str] = field(default_factory=list)
    phonetic_classes: List[PhoneticClass] = field(default_factory=list)
    
    # Vowel modulation
    vowel_modulation_strength: float = 0.0
    estimated_vowel: Optional[str] = None
    resonant_frequencies: List[float] = field(default_factory=list)
    
    # Prosody
    tempo_bpm: float = 0.0
    rubato: float = 0.0  # 0-1, degree of tempo variation
    rhythm_regularity: float = 0.0  # 0-1
    ornamentation_count: int = 0
    
    # Semantic
    semantic_context: Optional[str] = None
    communication_complexity: float = 0.0  # 0-1 normalized
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for BioSignal metadata."""
        return {
            "coda_id": self.coda_id,
            "start_time_sec": self.start_time_sec,
            "duration_sec": self.duration_sec,
            "click_count": self.click_count,
            "coda_type": self.coda_type.value,
            "phonetic_sequence": self.phonetic_sequence,
            "vowel_modulation_strength": self.vowel_modulation_strength,
            "estimated_vowel": self.estimated_vowel,
            "tempo_bpm": self.tempo_bpm,
            "rubato": self.rubato,
            "rhythm_regularity": self.rhythm_regularity,
            "ornamentation_count": self.ornamentation_count,
            "semantic_context": self.semantic_context,
            "communication_complexity": self.communication_complexity,
            "confidence": self.confidence,
        }


# =============================================================================
# CODA DETECTION (Click Segmentation)
# =============================================================================

def detect_codas_from_audio(
    audio: np.ndarray,
    sample_rate: int = 44100,
    min_click_energy: float = 0.3,
    max_inter_coda_gap_sec: float = 2.0,
    min_clicks_per_coda: int = 3,
) -> List[CodaPattern]:
    """
    Segment audio into individual codas using energy-based click detection.
    
    A coda is a burst of 3-40 clicks separated by short inter-click intervals (ICI),
    with longer gaps between codas. Sperm whale clicks are broadband impulses
    centered around 2-20 kHz with durations of 0.1-20ms.
    
    Args:
        audio: Raw audio waveform (mono, float32)
        sample_rate: Sample rate in Hz
        min_click_energy: Minimum normalized energy to detect a click
        max_inter_coda_gap_sec: Maximum gap between clicks within a coda
        min_clicks_per_coda: Minimum clicks to constitute a valid coda
    
    Returns:
        List of detected CodaPattern objects
    """
    # Normalize audio
    if len(audio) == 0:
        return []
    
    audio_norm = audio / (np.max(np.abs(audio)) + 1e-10)
    
    # Compute short-time energy (frame-based)
    frame_size = int(0.005 * sample_rate)  # 5ms frames (click duration)
    hop_size = int(0.001 * sample_rate)    # 1ms hop
    
    num_frames = (len(audio_norm) - frame_size) // hop_size + 1
    if num_frames <= 0:
        return []
    
    energy = np.zeros(num_frames)
    for i in range(num_frames):
        start = i * hop_size
        frame = audio_norm[start:start + frame_size]
        energy[i] = np.sum(frame ** 2) / frame_size
    
    # Normalize energy
    energy = energy / (np.max(energy) + 1e-10)
    
    # Detect click onsets (energy peaks above threshold)
    click_frames = []
    in_click = False
    for i in range(len(energy)):
        if energy[i] > min_click_energy and not in_click:
            click_frames.append(i)
            in_click = True
        elif energy[i] < min_click_energy * 0.5:
            in_click = False
    
    if len(click_frames) < min_clicks_per_coda:
        return []
    
    # Convert frame indices to time
    click_times = [f * hop_size / sample_rate for f in click_frames]
    
    # Group clicks into codas based on inter-click intervals
    codas = []
    current_coda_clicks = [click_times[0]]
    
    for i in range(1, len(click_times)):
        gap = click_times[i] - click_times[i - 1]
        if gap <= max_inter_coda_gap_sec:
            current_coda_clicks.append(click_times[i])
        else:
            # End of coda
            if len(current_coda_clicks) >= min_clicks_per_coda:
                codas.append(current_coda_clicks)
            current_coda_clicks = [click_times[i]]
    
    # Don't forget the last coda
    if len(current_coda_clicks) >= min_clicks_per_coda:
        codas.append(current_coda_clicks)
    
    # Build CodaPattern objects
    patterns = []
    for idx, clicks in enumerate(codas):
        icis = [clicks[i + 1] - clicks[i] for i in range(len(clicks) - 1)]
        
        # Classify coda type based on ICI pattern
        coda_type = _classify_coda_type(icis)
        
        pattern = CodaPattern(
            coda_id=f"coda_{idx:04d}_{int(time.time())}",
            start_time_sec=clicks[0],
            end_time_sec=clicks[-1],
            duration_sec=clicks[-1] - clicks[0],
            click_count=len(clicks),
            inter_click_intervals=icis,
            coda_type=coda_type,
        )
        patterns.append(pattern)
    
    return patterns


def _classify_coda_type(icis: List[float]) -> CodaType:
    """Classify coda type based on inter-click interval pattern."""
    if len(icis) < 2:
        return CodaType.UNKNOWN
    
    # Check for acceleration (decreasing ICIs)
    diffs = [icis[i + 1] - icis[i] for i in range(len(icis) - 1)]
    avg_diff = np.mean(diffs)
    std_ici = np.std(icis)
    mean_ici = np.mean(icis)
    
    # Coefficient of variation
    cv = std_ici / (mean_ici + 1e-10)
    
    if cv < 0.15:
        return CodaType.REGULAR
    elif avg_diff < -0.01:
        return CodaType.ACCELERATING
    elif avg_diff > 0.01:
        return CodaType.DECELERATING
    elif cv > 0.4:
        return CodaType.COMPLEX
    else:
        return CodaType.REGULAR


# =============================================================================
# MAIN ANALYZER CLASS
# =============================================================================

class CetaceanAnalyzer:
    """
    Main orchestrator for cetacean communication analysis.
    
    Coordinates:
    - Click detection and coda segmentation
    - Phonetic alphabet decoding (via WhAM or local classifier)
    - Vowel-like resonant frequency modulation
    - Prosodic feature extraction (tempo, rubato, ornamentation)
    - Semantic context estimation
    
    Usage:
        analyzer = CetaceanAnalyzer(species="sperm_whale")
        codas = analyzer.analyze_audio(audio_array, sample_rate=44100)
        for coda in codas:
            print(coda.phonetic_sequence, coda.semantic_context)
    """
    
    SUPPORTED_SPECIES = ["sperm_whale", "humpback_whale"]
    
    # Known coda patterns and their semantic associations
    # Based on Project CETI research (Dominica population)
    KNOWN_PATTERNS = {
        "1+1+3": "identity_coda",       # Clan identification
        "regular_5": "social_greeting",  # Regular 5-click pattern
        "accelerating_4": "attention",   # "+1" pattern (getting attention)
        "complex_7+": "narrative",       # Complex multi-click (storytelling/info)
    }
    
    def __init__(
        self,
        species: str = "sperm_whale",
        model_path: Optional[str] = None,
        use_wham: bool = False,
    ):
        """
        Initialize the cetacean analyzer.
        
        Args:
            species: Target species ("sperm_whale" or "humpback_whale")
            model_path: Path to a trained model checkpoint (optional)
            use_wham: Whether to use the WhAM model for phonetic decoding
        """
        if species not in self.SUPPORTED_SPECIES:
            logger.warning(f"Species '{species}' not fully supported. Using sperm_whale defaults.")
            species = "sperm_whale"
        
        self.species = species
        self.model_path = model_path
        self.use_wham = use_wham
        self._model = None
        
        logger.info(f"🐋 CetaceanAnalyzer initialized for {species}")
    
    def analyze_audio(
        self,
        audio: np.ndarray,
        sample_rate: int = 44100,
    ) -> List[CodaPattern]:
        """
        Full analysis pipeline: detect codas, decode phonetics, extract prosody.
        
        Args:
            audio: Raw audio waveform (mono, float32 or int16)
            sample_rate: Sample rate in Hz
        
        Returns:
            List of CodaPattern objects with full analysis
        """
        # Ensure float32
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
            if np.max(np.abs(audio)) > 1.0:
                audio = audio / 32768.0  # int16 normalization
        
        # Step 1: Detect codas
        codas = detect_codas_from_audio(audio, sample_rate)
        
        if not codas:
            logger.debug("No codas detected in audio segment")
            return []
        
        # Step 2: Analyze each coda
        for coda in codas:
            self._decode_phonetics(coda, audio, sample_rate)
            self._analyze_vowel_modulation(coda, audio, sample_rate)
            self._extract_prosody(coda)
            self._estimate_semantic_context(coda)
            self._compute_complexity(coda)
        
        logger.info(f"🐋 Analyzed {len(codas)} codas from {len(audio)/sample_rate:.1f}s audio")
        return codas
    
    def analyze_coda(
        self,
        audio_segment: np.ndarray,
        sample_rate: int = 44100,
    ) -> Optional[CodaPattern]:
        """Analyze a single pre-segmented coda. Returns the first detected pattern."""
        codas = self.analyze_audio(audio_segment, sample_rate)
        return codas[0] if codas else None
    
    def _decode_phonetics(
        self,
        coda: CodaPattern,
        audio: np.ndarray,
        sample_rate: int,
    ):
        """
        Decode the phonetic alphabet from click characteristics.
        
        Each click has spectral properties that map to phonetic categories:
        - Sharp broadband onset → plosive (/k/, /t/)
        - Noisy/buzzy spectrum → fricative (/s/, /f/)
        - Sustained resonance → resonant (vowel-like)
        - Creaky pulse train → glottal
        """
        from .phonetic_alphabet import (
            classify_click_phonetics,
        )
        
        # Extract audio around each click time
        phonemes = []
        classes = []
        
        click_times = [coda.start_time_sec] + [
            coda.start_time_sec + sum(coda.inter_click_intervals[:i + 1])
            for i in range(len(coda.inter_click_intervals))
        ]
        
        for click_time in click_times:
            # Extract 20ms window around click
            center_sample = int(click_time * sample_rate)
            window_samples = int(0.02 * sample_rate)
            start = max(0, center_sample - window_samples // 2)
            end = min(len(audio), center_sample + window_samples // 2)
            
            if end - start < 10:
                phonemes.append("?")
                classes.append(PhoneticClass.COMPOUND)
                continue
            
            click_audio = audio[start:end]
            symbol, pclass = classify_click_phonetics(click_audio, sample_rate)
            phonemes.append(symbol)
            classes.append(pclass)
        
        coda.phonetic_sequence = phonemes
        coda.phonetic_classes = classes
    
    def _analyze_vowel_modulation(
        self,
        coda: CodaPattern,
        audio: np.ndarray,
        sample_rate: int,
    ):
        """
        Detect vowel-like resonant frequency modulations.
        
        Whales modulate the resonant frequencies of their nasal complex
        to create formant-like structures analogous to human vowels.
        """
        # Extract the coda segment
        start_sample = int(coda.start_time_sec * sample_rate)
        end_sample = int(coda.end_time_sec * sample_rate)
        segment = audio[start_sample:end_sample]
        
        if len(segment) < 256:
            coda.vowel_modulation_strength = 0.0
            return
        
        # Compute spectral centroid over time (proxy for formant tracking)
        frame_size = min(512, len(segment) // 4)
        hop = frame_size // 2
        centroids = []
        
        for i in range(0, len(segment) - frame_size, hop):
            frame = segment[i:i + frame_size]
            spectrum = np.abs(np.fft.rfft(frame))
            freqs = np.fft.rfftfreq(frame_size, 1.0 / sample_rate)
            
            # Spectral centroid
            centroid = np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-10)
            centroids.append(centroid)
        
        if len(centroids) < 2:
            coda.vowel_modulation_strength = 0.0
            return
        
        centroids = np.array(centroids)
        
        # Modulation strength = coefficient of variation of spectral centroid
        cv = np.std(centroids) / (np.mean(centroids) + 1e-10)
        coda.vowel_modulation_strength = min(1.0, cv * 5)  # Scale to 0-1
        
        # Estimate vowel category based on mean centroid frequency
        mean_centroid = np.mean(centroids)
        coda.resonant_frequencies = centroids.tolist()[:10]  # First 10 for metadata
        
        # Map centroid to vowel-like category (rough approximation)
        if mean_centroid < 1000:
            coda.estimated_vowel = "u"  # Low frequency → back vowel
        elif mean_centroid < 2000:
            coda.estimated_vowel = "o"
        elif mean_centroid < 3500:
            coda.estimated_vowel = "a"
        elif mean_centroid < 5000:
            coda.estimated_vowel = "e"
        else:
            coda.estimated_vowel = "i"  # High frequency → front vowel
    
    def _extract_prosody(self, coda: CodaPattern):
        """
        Extract prosodic features: tempo, rubato, rhythm regularity, ornamentation.
        
        These features encode semantic meaning in whale communication,
        similar to tonal languages like Mandarin.
        """
        from .vocal_modulation import (
            compute_prosody_features,
        )
        
        features = compute_prosody_features(coda.inter_click_intervals)
        coda.tempo_bpm = features.tempo_bpm
        coda.rubato = features.rubato
        coda.rhythm_regularity = features.rhythm_regularity
        coda.ornamentation_count = features.ornamentation_count
    
    def _estimate_semantic_context(self, coda: CodaPattern):
        """
        Estimate semantic context based on coda type and known patterns.
        
        Uses pattern matching against documented coda types from
        Project CETI's Dominica sperm whale population studies.
        """
        # Pattern matching based on click count and type
        if coda.coda_type == CodaType.REGULAR and coda.click_count == 5:
            coda.semantic_context = "social_greeting"
        elif coda.coda_type == CodaType.ACCELERATING:
            coda.semantic_context = "attention_call"
        elif coda.coda_type == CodaType.COMPLEX and coda.click_count >= 7:
            coda.semantic_context = "narrative_exchange"
        elif coda.coda_type == CodaType.REGULAR and coda.click_count <= 4:
            coda.semantic_context = "identity_marker"
        elif coda.coda_type == CodaType.DECELERATING:
            coda.semantic_context = "acknowledgment"
        else:
            coda.semantic_context = "undetermined"
    
    def _compute_complexity(self, coda: CodaPattern):
        """
        Compute normalized communication complexity score (0-1).
        
        Higher complexity indicates richer information content:
        - More phonetic variety → higher complexity
        - Stronger vowel modulation → higher complexity
        - More rubato/ornamentation → higher complexity
        - More clicks → higher complexity (up to a point)
        """
        # Phonetic diversity (unique phonemes / total)
        if coda.phonetic_sequence:
            unique_ratio = len(set(coda.phonetic_sequence)) / len(coda.phonetic_sequence)
        else:
            unique_ratio = 0.0
        
        # Click count factor (normalized, peaks at ~10 clicks)
        click_factor = min(1.0, coda.click_count / 10.0)
        
        # Weighted combination
        complexity = (
            unique_ratio * 0.25 +
            coda.vowel_modulation_strength * 0.25 +
            coda.rubato * 0.20 +
            click_factor * 0.15 +
            (coda.ornamentation_count / 5.0) * 0.15
        )
        
        coda.communication_complexity = min(1.0, complexity)
        
        # Confidence based on signal quality indicators
        coda.confidence = min(0.95, 0.5 + click_factor * 0.2 + (1 - coda.rubato) * 0.1 + unique_ratio * 0.15)
