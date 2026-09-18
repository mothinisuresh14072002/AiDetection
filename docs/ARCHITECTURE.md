# Architecture

```
Browser / SDK
     |
 FastAPI
     |
DetectionService
     |
 modality-aware pipeline
  /    |    \
image audio video
     |
signals + provenance
     |
calibrated scoring
     |
structured result
```

Model adapters are intentionally isolated from the API. This makes it possible to benchmark multiple models and ensemble them without changing clients.
