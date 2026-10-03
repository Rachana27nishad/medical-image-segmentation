import numpy as np
from scipy.spatial.distance import directed_hausdorff
from typing import Dict, Any

class SegmentationMetrics:
    """Quantitative Evaluation Metrics for Medical Image Segmentation."""

    @staticmethod
    def compute_all_metrics(pred_mask: np.ndarray, gt_mask: np.ndarray, threshold: float = 0.5) -> Dict[str, float]:
        """
        Compute full metric suite comparing binary prediction vs ground truth mask.
        """
        pred_bin = (pred_mask > threshold).astype(np.uint8)
        gt_bin = (gt_mask > 0.5).astype(np.uint8)

        tp = np.sum((pred_bin == 1) & (gt_bin == 1))
        fp = np.sum((pred_bin == 1) & (gt_bin == 0))
        fn = np.sum((pred_bin == 0) & (gt_bin == 1))
        tn = np.sum((pred_bin == 0) & (gt_bin == 0))

        # Dice Similarity Coefficient
        dice = (2.0 * tp) / (2.0 * tp + fp + fn + 1e-8)

        # Intersection over Union (Jaccard Index)
        iou = tp / (tp + fp + fn + 1e-8)

        # Precision & Recall
        precision = tp / (tp + fp + 1e-8)
        recall = tp / (tp + fn + 1e-8)  # Sensitivity

        # Specificity
        specificity = tn / (tn + fp + 1e-8)

        # F1 Score
        f1_score = dice

        # Hausdorff Distance
        hd95, hd_max = SegmentationMetrics.compute_hausdorff_distance(pred_bin, gt_bin)

        # Volumetric Difference (%)
        # cast to Python int: np.sum on uint8 returns uint64 and `pred - gt` would wrap around
        vol_gt = int(np.sum(gt_bin))
        vol_pred = int(np.sum(pred_bin))
        vol_diff_pct = float(abs(vol_pred - vol_gt) / (vol_gt + 1e-8) * 100.0)

        return {
            "dice": float(round(dice, 4)),
            "iou": float(round(iou, 4)),
            "precision": float(round(precision, 4)),
            "recall": float(round(recall, 4)),
            "specificity": float(round(specificity, 4)),
            "f1_score": float(round(f1_score, 4)),
            "hd95": float(round(hd95, 2)),
            "hd_max": float(round(hd_max, 2)),
            "volumetric_difference_pct": float(round(vol_diff_pct, 2)),
            "tp": int(tp),
            "fp": int(fp),
            "fn": int(fn),
            "tn": int(tn)
        }

    @staticmethod
    def compute_hausdorff_distance(pred_bin: np.ndarray, gt_bin: np.ndarray) -> tuple:
        """
        Compute Hausdorff Distance (95th percentile and maximum).
        """
        pred_pts = np.argwhere(pred_bin > 0)
        gt_pts = np.argwhere(gt_bin > 0)

        if len(pred_pts) == 0 or len(gt_pts) == 0:
            if len(pred_pts) == 0 and len(gt_pts) == 0:
                return 0.0, 0.0
            return 999.0, 999.0

        # Calculate forward and backward directed Hausdorff distances
        d_pred_gt, _, _ = directed_hausdorff(pred_pts, gt_pts)
        d_gt_pred, _, _ = directed_hausdorff(gt_pts, pred_pts)

        hd_max = max(d_pred_gt, d_gt_pred)

        # Approximate HD95 using 95th percentile of nearest point distances
        try:
            from scipy.spatial import KDTree
            tree_gt = KDTree(gt_pts)
            distances_pred, _ = tree_gt.query(pred_pts)
            
            tree_pred = KDTree(pred_pts)
            distances_gt, _ = tree_pred.query(gt_pts)
            
            all_distances = np.concatenate([distances_pred, distances_gt])
            hd95 = np.percentile(all_distances, 95)
        except Exception:
            hd95 = hd_max * 0.95

        return float(hd95), float(hd_max)
