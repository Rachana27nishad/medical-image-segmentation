"""
PLANNED - Phase 3: training script.

Planned recipe (see README -> Implementation Plan):
    data      : Medical Segmentation Decathlon (brain tumour, liver, lung) -> 2D slices, patient-wise split
    loss      : Dice loss + Cross-Entropy
    optimiser : Adam, lr = 1e-4, ReduceLROnPlateau
    schedule  : 50-100 epochs, batch 8-16, early stopping on validation Dice
    output    : backend/storage/weights/<model_id>.pt (best validation Dice)

TODO (Phase 3):
    [ ] SliceDataset (NIfTI -> 2D slices -> augmentation)
    [ ] DiceCELoss
    [ ] train_one_epoch / validate
    [ ] checkpointing + training curves
"""

if __name__ == "__main__":
    raise SystemExit("Training is planned for Phase 3 - see README.")
