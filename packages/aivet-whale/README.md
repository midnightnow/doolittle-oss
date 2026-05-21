# aivet-whale — Sperm Whale Communication Primitive

> "Understanding begins with listening." — The Doolittle Manifesto

Implements the **Project CETI / WhAM** research breakthroughs (2024–2026) as a Doolittle primitive for AI-assisted interspecies communication analysis.

## What It Does

Analyzes sperm whale click sequences (codas) and extracts:

| Feature | Method | Reference |
|---------|--------|-----------|
| **Phonetic alphabet** | Spectral classification into 11 categories | Sharma et al. 2024 |
| **Vowel modulation** | Spectral centroid tracking (e-coda / i-coda) | Project CETI 2025 |
| **Coarticulation** | Sequential formant shift detection | Project CETI 2026 |
| **Tonal contours** | Rising/falling ICI patterns (Mandarin-like) | Project CETI 2026 |
| **Prosody** | Tempo, rubato, rhythm regularity, ornamentation | Gero et al. 2016 |
| **Welfare assessment** | Communication pattern → triage level mapping | Novel |

## Quick Start

```python
import numpy as np
from aivet_whale import CetaceanAnalyzer, coda_to_biosignal

# Initialize analyzer
analyzer = CetaceanAnalyzer(species="sperm_whale")

# Load audio (mono, float32, 44.1kHz)
audio = np.fromfile("hydrophone_recording.raw", dtype=np.float32)

# Analyze
codas = analyzer.analyze_audio(audio, sample_rate=44100)

for coda in codas:
    print(f"Type: {coda.coda_type.value}")
    print(f"Phonetics: {' '.join(coda.phonetic_sequence)}")
    print(f"Vowel: {coda.estimated_vowel} (strength={coda.vowel_modulation_strength:.2f})")
    print(f"Tempo: {coda.tempo_bpm:.0f} BPM, Rubato: {coda.rubato:.2f}")
    print(f"Semantic: {coda.semantic_context}")
    print(f"Complexity: {coda.communication_complexity:.2f}")
    print()

# Convert to Doolittle BioSignal for fusion
from aivet_whale import coda_to_biosignal
signal = coda_to_biosignal(codas[0], patient_id="whale_dominica_042")
print(f"Triage: {signal['triage_level']}")
```

## Installation

```bash
pip install -e .          # basic (numpy only)
pip install -e ".[audio]" # with librosa for advanced spectral analysis
pip install -e ".[dev]"   # with pytest for development
```

## Architecture

```
Hydrophone Audio
       │
       ▼
┌─────────────────┐
│  Coda Detector  │  Energy-based click segmentation
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬─────────────┐
    ▼         ▼              ▼             ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│Phonetic│ │  Vowel   │ │ Prosody  │ │  Tonal   │
│Alphabet│ │Modulation│ │ Analysis │ │ Contour  │
└────┬───┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
     │          │             │             │
     └──────────┴──────┬──────┴─────────────┘
                       ▼
              ┌────────────────┐
              │ CodaPattern    │  Unified analysis result
              │ + BioSignal    │  → Doolittle fusion engine
              └────────────────┘
```

## Key Concepts

### Phonetic Classes (11 categories)

| Symbol | Category | Description |
|--------|----------|-------------|
| `k` | Plosive | Sharp high-frequency click |
| `t` | Plosive | Mid-frequency plosive |
| `p` | Plosive | Low-frequency plosive |
| `s` | Fricative | High-frequency buzzy |
| `f` | Fricative | Mid-frequency noisy |
| `a~` | Resonant | Open vowel-like (low centroid) |
| `e~` | Resonant | Mid vowel-like |
| `i~` | Resonant | Close vowel-like (high centroid) |
| `?` | Glottal | Creaky pulse train |
| `m~` | Nasal | Low-frequency hum |
| `K*` | Compound | Click with ornamentation |

### Semantic Context (from coda patterns)

| Pattern | Meaning |
|---------|---------|
| Regular 5-click | Social greeting |
| Short regular (≤4) | Identity marker (clan) |
| Accelerating | Attention call |
| Complex 7+ clicks | Narrative exchange |
| Decelerating | Acknowledgment |

### Welfare Assessment

| Indicator | Triage Level |
|-----------|-------------|
| Normal social communication | `normal` |
| Reduced complexity | `low` |
| High rubato + acceleration | `moderate` |
| Very high ornamentation + short codas | `urgent` |

## Research Citations

- **Project CETI** — Cetacean Translation Initiative (2024–2026)
- **Sharma et al. 2024** — "Contextual and combinatorial structure in sperm whale vocalisations"
- **Gero et al. 2016** — "Individual, unit and vocal clan level identity cues in sperm whale codas"
- **Evangelista et al. 2019** — Feline Grimace Scale (methodology adapted for cetacean welfare)
- **WhAM** — Whale Animal Model (Project CETI's predictive transformer)

## Future Work

- [ ] Train 156-class phonetic classifier on Project CETI's 9000+ labelled codas
- [ ] Integrate WhAM transformer model when publicly released
- [ ] Upgrade to LPC-based formant extraction for e-coda / i-coda
- [ ] Add real-time hydrophone streaming via `aivet-connect`
- [ ] Extend to humpback whale song analysis
- [ ] Validate with marine biologists (Dominica population)

## License

MIT — See the [Doolittle Manifesto](../../MANIFESTO.md) for our ethical commitments.
