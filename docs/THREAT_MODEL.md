# Threat model

Treat uploaded media as hostile input.

## Risks
- Oversized uploads and resource exhaustion
- Malformed media triggering parser bugs
- Malicious files disguised by extensions
- Sensitive media retention
- Model denial-of-service through expensive inference
- False positives causing real-world harm

## Current controls
- 25 MiB upload limit
- No media persistence by default
- Lazy optional model loading
- Explicit uncertainty baseline
- Structured API errors

## Production controls
Add authentication, rate limiting, request timeouts, sandboxed media decoding, malware scanning, strict MIME/magic validation, encrypted temporary storage, automatic deletion, audit logging, and GPU workload isolation.
