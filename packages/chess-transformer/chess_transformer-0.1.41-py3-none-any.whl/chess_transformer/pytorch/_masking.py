from jaxtyping import Int
import torch
from torch import Tensor

def first_masks(masked_ids: Int[torch.Tensor, 'B L'], *, mask_id: int) -> Int[torch.Tensor, 'B']:
  """Indices of the first mask in each row of `masked_ids`. Returns -1's on rows without masks."""
  have_masks = (masked_ids == mask_id).any(dim=-1)
  max_idx = torch.argmax((masked_ids == mask_id).float(), dim=-1)
  max_idx[torch.where(~have_masks)] = -1
  return max_idx

def random_masking(
  batch: Int[Tensor, 'batch maxlen'],
  attn_mask: Int[Tensor, 'batch maxlen'] | None = None,
  *, mask_id: int, mask_prob: float
):
  """Mask `batch` with `mask_id` with probability `mask_prob`.
  - If provided, positions with `attn_mask == 0` are excluded from masking.
  """
  rand = torch.rand(batch.shape, device=batch.device)
  indices = (rand < mask_prob) & (attn_mask is None or attn_mask == 1)
  output = batch.clone()
  output[indices] = mask_id
  return output
