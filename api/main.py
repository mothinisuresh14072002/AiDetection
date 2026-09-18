from fastapi import FastAPI, File, HTTPException, UploadFile
from src.aidetection.core import detect_media_type
from src.aidetection.limits import validate_size
from src.aidetection.service import DetectionService

app = FastAPI(
    title="AiDetection API",
    version="0.2.0",
    description="Conservative multimodal AI-media detection API.",
)
service = DetectionService()

@app.get("/health")
def health():
    return {"status": "ok", "service": "aidetection", "version": "0.2.0"}

@app.get("/v1/capabilities")
def capabilities():
    return {
        "modalities": ["image", "audio", "video"],
        "detector_status": "baseline",
        "max_upload_bytes": 25 * 1024 * 1024,
    }

@app.post("/v1/analyze")
async def analyze(file: UploadFile = File(...)):
    data = await file.read()
    try:
        validate_size(data)
    except ValueError as exc:
        raise HTTPException(413, str(exc)) from exc
    media_type = detect_media_type(file.filename or "", file.content_type)
    if media_type.value == "unknown":
        raise HTTPException(415, "Unsupported or unknown media type")
    result = service.analyze(data, media_type)
    return {
        "media_type": result.media_type.value,
        "label": result.label,
        "confidence": result.confidence,
        "signals": list(result.signals),
    }
