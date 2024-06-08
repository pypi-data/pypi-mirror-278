from typing import TypedDict, NamedTuple, Sequence
from haskellian import iter as I
from jaxtyping import Int
import torch
from ...multi import Sample as WordSample

class Sample(NamedTuple):
  input_ids: Int[torch.Tensor, 'L']
  fens: Int[torch.Tensor, 'B L 64']
  ucis: Int[torch.Tensor, 'B L 5']

class Batch(TypedDict):
  input_ids: Int[torch.Tensor, 'B L']
  fens: Int[torch.Tensor, 'B L 64']
  ucis: Int[torch.Tensor, 'B L 5']
  attn_mask: Int[torch.Tensor, 'B L']

def sample_from(sample: WordSample) -> Sample:
  return Sample(
    input_ids=torch.tensor(sample['input_ids']),
    fens=torch.tensor(sample['fens']),
    ucis=torch.tensor(sample['ucis'])
  )

def collate_fn(batch: Sequence[Sample], *, pad_token_id: int, ignore_idx: int = -100, maxlen: int) -> Batch:

  input_ids, fens, ucis = I.unzip(batch)
  batch_size = len(input_ids)
  maxlen = min(max(len(x) for x in input_ids), maxlen)
  padded_input_ids = torch.full((batch_size, maxlen), fill_value=pad_token_id)
  padded_fens = torch.full((batch_size, maxlen, 64), fill_value=ignore_idx)
  padded_ucis = torch.full((batch_size, maxlen, 5), fill_value=ignore_idx)
  attn_mask = torch.zeros((batch_size, maxlen))

  for i in range(batch_size):
    l = len(input_ids[i])
    padded_input_ids[i, :l] = input_ids[i]
    padded_fens[i, :l] = fens[i]
    padded_ucis[i, :l] = ucis[i]
    attn_mask[i, :l] = 1

  return Batch(input_ids=padded_input_ids, fens=padded_fens, ucis=padded_ucis, attn_mask=attn_mask)

class BatchRNN(TypedDict):
  input_ids: Int[torch.Tensor, 'B L']
  fens: Int[torch.Tensor, 'B L 64']
  ucis: Int[torch.Tensor, 'B L 5']
  seq_lens: Sequence[int]

def collate_rnn(batch: Sequence[Sample], pad_token_id: int, ignore_idx: int = -100) -> BatchRNN:

  input_ids, fens, ucis = I.unzip(batch)
  batch_size = len(input_ids)
  seq_lens = [len(x) for x in input_ids]
  maxlen = max(seq_lens)
  padded_input_ids = torch.full((batch_size, maxlen), fill_value=pad_token_id)
  padded_fens = torch.full((batch_size, maxlen, 64), fill_value=ignore_idx)
  padded_ucis = torch.full((batch_size, maxlen, 5), fill_value=ignore_idx)

  for i in range(batch_size):
    l = len(input_ids[i])
    padded_input_ids[i, :l] = input_ids[i]
    padded_fens[i, :l] = fens[i]
    padded_ucis[i, :l] = ucis[i]

  return BatchRNN(input_ids=padded_input_ids, fens=padded_fens, ucis=padded_ucis, seq_lens=seq_lens)
