import hashlib
import time
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from aidetection.limits import MAX_UPLOAD_BYTES
from aidetection.service import DetectionService

app = FastAPI(
    title="AiDetection API",
    version="0.4.1",
    description="Multimodal AI-media detection API.",
)
service = DetectionService()


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(Path(__file__).resolve().parent.parent / "web" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "aidetection", "version": "0.4.1"}


@app.get("/v1/capabilities")
def capabilities():
    return {
        "modalities": ["image", "audio", "video"],
        "detector_status": "optional-model-backed",
        "max_upload_bytes": MAX_UPLOAD_BYTES,
    }


@app.post("/v1/analyze")
async def analyze(file: UploadFile = File(...)):  # noqa: B008
    started = time.perf_counter()
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    try:
        result = service.analyze_upload(data, file.filename or "", file.content_type)
    except ValueError as exc:
        message = str(exc)
        if "exceeds" in message:
            status = 413
        elif "media type" in message or "signature" in message:
            status = 415
        else:
            status = 400
        raise HTTPException(status, message) from exc
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    return {
        "media_type": result.media_type.value,
        "label": result.label,
        "confidence": result.confidence,
        "signals": list(result.signals),
        "sha256": hashlib.sha256(data).hexdigest(),
        "processing_ms": round((time.perf_counter() - started) * 1000, 2),
    }
