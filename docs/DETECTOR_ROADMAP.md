# Detector roadmap

AiDetection separates the API contract from model implementations so detectors can evolve without breaking clients.

## Image
Planned adapters: frequency-domain artifacts, compression consistency, metadata/provenance inspection, and trained vision classifiers.

## Audio
Planned adapters: spectrogram classifiers, codec/resampling analysis, phase/voice consistency signals, and provenance checks.

## Video
Planned adapters: temporal consistency, frame-level image detection, audio-video synchronization, face/reenactment signals, and provenance checks.

## Evaluation
Every production detector should report:
- precision, recall, F1, ROC-AUC and PR-AUC
- calibration/error analysis
- performance by generator family and compression level
- false-positive analysis on real media
- dataset licensing and train/test separation

No detector should be described as universally accurate. Scores must include model/version and evaluation context.
