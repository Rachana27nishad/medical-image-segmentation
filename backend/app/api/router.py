from fastapi import APIRouter

from app.api.endpoints import data, evaluate, models, preprocess, segment

api_router = APIRouter()
api_router.include_router(models.router, tags=["Model Zoo"])
api_router.include_router(data.router, tags=["Medical Data"])
api_router.include_router(preprocess.router, tags=["Preprocessing"])
# Phase 2/3 - registered so they show up in /docs, but they answer HTTP 501 for now
api_router.include_router(segment.router, tags=["Segmentation (planned)"])
api_router.include_router(evaluate.router, tags=["Evaluation (planned)"])
