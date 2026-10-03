"""
PLANNED - Phase 3: inference engine.

Pipeline to implement:
    image -> (optional) HU window -> (optional) CLAHE -> min-max normalise -> resize 256x256
          -> model(tensor) -> softmax -> foreground probability -> resize back
          -> threshold -> binary mask -> overlay + contour (OpenCV) -> base64

TODO (Phase 3):
    [ ] load trained weights from settings.WEIGHTS_DIR/<model_id>.pt
    [ ] run_inference(image, model_name, threshold, window_preset, apply_clahe)
    [ ] overlay / contour rendering
    [ ] return mask + probability statistics
"""


class InferenceEngine:
    def run_inference(self, *args, **kwargs):
        raise NotImplementedError("Inference engine is planned for Phase 3 - see README.")
