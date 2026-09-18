import hashlib
import time
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from aidetection.limits import MAX_UPLOAD_BYTES
from aidetection.service import DetectionService

app = FastAPI(
    title="AiDetection API",
    version="0.4.1",
    description="Multimodal AI-media detection API.",
)
service = DetectionService()


class AnalysisResponse(BaseModel):
    media_type: str
    label: str
    confidence: float = Field(ge=0, le=1)
    ai_probability: float = Field(ge=0, le=1)
    signals: list[str]
    sha256: str = Field(min_length=64, max_length=64)
    processing_ms: float = Field(ge=0)
    request_id: str


class ErrorResponse(BaseModel):
    detail: str
    request_id: str


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
        "model_inference": False,
    }


@app.post("/v1/analyze", response_model=AnalysisResponse)
async def analyze(file: UploadFile = File(...)):  # noqa: B008
    started = time.perf_counter()
    request_id = uuid4().hex
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    try:
        result = service.analyze_upload(data, file.filename or "", file.content_type)
    except ValueError as exc:
        message = str(exc)
        status = 413 if "exceeds" in message else 415 if "media type" in message or "signature" in message else 400
        raise HTTPException(status, {"detail": message, "request_id": request_id}) from exc
    except RuntimeError as exc:
        raise HTTPException(503, {"detail": str(exc), "request_id": request_id}) from exc
    return AnalysisResponse(
        media_type=result.media_type.value,
        label=result.label,
        confidence=result.confidence,
        ai_probability=result.ai_probability,
        signals=list(result.signals),
        sha256=hashlib.sha256(data).hexdigest(),
        processing_ms=round((time.perf_counter() - started) * 1000, 2),
        request_id=request_id,
    )
