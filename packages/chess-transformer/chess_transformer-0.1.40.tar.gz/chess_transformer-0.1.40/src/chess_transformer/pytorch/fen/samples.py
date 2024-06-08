from typing import TypedDict, NamedTuple, Sequence
from haskellian import iter as I
from jaxtyping import Int
import torch
from ...fen import Sample as WordSample

class Sample(NamedTuple):
  input_ids: Int[torch.Tensor, 'L']
  labs: Int[torch.Tensor, 'L 5']

class Batch(TypedDict):
  input_ids: Int[torch.Tensor, 'B L']
  labs: Int[torch.Tensor, 'B L 64']
  attn_mask: Int[torch.Tensor, 'B L']

def sample_from(sample: WordSample) -> Sample:
  return Sample(torch.tensor(sample.input_ids), torch.tensor(sample.labs))

def collate_fn(batch: Sequence[Sample], pad_token_id: int, ignore_idx: int = -100) -> Batch:

  input_ids, labs = I.unzip(batch)
  batch_size = len(input_ids)
  maxlen = max(len(x) for x in input_ids)
  padded_input_ids = torch.full((batch_size, maxlen), fill_value=pad_token_id)
  padded_labs = torch.full((batch_size, maxlen, 64), fill_value=ignore_idx)
  attn_mask = torch.zeros((batch_size, maxlen))

  for i in range(batch_size):
    l = len(input_ids[i])
    padded_input_ids[i, :l] = input_ids[i]
    padded_labs[i, :l] = labs[i]
    attn_mask[i, :l] = 1

  return Batch(input_ids=padded_input_ids, labs=padded_labs, attn_mask=attn_mask)
