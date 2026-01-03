#!/usr/bin/env python3
"""
Doolittle Open Source Scaffolding Script

Creates the complete monorepo structure for the Doolittle project.
Run with: python scaffold_doolittle.py
"""

import os
import textwrap

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).strip() + "\n")
    print(f"✅ Created: {path}")

def scaffold():
    root = "."

    # 1. ROOT DOCUMENTATION
    # ==========================================
    create_file(f"{root}/README.md", """
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
    """)

    create_file(f"{root}/MANIFESTO.md", """
    # The Doolittle Manifesto

    > "Understanding begins with listening."

    We are a community of computer scientists, veterinarians, ethologists, and pet owners
    working together to decode the languages of the animal kingdom.

    ## Our Core Beliefs

    ### 1. Animals Have Rich Inner Lives
    They experience pain, joy, fear, and comfort. They are not automata. Our technology
    must honor their sentience and serve their welfare.

    ### 2. Communication is a Spectrum
    Animals speak through micro-expressions, vocalizations, posture, and behavior.
    Understanding requires multimodal observation - the eyes, ears, and context together.

    ### 3. Science Belongs to the Commons
    Our research, data, and models are open. We reject the enclosure of knowledge that
    could alleviate suffering. Proprietary pain detection is an oxymoron.

    ### 4. Welfare First, Always
    We build to reduce suffering, never to exploit. Our tools are designed to help
    caregivers understand their companions, not to surveil or control them.

    ### 5. Humility in Interpretation
    We do not claim to "speak" for animals. We build tools that help humans listen
    better. Translation is approximation; we communicate our uncertainty.

    ## Our Commitments

    - **Open Data**: All training datasets published with clear provenance
    - **Reproducible Research**: Full code and methodology transparency
    - **Veterinary Partnership**: Clinical validation before deployment
    - **Species Respect**: No invasive data collection methods
    - **Privacy Protection**: Pet owner data is never sold or shared

    ## The Vision

    We imagine a future where:
    - A smartphone can help detect early signs of pain in pets
    - Veterinarians have AI assistants trained on validated pain scales
    - Shelter animals can be assessed quickly and accurately
    - Researchers worldwide collaborate on open datasets
    - The bond between humans and animals deepens through understanding

    ## Join Us

    Whether you're a developer, veterinarian, data scientist, or simply someone who
    loves animals - there's a place for you in the Doolittle Collective.

    Together, we listen. Together, we understand.

    ---

    *"The greatness of a nation can be judged by the way its animals are treated."*
    *— Mahatma Gandhi*
    """)

    create_file(f"{root}/CONTRIBUTING.md", """
    # Contributing to Doolittle

    Thank you for your interest in contributing to the Doolittle project!
    We welcome contributions of all kinds.

    ## Ways to Contribute

    ### Code Contributions
    1. Fork the repository
    2. Create a feature branch (`git checkout -b feature/amazing-feature`)
    3. Make your changes
    4. Run tests (`poetry run pytest`)
    5. Commit with clear messages
    6. Push and open a Pull Request

    ### Data Contributions
    We accept labeled datasets for:
    - Feline Grimace Scale annotations
    - Cat/dog vocalization clips with emotion labels
    - Pain assessment videos with veterinary validation

    Please see `datasets/CONTRIBUTING.md` for data submission guidelines.

    ### Documentation
    - Improve existing docs
    - Add tutorials and examples
    - Translate to other languages

    ## Code Style

    - Python: Follow PEP 8, use type hints
    - Tests: pytest, aim for >80% coverage
    - Docs: Google-style docstrings

    ## Animal Welfare Standards

    All contributions must adhere to our welfare principles:
    - No data from invasive procedures
    - Clear consent from pet owners
    - No content that could enable animal harm

    ## Review Process

    1. All PRs require review from a maintainer
    2. Clinical features require veterinary sign-off
    3. Data contributions require provenance documentation

    ## Questions?

    Open a Discussion or reach out to the maintainers.
    """)

    create_file(f"{root}/LICENSE", """
    Apache License
    Version 2.0, January 2004
    http://www.apache.org/licenses/

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    """)

    # 2. ROOT PYPROJECT.TOML (Workspace)
    # ==========================================
    create_file(f"{root}/pyproject.toml", """
    [tool.poetry]
    name = "doolittle"
    version = "0.1.0"
    description = "Open-source primitives for AI-assisted interspecies communication"
    authors = ["Doolittle Collective <hello@doolittle.org>"]
    license = "Apache-2.0"
    readme = "README.md"

    [tool.poetry.dependencies]
    python = "^3.10"
    numpy = "^1.24"
    pydantic = "^2.0"
    scipy = "^1.11"

    [tool.poetry.group.dev.dependencies]
    pytest = "^7.4"
    pytest-cov = "^4.1"
    black = "^23.0"
    ruff = "^0.1"
    mypy = "^1.6"

    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"

    [tool.pytest.ini_options]
    testpaths = ["packages"]
    python_files = "test_*.py"

    [tool.black]
    line-length = 100
    target-version = ["py310"]

    [tool.ruff]
    line-length = 100
    select = ["E", "F", "I", "N", "W"]
    """)

    # 3. PACKAGES (The Modules)
    # ==========================================

    packages = {
        "doolittle-core": "Shared types, schemas (BioSignal), and species configurations",
        "aivet-vision": "The Eyes - Grimace detection, optical flow, gait analysis",
        "aivet-listen": "The Ears - Vocal analysis, spectral classification",
        "aivet-dolittle": "The Translator - Signal to symptom mapping",
        "aivet-core": "The Brain - Bayesian fusion and triage engine",
        "aivet-connect": "The Bridge - API connectors and integrations",
    }

    for pkg, desc in packages.items():
        # Create pyproject.toml for each package
        create_file(f"{root}/packages/{pkg}/pyproject.toml", f"""
        [tool.poetry]
        name = "{pkg}"
        version = "0.1.0"
        description = "{desc}"
        authors = ["Doolittle Collective <hello@doolittle.org>"]
        license = "Apache-2.0"

        [tool.poetry.dependencies]
        python = "^3.10"
        numpy = "^1.24"
        pydantic = "^2.0"
        """)

        # Create source init
        create_file(f"{root}/packages/{pkg}/src/__init__.py", f'''"""
{desc}

Part of the Doolittle open-source collective.
"""

__version__ = "0.1.0"
''')

    # 4. PACKAGE SPECIFIC FILES (The Primitives)
    # ==========================================

    # doolittle-core: Schemas
    create_file(f"{root}/packages/doolittle-core/src/schema.py", """
    \"\"\"
    Core schemas for the Doolittle ecosystem.

    These types are shared across all packages to ensure consistent
    data structures throughout the pipeline.
    \"\"\"

    from enum import Enum
    from typing import Dict, List, Optional, Any
    from pydantic import BaseModel, Field
    from datetime import datetime

    class Species(str, Enum):
        \"\"\"Supported species for analysis.\"\"\"
        CAT = "cat"
        DOG = "dog"
        RABBIT = "rabbit"
        HORSE = "horse"
        BIRD = "bird"
        UNKNOWN = "unknown"

    class SignalSource(str, Enum):
        \"\"\"Source of a biological signal.\"\"\"
        VISION_GRIMACE = "vision_grimace"
        VISION_VITALS = "vision_vitals"
        VISION_POSE = "vision_pose"
        AUDIO_VOCAL = "audio_vocal"
        AUDIO_BREATHING = "audio_breathing"

    class SignalModality(str, Enum):
        \"\"\"Modality of the signal.\"\"\"
        VISUAL = "visual"
        AUDIO = "audio"
        MULTIMODAL = "multimodal"

    class BioSignal(BaseModel):
        \"\"\"
        Universal biological signal container.

        All primitives emit BioSignals that can be fused by the triage engine.
        \"\"\"
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
        \"\"\"Pain assessment result from any primitive or fusion.\"\"\"
        pain_probability: float = Field(ge=0.0, le=1.0)
        confidence: float = Field(ge=0.0, le=1.0)
        sources: List[SignalSource]
        modality: SignalModality
        timestamp: float

    class TriageLevel(str, Enum):
        \"\"\"Clinical triage urgency levels.\"\"\"
        ROUTINE = "routine"
        LOW = "low"
        MODERATE = "moderate"
        URGENT = "urgent"
        EMERGENCY = "emergency"
    """)

    create_file(f"{root}/packages/doolittle-core/src/species.py", """
    \"\"\"
    Species-specific configurations and parameters.
    \"\"\"

    from dataclasses import dataclass
    from typing import Dict, Tuple

    @dataclass
    class SpeciesConfig:
        \"\"\"Configuration for a specific species.\"\"\"
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
        \"\"\"Get configuration for a species, with fallback defaults.\"\"\"
        return SPECIES_CONFIGS.get(species.lower(), SpeciesConfig(
            name=species,
            pain_hiding_factor=0.5,
            vocal_freq_range=(50, 8000),
            grimace_supported=False,
            gcps_supported=False,
            typical_resting_rr=(15, 40),
            typical_resting_hr=(60, 180),
        ))
    """)

    # aivet-vision: Structure
    create_file(f"{root}/packages/aivet-vision/src/grimace/__init__.py", '''"""
Grimace Scale implementations for pain detection.

Supported scales:
- Feline Grimace Scale (FGS) - cats
- Rabbit Grimace Scale (RGS) - rabbits
- Glasgow Composite Pain Scale (GCPS) - dogs (partial)
"""
''')

    create_file(f"{root}/packages/aivet-vision/src/vitals/__init__.py", '''"""
Non-contact vital sign estimation.

Uses optical flow and color analysis to detect:
- Respiration rate
- Heart rate (via photoplethysmography)
- Movement patterns
"""
''')

    # aivet-listen: Structure
    create_file(f"{root}/packages/aivet-listen/src/vocalization/__init__.py", '''"""
Vocalization analysis for emotional and pain assessment.

Analyzes:
- Spectral features (pitch, jitter, shimmer, HNR)
- Vocal type classification (meow, growl, purr, etc.)
- Emotional valence (positive, negative, neutral)
- Pain probability estimation
"""
''')

    # aivet-core: The Pipeline
    create_file(f"{root}/packages/aivet-core/src/pipeline.py", """
    \"\"\"
    The main AiVet pipeline orchestrator.

    Coordinates vision, audio, and fusion primitives to produce
    unified triage assessments.
    \"\"\"

    from typing import Optional, Dict, Any
    from dataclasses import dataclass
    import numpy as np

    @dataclass
    class PipelineContext:
        \"\"\"Shared context for a triage session.\"\"\"
        session_id: str
        species: str
        patient_id: Optional[str] = None
        metadata: Dict[str, Any] = None

    class AiVetPipeline:
        \"\"\"
        Main orchestrator for the AiVet system.

        Coordinates:
        - Vision primitives (grimace, vitals)
        - Audio primitives (vocalization)
        - Fusion engine (Bayesian combination)
        - Output formatting
        \"\"\"

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
        ) -> Dict[str, Any]:
            \"\"\"
            Process a single frame (image + optional audio).

            Returns a triage assessment.
            \"\"\"
            results = {}

            # Run vision if image provided
            if image is not None:
                results["vision"] = self._process_vision(image)

            # Run audio if audio provided
            if audio is not None:
                results["audio"] = self._process_audio(audio)

            # Fuse if we have any signals
            if results:
                results["triage"] = self._fuse_signals(results)

            return results

        def _process_vision(self, image: np.ndarray) -> Dict[str, Any]:
            \"\"\"Process visual input.\"\"\"
            # Placeholder - actual implementation in aivet-vision
            return {"status": "not_implemented"}

        def _process_audio(self, audio: np.ndarray) -> Dict[str, Any]:
            \"\"\"Process audio input.\"\"\"
            # Placeholder - actual implementation in aivet-listen
            return {"status": "not_implemented"}

        def _fuse_signals(self, signals: Dict[str, Any]) -> Dict[str, Any]:
            \"\"\"Fuse all signals into unified assessment.\"\"\"
            # Placeholder - actual implementation in aivet-core/fusion
            return {"status": "not_implemented"}
    """)

    create_file(f"{root}/packages/aivet-core/src/demo.py", """
    \"\"\"
    Demo script showing basic Doolittle usage.
    \"\"\"

    import numpy as np
    from pipeline import AiVetPipeline, PipelineContext

    def main():
        print("🐾 Doolittle Demo")
        print("=" * 40)

        # Create a session context
        context = PipelineContext(
            session_id="demo-001",
            species="cat",
            patient_id="whiskers",
        )

        # Initialize pipeline
        pipeline = AiVetPipeline(context)

        # Simulate a frame (in production, this would be real video/audio)
        mock_image = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_audio = np.random.randn(16000).astype(np.float32) * 0.1

        # Process
        result = pipeline.process_frame(image=mock_image, audio=mock_audio)

        print(f"\\nSession: {context.session_id}")
        print(f"Species: {context.species}")
        print(f"Patient: {context.patient_id}")
        print(f"\\nResult: {result}")

        print("\\n✅ Demo complete!")
        print("\\nNote: This is a scaffold. Implement the primitives in:")
        print("  - packages/aivet-vision/src/grimace/")
        print("  - packages/aivet-listen/src/vocalization/")
        print("  - packages/aivet-core/src/fusion/")

    if __name__ == "__main__":
        main()
    """)

    # 5. DATASETS & RESEARCH
    # ==========================================
    create_file(f"{root}/datasets/README.md", """
    # Doolittle Open Data Commons

    This directory contains schemas and documentation for our open datasets.

    ## Hosted Datasets

    Our labeled datasets are hosted on Hugging Face:
    - `doolittle/feline-grimace-scale` - FGS annotated images
    - `doolittle/cat-vocalizations` - Labeled cat audio clips
    - `doolittle/multimodal-pain` - Combined video+audio pain assessments

    ## Contributing Data

    See [CONTRIBUTING.md](CONTRIBUTING.md) for data submission guidelines.

    ## Data Schema

    All datasets follow standardized schemas defined in `schemas/`.
    """)

    create_file(f"{root}/datasets/CONTRIBUTING.md", """
    # Contributing Data to Doolittle

    Thank you for contributing to open veterinary science!

    ## Requirements

    ### Consent
    - Written consent from pet owner required
    - No identifiable human information

    ### Quality
    - Minimum resolution: 720p for video, 16kHz for audio
    - Clear view of subject
    - Labeled by qualified annotator (vet or trained volunteer)

    ### Format
    - Images: JPEG or PNG
    - Video: MP4 (H.264)
    - Audio: WAV or FLAC
    - Annotations: JSON following our schema

    ## Submission Process

    1. Fork the dataset repository on Hugging Face
    2. Add your data with annotations
    3. Include provenance document
    4. Open a Pull Request

    ## Annotation Guidelines

    See `schemas/annotation_guide.md` for detailed labeling instructions.
    """)

    create_file(f"{root}/datasets/grimace/metadata.json", """{
      "name": "feline-grimace-scale",
      "version": "0.1.0",
      "description": "Feline Grimace Scale annotated images for pain detection",
      "license": "CC-BY-4.0",
      "species": ["cat"],
      "labels": ["FGS_score", "action_units", "pain_detected"],
      "splits": ["train", "validation", "test"],
      "source": "Doolittle Open Data Commons"
    }""")

    create_file(f"{root}/research/papers/README.md", """
    # Community Publications

    Research papers and findings from the Doolittle community.

    ## Key References

    ### Feline Grimace Scale
    - Evangelista et al. (2019) - Original FGS validation
    - Development and validation study

    ### Pain Detection
    - Various community contributions

    ## Submitting Research

    Open a PR to add your publication to this directory.
    """)

    # 6. APPS (Placeholders)
    # ==========================================
    create_file(f"{root}/apps/petsorcery-web/package.json", """{
      "name": "petsorcery-web",
      "version": "0.1.0",
      "description": "Consumer web app for pet wellness monitoring",
      "private": true,
      "scripts": {
        "dev": "next dev",
        "build": "next build"
      }
    }""")

    create_file(f"{root}/apps/petsorcery-web/README.md", """
    # PetSorcery Web

    Consumer-facing web application for pet wellness monitoring.

    ## Features
    - Upload video for pain assessment
    - Real-time camera monitoring
    - Wellness tracking over time

    ## Getting Started

    ```bash
    npm install
    npm run dev
    ```
    """)

    create_file(f"{root}/apps/vetsorcery-integration/README.md", """
    # VetSorcery PIMS Connector

    Integration layer connecting Doolittle to professional Practice Information Management Systems.

    ## Supported Systems
    - VetSorcery (native)
    - ezyVet (planned)
    - Cornerstone (planned)

    ## API Documentation

    See `docs/api.md` for integration details.
    """)

    # 7. CI/CD
    # ==========================================
    create_file(f"{root}/.github/workflows/test.yml", """
    name: Test

    on:
      push:
        branches: [main, develop]
      pull_request:
        branches: [main]

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: ["3.10", "3.11", "3.12"]

        steps:
          - uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: ${{ matrix.python-version }}

          - name: Install Poetry
            run: pip install poetry

          - name: Install dependencies
            run: poetry install

          - name: Run tests
            run: poetry run pytest --cov

          - name: Lint
            run: poetry run ruff check .
    """)

    create_file(f"{root}/.gitignore", """
    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    .Python
    build/
    dist/
    *.egg-info/
    .eggs/

    # Virtual environments
    .venv/
    venv/
    ENV/

    # IDE
    .idea/
    .vscode/
    *.swp
    *.swo

    # Testing
    .pytest_cache/
    .coverage
    htmlcov/

    # OS
    .DS_Store
    Thumbs.db

    # Poetry
    poetry.lock

    # Local config
    .env
    .env.local
    """)

    print("\n" + "=" * 50)
    print("🎉 Doolittle Repository Scaffolding Complete!")
    print("=" * 50)
    print(f"\n📂 Location: {os.path.abspath(root)}")
    print("\n📋 Next Steps:")
    print("   1. cd doolittle-oss")
    print("   2. git init && git add . && git commit -m 'feat: Initial Doolittle architecture'")
    print("   3. poetry install")
    print("   4. python packages/aivet-core/src/demo.py")
    print("\n🌍 Ready to build the future of interspecies communication!")

if __name__ == "__main__":
    scaffold()
