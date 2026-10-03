import numpy as np
from app.services.metrics import SegmentationMetrics

def test_perfect_overlap_metrics():
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[20:50, 20:50] = 255
    
    metrics = SegmentationMetrics.compute_all_metrics(mask, mask, threshold=128)
    assert metrics["dice"] == 1.0, f"Expected Dice 1.0, got {metrics['dice']}"
    assert metrics["iou"] == 1.0, f"Expected IoU 1.0, got {metrics['iou']}"
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["hd95"] == 0.0

def test_disjoint_masks():
    pred = np.zeros((100, 100), dtype=np.uint8)
    pred[0:20, 0:20] = 255

    gt = np.zeros((100, 100), dtype=np.uint8)
    gt[50:70, 50:70] = 255

    metrics = SegmentationMetrics.compute_all_metrics(pred, gt, threshold=128)
    assert metrics["dice"] == 0.0
    assert metrics["iou"] == 0.0
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0


def test_volumetric_difference_no_uint_overflow():
    """Regression: prediction smaller than ground truth used to wrap around (uint64)."""
    gt = np.zeros((100, 100), dtype=np.uint8)
    gt[10:60, 10:60] = 255          # 2500 px
    pred = np.zeros((100, 100), dtype=np.uint8)
    pred[10:35, 10:60] = 255        # 1250 px  -> exactly 50 % smaller
    m = SegmentationMetrics.compute_all_metrics(pred, gt, threshold=128)
    assert m["volumetric_difference_pct"] == 50.0
