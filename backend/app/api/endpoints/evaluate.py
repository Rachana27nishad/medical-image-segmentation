from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/evaluate/benchmark")
async def run_benchmark():
    """
    PLANNED - Phase 4.
    Will compare all models on a held-out test set and return Dice, IoU, Precision,
    Recall and HD95 per model and per modality.
    """
    raise HTTPException(
        status_code=501,
        detail="Benchmark endpoint is not implemented yet (planned for Phase 4). "
        "See README -> Implementation Plan.",
    )
