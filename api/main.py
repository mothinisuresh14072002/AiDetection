from fastapi import FastAPI, File, HTTPException, UploadFile
from src.aidetection.core import analyze_bytes, detect_media_type

app = FastAPI(title="AiDetection API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "aidetection"}

@app.post("/v1/analyze")
async def analyze(file: UploadFile = File(...)):
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file")
    media_type = detect_media_type(file.filename or "", file.content_type)
    if media_type.value == "unknown":
        raise HTTPException(415, "Unsupported or unknown media type")
    result = analyze_bytes(data, media_type)
    return {"media_type": result.media_type.value, "label": result.label,
            "confidence": result.confidence, "signals": list(result.signals)}
