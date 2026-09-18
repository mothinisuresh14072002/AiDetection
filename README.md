# AiDetection

**Open-source multimodal AI-media detection toolkit for images, audio, and video.**

One API, optional local Hugging Face inference, provenance signals, conservative scoring, browser UI, Docker support, and evaluation-first design.

> AI-media detection is probabilistic. A detector score is not proof of authorship, identity, intent, or provenance.

## Quick start

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    uvicorn api.main:app --reload

Open http://127.0.0.1:8000 for the web UI or /docs for Swagger.

## Enable local model inference

    pip install -e ".[models]"
    export AIDETECTION_ENABLE_MODELS=1
    uvicorn api.main:app --host 0.0.0.0 --port 8000

Models are downloaded on first use and are not committed to the repository. Configure model IDs with AIDETECTION_IMAGE_MODEL and AIDETECTION_AUDIO_MODEL.

Video samples frames and applies the image detector as a bridge; this is not equivalent to a dedicated temporal video detector.

## API

    curl -X POST http://127.0.0.1:8000/v1/analyze -F "file=@sample.jpg"

The response contains modality, label, confidence, and evidence signals.

## Evaluation

Benchmark on held-out real media and multiple synthetic-generator families. Track precision, recall, F1, ROC-AUC, PR-AUC, calibration, false positives, compression robustness, and generator-specific performance.

## Roadmap

Dedicated image ensembles, temporal video models, multilingual audio ensembles, C2PA verification, background jobs, benchmark runner, calibration, model cards, and production hardening.

## License

Apache-2.0.
