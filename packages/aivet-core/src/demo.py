"""
Demo script showing basic Doolittle usage.
"""

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

    print(f"\nSession: {context.session_id}")
    print(f"Species: {context.species}")
    print(f"Patient: {context.patient_id}")
    print(f"\nResult: {result}")

    print("\n✅ Demo complete!")
    print("\nNote: This is a scaffold. Implement the primitives in:")
    print("  - packages/aivet-vision/src/grimace/")
    print("  - packages/aivet-listen/src/vocalization/")
    print("  - packages/aivet-core/src/fusion/")

if __name__ == "__main__":
    main()
