"""
Phase-1 verification demo  (run:  python run_demo.py)

Shows what is finished in this submission:
  [1] U-Net architecture (forward pass, output shape, parameter count)
  [2] Synthetic multi-modal data generator (Brain MRI / Chest CT / Abdominal CT)
  [3] Preprocessing (CT windowing, CLAHE, normalisation) + saves a preview PNG
  [4] Evaluation metrics (Dice, IoU, HD95 ...) on a deliberately perturbed mask

NOTE: the model is NOT trained yet (Phase 3), so no model-accuracy numbers are shown.
"""
import os
import sys

import cv2
import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.models.unet import UNet                                   # noqa: E402
from app.services.metrics import SegmentationMetrics               # noqa: E402
from app.services.preprocessing import ImagePreprocessor           # noqa: E402
from app.services.synthetic_data import MedicalDataGenerator       # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(__file__), "docs", "images")


def header(title):
    print("\n" + "=" * 70 + f"\n  {title}\n" + "=" * 70)


def main():
    header("Medical Image Segmentation - Phase 1 Demo")

    # ---- 1. Model ----------------------------------------------------------
    print("\n[1/4] U-Net architecture")
    model = UNet(n_channels=1, n_classes=2).eval()
    with torch.no_grad():
        out = model(torch.randn(1, 1, 256, 256))
    n_params = sum(p.numel() for p in model.parameters()) / 1e6
    print(f"  input  : (1, 1, 256, 256)")
    print(f"  output : {tuple(out.shape)}   parameters: {n_params:.2f} M")
    assert out.shape == (1, 2, 256, 256)
    print("  [PASSED] forward pass OK  (weights are random - training is Phase 3)")

    # ---- 2. Data -----------------------------------------------------------
    print("\n[2/4] Synthetic data generator")
    samples = {
        "brain_mri": MedicalDataGenerator.generate_brain_mri_sample(),
        "lung_ct": MedicalDataGenerator.generate_lung_ct_sample(),
        "abdomen_ct": MedicalDataGenerator.generate_abdominal_ct_sample(),
    }
    for sid, s in samples.items():
        print(f"  {sid:<11} {s['modality']:<13} target={s['target']:<22} lesion area={int((s['mask'] > 0).sum())} px")

    # ---- 3. Preprocessing --------------------------------------------------
    print("\n[3/4] Preprocessing pipeline")
    rows = []
    for sid, s in samples.items():
        img = s["image"]
        hu = ImagePreprocessor.intensity_to_pseudo_hu(img)
        windowed = ImagePreprocessor.apply_ct_window(hu, s["preset"])
        clahe = ImagePreprocessor.apply_clahe(windowed)
        rows.append(np.hstack([img, windowed, clahe]))
        print(f"  {sid:<11} window='{s['preset']}'  mean {img.mean():6.1f} -> {windowed.mean():6.1f} -> (CLAHE) {clahe.mean():6.1f}")
    os.makedirs(OUT_DIR, exist_ok=True)
    preview = np.vstack(rows)
    cv2.imwrite(os.path.join(OUT_DIR, "preprocessing_preview.png"), preview)
    print(f"  [PASSED] preview saved -> docs/images/preprocessing_preview.png  (original | windowed | CLAHE)")

    # ---- 4. Metrics --------------------------------------------------------
    print("\n[4/4] Evaluation metrics (ground truth vs. a shifted + eroded copy of itself)")
    gt = samples["brain_mri"]["mask"]
    shifted = np.roll(gt, shift=(4, 6), axis=(0, 1))
    pred = cv2.erode(shifted, np.ones((3, 3), np.uint8), iterations=2)
    m = SegmentationMetrics.compute_all_metrics(pred, gt, threshold=128)
    print(f"  Dice={m['dice']:.4f}  IoU={m['iou']:.4f}  Precision={m['precision']:.4f}  "
          f"Recall={m['recall']:.4f}  HD95={m['hd95']:.2f}px  VolDiff={m['volumetric_difference_pct']:.2f}%")
    perfect = SegmentationMetrics.compute_all_metrics(gt, gt, threshold=128)
    assert perfect["dice"] == 1.0 and perfect["hd95"] == 0.0
    print("  [PASSED] metric sanity check (identical masks -> Dice 1.0, HD95 0.0)")

    print("\n[SUCCESS] Phase 1 components verified.  Next: Attention U-Net, training, inference (see README).")


if __name__ == "__main__":
    main()
