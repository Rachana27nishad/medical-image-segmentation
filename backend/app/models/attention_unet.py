"""
PLANNED - Phase 2: Attention U-Net.

Idea: U-Net + an Attention Gate on every skip connection.
    g  = gating signal (decoder feature, coarser, more semantic)
    x  = skip feature  (encoder feature, finer, more spatial)
    alpha = sigmoid( psi( ReLU( W_g(g) + W_x(x) ) ) )      # values in [0, 1] per pixel
    output = x * alpha                                      # background is suppressed

TODO (Phase 2):
    [ ] class AttentionGate(nn.Module)       -> F_g, F_l, F_int 1x1 convs + BN + sigmoid
    [ ] class UpBlockAttention(nn.Module)    -> upsample, attention on skip, concat, DoubleConv
    [ ] class AttentionUNet(nn.Module)       -> same encoder as unet.UNet, attention decoder
    [ ] unit test: output shape == (B, n_classes, H, W)
"""


class AttentionUNet:  # placeholder so imports fail loudly instead of silently
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("AttentionUNet is planned for Phase 2 - see README.")
