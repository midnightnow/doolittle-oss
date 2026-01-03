"""
Species-specific configurations and parameters.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class SpeciesConfig:
    """Configuration for a specific species."""
    name: str
    pain_hiding_factor: float  # 0-1, higher = hides pain more
    vocal_freq_range: Tuple[float, float]  # Hz
    grimace_supported: bool
    gcps_supported: bool  # Glasgow Composite Pain Scale
    typical_resting_rr: Tuple[int, int]  # Respiration rate range
    typical_resting_hr: Tuple[int, int]  # Heart rate range

SPECIES_CONFIGS: Dict[str, SpeciesConfig] = {
    "cat": SpeciesConfig(
        name="Felis catus",
        pain_hiding_factor=0.6,
        vocal_freq_range=(50, 10000),
        grimace_supported=True,
        gcps_supported=False,
        typical_resting_rr=(20, 30),
        typical_resting_hr=(120, 140),
    ),
    "dog": SpeciesConfig(
        name="Canis familiaris",
        pain_hiding_factor=0.2,
        vocal_freq_range=(40, 8000),
        grimace_supported=False,
        gcps_supported=True,
        typical_resting_rr=(10, 30),
        typical_resting_hr=(60, 140),
    ),
    "rabbit": SpeciesConfig(
        name="Oryctolagus cuniculus",
        pain_hiding_factor=0.8,
        vocal_freq_range=(100, 16000),
        grimace_supported=True,
        gcps_supported=False,
        typical_resting_rr=(30, 60),
        typical_resting_hr=(130, 325),
    ),
}

def get_species_config(species: str) -> SpeciesConfig:
    """Get configuration for a species, with fallback defaults."""
    return SPECIES_CONFIGS.get(species.lower(), SpeciesConfig(
        name=species,
        pain_hiding_factor=0.5,
        vocal_freq_range=(50, 8000),
        grimace_supported=False,
        gcps_supported=False,
        typical_resting_rr=(15, 40),
        typical_resting_hr=(60, 180),
    ))
