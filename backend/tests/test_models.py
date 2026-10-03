import torch

from app.models.unet import UNet


def test_unet_forward_shape():
    model = UNet(n_channels=1, n_classes=2).eval()
    with torch.no_grad():
        out = model(torch.randn(2, 1, 128, 128))
    assert out.shape == (2, 2, 128, 128)


def test_unet_handles_odd_sizes():
    model = UNet(n_channels=1, n_classes=2).eval()
    with torch.no_grad():
        out = model(torch.randn(1, 1, 130, 126))
    assert out.shape == (1, 2, 130, 126)
