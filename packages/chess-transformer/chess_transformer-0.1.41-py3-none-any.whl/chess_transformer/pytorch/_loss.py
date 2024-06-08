from typing import Sequence, Protocol
from jaxtyping import Int, Float
import torch
from torch import Tensor, nn

class AggregateFn(Protocol):
  def __call__(self, x: Float[Tensor, 'segment batch']) -> Float[Tensor, 'batch']: ...

class LossFn(Protocol):
  def __call__(
    self, logits: Float[Tensor, 'batch seq_len _'],
    labels: Int[Tensor, 'batch seq_len']
  ) -> Float[Tensor, '']:
    ...


def segmented_loss(
  logits: Float[Tensor, 'batch seq_len _'],
  labels: Int[Tensor, 'batch seq_len len(ends)'],
  *,
  loss: LossFn = nn.CrossEntropyLoss(ignore_index=-100),
  ends: Sequence[int],
) -> list[Float[Tensor, '']]:
  split_logits = [logits[:, :, i:j].transpose(1, 2) for i, j in zip([0, *ends[:-1]], ends)]
  split_labels = [labels[:, :, i] for i in range(len(ends))]
  return [loss(logits, labs) for logits, labs in zip(split_logits, split_labels)]
