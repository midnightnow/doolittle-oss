# 🌍 Doolittle

**Decoding Interspecies Communication through Open Science.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Status-Alpha-orange)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()

Doolittle is an open-source collective building the primitives for AI-assisted interspecies communication.
It powers the **PetSorcery** (Consumer) and **VetSorcery** (Professional) ecosystems.

## 🎯 Mission

> "Understanding begins with listening."

We're building the scientific foundation for decoding animal communication through:
- **Pain Detection**: Feline Grimace Scale (FGS), Glasgow Composite Pain Scale
- **Vocalization Analysis**: Spectral classification of distress, content, and social calls
- **Multimodal Fusion**: Bayesian integration of visual + audio signals
- **Species Translation**: Converting animal signals into human-understandable assessments

## 🏗 The Monorepo

| Package | Description |
|---------|-------------|
| `doolittle-core` | Shared schemas (`BioSignal`), species enums, and base types. |
| `aivet-vision` | **The Eyes**. Optical flow respiration, grimace scales (FGS/GCPS), gait analysis. |
| `aivet-listen` | **The Ears**. Vocal sentiment analysis, spectral feature extraction. |
| `aivet-dolittle` | **The Translator**. Logic layer that converts signals into clinical symptoms. |
| `aivet-core` | **The Brain**. Bayesian fusion engine and triage protocols. |
| `aivet-connect` | **The Bridge**. WebRTC, PIMS integration, and API connectors. |

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/doolittle-collective/doolittle.git
cd doolittle

# Install dependencies (using Poetry)
poetry install

# Run the demo triage loop
python packages/aivet-core/src/demo.py
```

## 📊 Quick Example

```python
from doolittle import DolittleBridge, OutputFormat

# Initialize the bridge for a cat
bridge = DolittleBridge(species="cat")

# Start a monitoring session
bridge.start_session(session_id="whiskers-001", species="cat")

# Run triage on video frame + audio clip
result = bridge.run_triage(
    image=video_frame,
    audio=audio_clip,
    output_format=OutputFormat.CLINICAL
)

print(f"Pain Probability: {result['pain_probability']:.1%}")
print(f"Triage Level: {result['triage_level']}")
print(f"Pet Says: {result['pet_message']}")
```

## 🔬 The Science

### Feline Grimace Scale (FGS)
- 5 Action Units: Ear position, Orbital tightening, Muzzle tension, Whisker change, Head position
- Pain threshold: Normalized score ≥ 0.39
- Validated in peer-reviewed literature

### Vocal Analysis
- Spectral features: Pitch, Jitter, Shimmer, HNR
- Pain signature: High jitter (>3%) + elevated pitch (>800Hz)
- Species-specific frequency ranges

### Multimodal Fusion
- Bayesian confidence weighting
- Agreement bonus for correlated signals
- Species-specific pain hiding factors

## 🤝 Contributing

We welcome contributions of code, labeled data, and veterinary expertise.
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- **Code**: Improve detection algorithms, add new species support
- **Data**: Contribute labeled video/audio datasets (Hugging Face)
- **Expertise**: Veterinary validation, ethological review
- **Documentation**: Tutorials, translations, use cases

## 📜 License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Dr. Marina Evangelista (FGS validation research)
- The veterinary community for domain expertise
- Open source contributors worldwide

---

*Built with ❤️ by the Doolittle Collective*
