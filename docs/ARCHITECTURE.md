# Architecture

AiDetection separates upload handling, media classification, detector inference, scoring, and presentation.

## Request flow

1. FastAPI accepts a bounded multipart upload.
2. The service resolves the media modality.
3. The pipeline records lightweight provenance markers and selects the configured detector path.
4. Image and audio detectors are optional adapters; video samples frames through the image adapter.
5. The scoring layer converts detector probability into a conservative label.
6. The API returns the label, evidence signals, SHA-256 digest, and processing time.

## Design principles

- Uploaded media is untrusted and is not persisted by the API.
- Heavy ML dependencies are opt-in.
- Metadata and model outputs are signals, not proof.
- Detector implementations remain replaceable.
- Accuracy claims require measured held-out evaluation.

| Modality | Current path | Next step |
| --- | --- | --- |
| Image | Optional image classifier | Artifact/frequency features and calibration |
| Audio | Optional audio classifier | Waveform/spectrogram features and codec robustness |
| Video | Frame sampling + image classifier | Temporal consistency and A/V synchronization |
