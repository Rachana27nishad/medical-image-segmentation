import numpy as np
import cv2
from typing import Tuple, Dict, Any

class ImagePreprocessor:
    """Medical Image Preprocessing pipeline including CT Windowing, CLAHE, and Normalization."""

    CT_WINDOWS = {
        "brain": {"center": 40, "width": 80},
        "lung": {"center": -600, "width": 1500},
        "abdomen": {"center": 40, "width": 400},
        "bone": {"center": 400, "width": 1800},
        "liver": {"center": 60, "width": 160},
        "default": None
    }

    @staticmethod
    def intensity_to_pseudo_hu(img_u8: np.ndarray, hu_min: float = -1000.0, hu_max: float = 1000.0) -> np.ndarray:
        """
        Linearly map an 8-bit image (0-255) to a *simulated* Hounsfield range.
        Needed because the demo/synthetic images are 8-bit, while the window presets
        are defined in HU. Real DICOM/NIfTI CT data already is in HU and skips this step.
        """
        return hu_min + (img_u8.astype(np.float32) / 255.0) * (hu_max - hu_min)

    @staticmethod
    def apply_ct_window(img_hu: np.ndarray, window_preset: str = "abdomen") -> np.ndarray:
        """Apply Hounsfield Unit (HU) windowing to CT images."""
        if window_preset not in ImagePreprocessor.CT_WINDOWS or ImagePreprocessor.CT_WINDOWS[window_preset] is None:
            return img_hu

        win = ImagePreprocessor.CT_WINDOWS[window_preset]
        win_min = win["center"] - (win["width"] / 2.0)
        win_max = win["center"] + (win["width"] / 2.0)

        img_windowed = np.clip(img_hu, win_min, win_max)
        img_norm = (img_windowed - win_min) / (win_max - win_min)
        return (img_norm * 255.0).astype(np.uint8)

    @staticmethod
    def apply_clahe(img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)."""
        if len(img.shape) == 3 and img.shape[2] == 3:
            # Convert to LAB for color images
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            return cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        else:
            if img.dtype != np.uint8:
                img_u8 = ((img - img.min()) / (img.max() - img.min() + 1e-8) * 255.0).astype(np.uint8)
            else:
                img_u8 = img
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
            return clahe.apply(img_u8)

    @staticmethod
    def normalize_min_max(img: np.ndarray) -> np.ndarray:
        """Min-Max normalize image to [0, 1]."""
        img_min, img_max = img.min(), img.max()
        if img_max - img_min < 1e-8:
            return np.zeros_like(img, dtype=np.float32)
        return (img.astype(np.float32) - img_min) / (img_max - img_min)

    @staticmethod
    def normalize_z_score(img: np.ndarray) -> np.ndarray:
        """Z-score normalization (zero mean, unit variance)."""
        mean = np.mean(img)
        std = np.std(img)
        if std < 1e-8:
            return img - mean
        return (img - mean) / std

    @staticmethod
    def resize_image(img: np.ndarray, target_size: Tuple[int, int] = (256, 256)) -> np.ndarray:
        """Resize image to target shape."""
        return cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
