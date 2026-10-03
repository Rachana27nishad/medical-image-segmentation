import numpy as np

from app.services.preprocessing import ImagePreprocessor
from app.services.synthetic_data import MedicalDataGenerator


def test_synthetic_samples_have_mask_and_expected_shape():
    for gen in (
        MedicalDataGenerator.generate_brain_mri_sample,
        MedicalDataGenerator.generate_lung_ct_sample,
        MedicalDataGenerator.generate_abdominal_ct_sample,
    ):
        sample = gen()
        assert sample["image"].shape == (256, 256)
        assert sample["image"].dtype == np.uint8
        assert sample["mask"].sum() > 0


def test_ct_window_output_is_uint8_full_range():
    img = np.linspace(-1000, 1000, 256 * 256, dtype=np.float32).reshape(256, 256)
    out = ImagePreprocessor.apply_ct_window(img, "abdomen")
    assert out.dtype == np.uint8
    assert out.min() == 0 and out.max() == 255


def test_pseudo_hu_range():
    img = np.array([[0, 255]], dtype=np.uint8)
    hu = ImagePreprocessor.intensity_to_pseudo_hu(img)
    assert hu[0, 0] == -1000 and hu[0, 1] == 1000


def test_clahe_keeps_shape_and_dtype():
    img = MedicalDataGenerator.generate_brain_mri_sample()["image"]
    out = ImagePreprocessor.apply_clahe(img)
    assert out.shape == img.shape and out.dtype == np.uint8


def test_min_max_normalisation_bounds():
    out = ImagePreprocessor.normalize_min_max(np.array([[10, 20], [30, 50]], dtype=np.uint8))
    assert out.min() == 0.0 and out.max() == 1.0
