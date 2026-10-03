import os

_BASE = os.path.join(os.path.dirname(__file__), "..", "..")


class Settings:
    PROJECT_NAME: str = "Medical Image Segmentation API (Phase 1)"
    VERSION: str = "0.1.0-phase1"
    API_V1_STR: str = "/api/v1"

    DEFAULT_IMG_SIZE: tuple = (256, 256)

    UPLOAD_DIR: str = os.path.join(_BASE, "storage", "uploads")
    SAMPLES_DIR: str = os.path.join(_BASE, "storage", "samples")
    WEIGHTS_DIR: str = os.path.join(_BASE, "storage", "weights")  # Phase 3: trained checkpoints go here


settings = Settings()
for _d in (settings.UPLOAD_DIR, settings.SAMPLES_DIR, settings.WEIGHTS_DIR):
    os.makedirs(_d, exist_ok=True)
