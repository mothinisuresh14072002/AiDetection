# Deployment

## Docker

    docker compose up --build

Then open http://localhost:8000.

## Model-enabled deployment

Build an image with the models extra or install the models dependencies in the runtime image, then set AIDETECTION_ENABLE_MODELS=1.

For GPU deployments, use an NVIDIA-compatible runtime and pin tested CUDA/PyTorch versions. Do not enable model inference in an untrusted multi-tenant environment without resource controls.

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
