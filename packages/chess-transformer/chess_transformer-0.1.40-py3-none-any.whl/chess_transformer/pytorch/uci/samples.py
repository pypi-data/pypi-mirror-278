from typing import NamedTuple, Sequence
from haskellian import iter as I
from jaxtyping import Int
import torch
from ...uci import Sample as WordSample

class Sample(NamedTuple):
  input_ids: Int[torch.Tensor, 'L']
  labs: Int[torch.Tensor, 'L 5']
  uci_labs: Sequence[str]

class Batch(NamedTuple):
  input_ids: Int[torch.Tensor, 'B L']
  labs: Int[torch.Tensor, 'B L 5']
  uci_labs: Sequence[Sequence[str]]

def sample_from(sample: WordSample, uci_labs: Sequence[str]) -> Sample:
  return Sample(torch.tensor(sample.input_ids), torch.tensor(sample.labs), uci_labs)

def collate_fn(batch: Sequence[Sample], pad_token_id: int, ignore_idx: int = -100) -> Batch:

  input_ids, labs, uci_labs = I.unzip(batch)
  batch_size = len(input_ids)
  maxlen = max(len(x) for x in input_ids)
  padded_input_ids = torch.full((batch_size, maxlen), fill_value=pad_token_id)
  padded_labs = torch.full((batch_size, maxlen, 5), fill_value=ignore_idx)

  for i in range(batch_size):
    l = len(input_ids[i])
    padded_input_ids[i, :l] = input_ids[i]
    padded_labs[i, :l] = labs[i]

  return Batch(padded_input_ids, padded_labs, uci_labs)
