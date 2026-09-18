# Model setup

The repository does not commit model weights.

## Image

Default:
Reju983/ai-generated-image-detector

Override:
AIDETECTION_IMAGE_MODEL=your-org/your-image-model

## Audio

Default:
garystafford/wav2vec2-deepfake-voice-detector

Override:
AIDETECTION_AUDIO_MODEL=your-org/your-audio-model

## Enable

    pip install -e ".[models]"
    export AIDETECTION_ENABLE_MODELS=1

Models are downloaded lazily. Review each model card, license, training data, and limitations before deployment. Do not treat reported benchmark numbers from a model card as performance of AiDetection itself.

## Video

The current bridge samples up to 12 frames and aggregates image-detector probabilities. A dedicated temporal model should replace this for production video detection.
