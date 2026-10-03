from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/segment")
async def segment_image():
    """
    PLANNED - Phase 2/3.
    Will accept an uploaded scan (or a sample id), run the selected model and return the
    mask overlay, tumour area and (for samples) quantitative metrics.
    """
    raise HTTPException(
        status_code=501,
        detail="Segmentation endpoint is not implemented yet (planned for Phase 2/3). "
        "See README -> Implementation Plan.",
    )
