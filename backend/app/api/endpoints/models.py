from fastapi import APIRouter

router = APIRouter()


@router.get("/models")
async def list_models():
    """Model zoo. `status` tells which architectures are implemented in this submission."""
    return {
        "models": [
            {
                "id": "unet",
                "name": "Standard U-Net",
                "type": "Classic Convolutional Encoder-Decoder",
                "description": "2D U-Net with double-conv blocks, max-pool encoder and symmetric skip connections.",
                "parameters": "17.3M",
                "status": "implemented",
            },
            {
                "id": "attention_unet",
                "name": "Attention U-Net",
                "type": "Attention-Guided Encoder-Decoder",
                "description": "U-Net with attention gates on the skip connections to suppress irrelevant background.",
                "parameters": "13.8M",
                "status": "planned",
            },
            {
                "id": "monai_segresnet",
                "name": "MONAI SegResNet",
                "type": "Residual Encoder-Decoder",
                "description": "Residual encoder-decoder from the MONAI medical imaging framework.",
                "parameters": "-",
                "status": "planned",
            },
        ]
    }
