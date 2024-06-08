from typing import Sequence
from jaxtyping import Float, Int
import torch
import chess_utils as cu
from ...uci._labels import decode_uci

def argmax_preds(logits: Float[torch.Tensor, 'B L 36']) -> Int[torch.Tensor, 'B L 5']:
  batch_size = logits.size(0)
  from_files = torch.argmax(logits[:, :, 0:8].reshape(batch_size, -1, 8), dim=-1)
  from_ranks = torch.argmax(logits[:, :, 8:16].reshape(batch_size, -1, 8), dim=-1)
  to_files = torch.argmax(logits[:, :, 16:24].reshape(batch_size, -1, 8), dim=-1)
  to_ranks = torch.argmax(logits[:, :, 24:32].reshape(batch_size, -1, 8), dim=-1)
  proms = torch.argmax(logits[:, :, 32:36].reshape(batch_size, -1, 4), dim=-1)
  return torch.stack([from_files, from_ranks, to_files, to_ranks, proms], dim=-1)

def argmax_ucis(logits: Float[torch.Tensor, 'B L 36']) -> Sequence[Sequence[str]]:
  batch_size = logits.size(0)
  from_files, from_ranks, to_files, to_ranks, proms = argmax_preds(logits).unbind(-1)
  
  return [
    [
      decode_uci(*[int(i.item()) for i in idxs])
      for idxs in zip(from_files[b], from_ranks[b], to_files[b], to_ranks[b], proms[b])
    ]
    for b in range(batch_size)
  ]

def greedy_pgn(logits: Float[torch.Tensor, 'B L 36']) -> Sequence[Sequence[str]]:
  return [list(cu.ucis2sans(ucis)) for ucis in argmax_ucis(logits)]