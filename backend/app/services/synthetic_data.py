import numpy as np
import cv2
from typing import Dict, Any, Tuple

class MedicalDataGenerator:
    """Synthetic Medical Image and Mask Generator for CT, MRI, and Retinal modalities."""

    @staticmethod
    def generate_brain_mri_sample(size: Tuple[int, int] = (256, 256), seed: int = 42) -> Dict[str, Any]:
        """Generate synthetic Brain MRI image with a simulated tumor/lesion."""
        np.random.seed(seed)
        h, w = size
        img = np.zeros((h, w), dtype=np.float32)
        mask = np.zeros((h, w), dtype=np.uint8)

        # 1. Skull and Brain Tissue Base (Ellipse)
        center = (w // 2, h // 2)
        axes = (int(w * 0.38), int(h * 0.42))
        cv2.ellipse(img, center, axes, 0, 0, 360, 140, -1)

        # 2. Ventricles (dark inner region)
        cv2.ellipse(img, (center[0] - 15, center[1]), (12, 30), 15, 0, 360, 40, -1)
        cv2.ellipse(img, (center[0] + 15, center[1]), (12, 30), -15, 0, 360, 40, -1)

        # 3. Brain texture/folds (Gaussian noise + smoothing)
        noise = np.random.normal(0, 15, (h, w))
        img = np.clip(img + noise, 0, 255)
        img = cv2.GaussianBlur(img, (5, 5), 1.0)

        # 4. Simulated Tumor / Glioma lesion (bright hyperintense region)
        tumor_center = (center[0] + 35, center[1] - 25)
        tumor_axes = (25, 20)
        cv2.ellipse(mask, tumor_center, tumor_axes, 30, 0, 360, 255, -1)
        
        # Add irregular tumor edges using noise displacement
        dist_grid = np.zeros((h, w), dtype=np.float32)
        cv2.ellipse(dist_grid, tumor_center, tumor_axes, 30, 0, 360, 1.0, -1)
        edge_noise = cv2.GaussianBlur(np.random.normal(0, 0.2, (h, w)), (7, 7), 2.0)
        mask = ((dist_grid + edge_noise) > 0.6).astype(np.uint8) * 255

        # Blend hyperintensity in MRI
        img[mask > 0] = np.clip(img[mask > 0] * 1.6 + 60, 0, 255)
        img = cv2.GaussianBlur(img, (3, 3), 0.8)

        return {
            "image": img.astype(np.uint8),
            "mask": mask,
            "modality": "Brain MRI",
            "target": "Brain Tumor / Glioma",
            "preset": "brain",
            "description": "T2-weighted MRI brain scan showing hyperintense focal lesion in parietal lobe."
        }

    @staticmethod
    def generate_lung_ct_sample(size: Tuple[int, int] = (256, 256), seed: int = 101) -> Dict[str, Any]:
        """Generate synthetic Lung CT scan with pulmonary nodule."""
        np.random.seed(seed)
        h, w = size
        img = np.full((h, w), 180, dtype=np.float32)  # Chest wall background
        mask = np.zeros((h, w), dtype=np.uint8)

        # Lungs (dark low-density regions)
        left_lung = (int(w * 0.35), int(h * 0.5))
        right_lung = (int(w * 0.65), int(h * 0.5))
        lung_axes = (int(w * 0.18), int(h * 0.32))

        cv2.ellipse(img, left_lung, lung_axes, -10, 0, 360, 30, -1)
        cv2.ellipse(img, right_lung, lung_axes, 10, 0, 360, 30, -1)

        # Spine and ribs (bright high HU density)
        cv2.circle(img, (w // 2, int(h * 0.82)), 14, 240, -1)

        # Vascular branching inside lungs
        for _ in range(8):
            pt1 = (left_lung[0] + np.random.randint(-15, 15), left_lung[1] + np.random.randint(-30, 30))
            pt2 = (pt1[0] + np.random.randint(-20, 20), pt1[1] + np.random.randint(-20, 20))
            cv2.line(img, pt1, pt2, 110, 2)

        # Simulated Nodule / Tumor in Right Lung
        nodule_center = (right_lung[0] + 12, right_lung[1] - 20)
        cv2.circle(mask, nodule_center, 18, 255, -1)
        img[mask > 0] = 210

        img = cv2.GaussianBlur(img, (3, 3), 0.8)
        return {
            "image": img.astype(np.uint8),
            "mask": mask,
            "modality": "Chest CT",
            "target": "Pulmonary Nodule",
            "preset": "lung",
            "description": "Thoracic CT scan showing high-density solitary pulmonary nodule in right upper lobe."
        }

    @staticmethod
    def generate_abdominal_ct_sample(size: Tuple[int, int] = (256, 256), seed: int = 202) -> Dict[str, Any]:
        """Generate synthetic Abdominal CT scan with liver tumor."""
        np.random.seed(seed)
        h, w = size
        img = np.full((h, w), 40, dtype=np.float32)
        mask = np.zeros((h, w), dtype=np.uint8)

        # Liver contour (large organ in right upper quadrant)
        pts = np.array([
            [int(w * 0.2), int(h * 0.3)],
            [int(w * 0.65), int(h * 0.25)],
            [int(w * 0.72), int(h * 0.65)],
            [int(w * 0.4), int(h * 0.75)],
            [int(w * 0.2), int(h * 0.5)]
        ], np.int32)
        cv2.fillPoly(img, [pts], 140)

        # Kidney (left quadrant)
        cv2.ellipse(img, (int(w * 0.75), int(h * 0.55)), (18, 30), 20, 0, 360, 160, -1)

        # Simulated Liver Lesion / Tumor
        lesion_center = (int(w * 0.48), int(h * 0.45))
        cv2.circle(mask, lesion_center, 22, 255, -1)
        img[mask > 0] = 75  # Hypodense liver tumor

        img = cv2.GaussianBlur(img, (3, 3), 0.8)
        return {
            "image": img.astype(np.uint8),
            "mask": mask,
            "modality": "Abdominal CT",
            "target": "Liver Tumors / Lesion",
            "preset": "abdomen",
            "description": "Contrast-enhanced Abdominal CT showing hypodense hepatic focal lesion."
        }
