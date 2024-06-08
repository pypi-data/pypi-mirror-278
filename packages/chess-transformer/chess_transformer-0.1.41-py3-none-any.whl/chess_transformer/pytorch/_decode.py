from typing import Sequence
from jaxtyping import Int, Float
import torch

def segmented_argmax(
  logits: Float[torch.Tensor, 'batch seq_len _'],
  *, ends: Sequence[int]
) -> Int[torch.Tensor, 'batch seq_len len(ends)']:
  split_logits = [logits[:, :, i:j] for i, j in zip([0, *ends[:-1]], ends)]
  argmaxs = [torch.argmax(split_logit, dim=-1) for split_logit in split_logits]
  return torch.stack(argmaxs, dim=-1)
