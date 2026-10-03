"""
PLANNED - Phase 2: MONAI SegResNet wrapper.

TODO (Phase 2):
    [ ] wrap monai.networks.nets.SegResNet(spatial_dims=2, in_channels=1, out_channels=2, ...)
    [ ] same forward signature as UNet so every model can be trained/evaluated by the same code
    [ ] unit test: output shape == (B, n_classes, H, W)
"""


class MONAISegResNetWrapper:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("MONAI SegResNet is planned for Phase 2 - see README.")
