from fastapi import APIRouter
import base64
import cv2
from app.services.synthetic_data import MedicalDataGenerator

router = APIRouter()

@router.get("/data/samples")
async def get_samples():
    """
    Get sample multi-modal medical images with ground truth masks encoded as base64.
    """
    samples_data = []
    
    generators = [
        ("brain_mri", MedicalDataGenerator.generate_brain_mri_sample),
        ("lung_ct", MedicalDataGenerator.generate_lung_ct_sample),
        ("abdomen_ct", MedicalDataGenerator.generate_abdominal_ct_sample)
    ]

    for s_id, gen_fn in generators:
        sample = gen_fn()
        img = sample["image"]
        mask = sample["mask"]

        # Base64 image
        _, img_buf = cv2.imencode('.png', img)
        img_b64 = f"data:image/png;base64,{base64.b64encode(img_buf).decode('utf-8')}"

        # Base64 mask
        _, mask_buf = cv2.imencode('.png', mask)
        mask_b64 = f"data:image/png;base64,{base64.b64encode(mask_buf).decode('utf-8')}"

        samples_data.append({
            "id": s_id,
            "modality": sample["modality"],
            "target": sample["target"],
            "preset": sample["preset"],
            "description": sample["description"],
            "image_b64": img_b64,
            "mask_b64": mask_b64,
            "width": img.shape[1],
            "height": img.shape[0]
        })

    return {"samples": samples_data}
