from fastapi import FastAPI, File, HTTPException, UploadFile
from src.aidetection.limits import validate_size
from src.aidetection.service import DetectionService

app=FastAPI(title="AiDetection API",version="0.3.0",description="Multimodal AI-media detection API.")
service=DetectionService()

@app.get("/health")
def health():
    return {"status":"ok","service":"aidetection","version":"0.3.0"}

@app.get("/v1/capabilities")
def capabilities():
    return {"modalities":["image","audio","video"],"detector_status":"conservative-baseline","max_upload_bytes":25*1024*1024}

@app.post("/v1/analyze")
async def analyze(file: UploadFile=File(...)):
    data=await file.read()
    try:
        validate_size(data)
        result=service.analyze_upload(data,file.filename or "",file.content_type)
    except ValueError as exc:
        message=str(exc)
        status=415 if "media type" in message else 413 if "exceeds" in message else 400
        raise HTTPException(status,message) from exc
    return {"media_type":result.media_type.value,"label":result.label,"confidence":result.confidence,"signals":list(result.signals)}
