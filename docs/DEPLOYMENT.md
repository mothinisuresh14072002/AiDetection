# Deployment

## Docker

    docker compose up --build

Then open http://localhost:8000.

## Model-enabled deployment

Install the models extra and set AIDETECTION_ENABLE_MODELS=1. For GPU deployments, pin tested CUDA/PyTorch versions and isolate the inference workload.

## Production checklist

- TLS termination
- Authentication
- Per-user rate limits
- Request and inference timeouts
- Sandboxed media decoding
- Malware scanning
- Encrypted temporary storage
- Automatic deletion
- Observability and audit logging
- GPU/CPU resource quotas
- Model and dataset license review
- Versioned evaluation reports
