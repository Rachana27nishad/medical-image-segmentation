import base64
import io
from typing import Optional

import cv2
import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image

from app.services.preprocessing import ImagePreprocessor
from app.services.synthetic_data import MedicalDataGenerator

router = APIRouter()

SAMPLE_GENERATORS = {
    "brain_mri": MedicalDataGenerator.generate_brain_mri_sample,
    "lung_ct": MedicalDataGenerator.generate_lung_ct_sample,
    "abdomen_ct": MedicalDataGenerator.generate_abdominal_ct_sample,
}


def _to_b64_png(img: np.ndarray) -> str:
    ok, buf = cv2.imencode(".png", img)
    if not ok:
        raise HTTPException(status_code=500, detail="Could not encode image")
    return f"data:image/png;base64,{base64.b64encode(buf).decode('utf-8')}"


@router.post("/preprocess")
async def preprocess_image(
    sample_id: Optional[str] = Form("brain_mri"),
    window_preset: str = Form("default"),
    apply_clahe: bool = Form(False),
    file: Optional[UploadFile] = File(None),
):
    """
    Phase-1 demo endpoint: apply CT windowing and/or CLAHE and return the original
    and processed image (base64 PNG) with simple intensity statistics.
    """
    if file is not None:
        try:
            pil_img = Image.open(io.BytesIO(await file.read())).convert("L")
            original = np.array(pil_img)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {exc}")
    else:
        if sample_id not in SAMPLE_GENERATORS:
            raise HTTPException(status_code=404, detail=f"Unknown sample_id '{sample_id}'")
        original = SAMPLE_GENERATORS[sample_id]()["image"]

    processed = original.copy()
    if window_preset != "default":
        # The demo images are 8-bit, so map them to a simulated HU range first.
        hu = ImagePreprocessor.intensity_to_pseudo_hu(processed)
        processed = ImagePreprocessor.apply_ct_window(hu, window_preset)
    if apply_clahe:
        processed = ImagePreprocessor.apply_clahe(processed)

    return {
        "success": True,
        "window_preset": window_preset,
        "apply_clahe": apply_clahe,
        "original_b64": _to_b64_png(original),
        "processed_b64": _to_b64_png(processed),
        "stats": {
            "original": {"min": int(original.min()), "max": int(original.max()), "mean": round(float(original.mean()), 2)},
            "processed": {"min": int(processed.min()), "max": int(processed.max()), "mean": round(float(processed.mean()), 2)},
        },
    }
