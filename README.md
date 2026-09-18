# AiDetection

**Open-source multimodal AI-media detection toolkit for images, audio, and video.**

One API, optional local Hugging Face inference, provenance signals, conservative scoring, browser UI, Docker support, and evaluation-first design.

> AI-media detection is probabilistic. A detector score is not proof of authorship, identity, intent, or provenance.

## Quick start

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    uvicorn api.main:app --reload

Open http://127.0.0.1:8000 for the browser UI or /docs for Swagger.

## Detection models

The repository keeps model weights out of Git. The current optional defaults are Apache-2.0 Hugging Face models: an image detector from Reju983 based on Community Forensics, and a Wav2Vec2 audio deepfake detector from garystafford. Review each model card, training data, and license before production use.

The project does not claim a universal accuracy number: detector performance depends on generators, compression, preprocessing, and the evaluation set.

## Enable local model inference

    pip install -e ".[models]"
    export AIDETECTION_ENABLE_MODELS=1
    uvicorn api.main:app --host 0.0.0.0 --port 8000

Models are downloaded on first use and are not committed to the repository. Configure model IDs with AIDETECTION_IMAGE_MODEL and AIDETECTION_AUDIO_MODEL.

Video samples frames and applies the image detector as a bridge; this is not equivalent to a dedicated temporal video detector.

## API

    curl -X POST http://127.0.0.1:8000/v1/analyze -F "file=@sample.jpg"

The response contains modality, label, confidence, evidence signals, SHA-256, and processing time.

## Safety

Uploaded media is treated as untrusted input. The default request limit is 25 MiB. Production deployments should add authentication, rate limiting, sandboxed media decoding, malware scanning, timeouts, encryption, and automatic deletion.

## Evaluation

Benchmark on held-out real media and multiple synthetic-generator families. Track precision, recall, F1, ROC-AUC, PR-AUC, calibration, false positives, compression robustness, and generator-specific performance.

## License

Apache-2.0.
