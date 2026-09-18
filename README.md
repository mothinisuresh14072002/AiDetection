# AiDetection

**Open-source multimodal AI media detection toolkit** for images, audio, and video.

> Detection is probabilistic. A detector score is not proof of authorship or provenance.

## Vision
AiDetection provides one interface for analyzing multiple media types, with pluggable detectors, confidence-aware results, explainability, reproducible evaluation, and a web/API layer.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn api.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

## Detector policy
The repository starts with a deterministic baseline adapter so the project is runnable without downloading large model weights. Production model adapters should be benchmarked, calibrated, and reported separately for each modality and dataset.

## Contributing
See CONTRIBUTING.md. Please include tests for behavioral changes.

## License
Apache-2.0
