from typing_extensions import Sequence, TypedDict, NotRequired
from jaxtyping import Float, Int
from haskellian import iter as I
import numpy as np
import torch
from torch import Tensor, nn
from .._decode import segmented_argmax
from .._loss import segmented_loss
from ... import fen
from ..metrics import consecutive_eq, accuracy, intra_accuracy, \
  pre_bound_accuracy, post_bound_accuracy

LOGITS_ENDS = [13*(i+1) for i in range(64)]

def loss(
  logits: Float[Tensor, 'batch seq_len 64*13'],
  labels: Int[Tensor, 'batch seq_len 64'], *,
  ce_loss: nn.CrossEntropyLoss = nn.CrossEntropyLoss(ignore_index=-100)
) -> Float[Tensor, '']:
  """Cross-entropy loss summed across the board squares"""
  losses = segmented_loss(logits, labels, loss=ce_loss, ends=LOGITS_ENDS)
  return sum(l for l in losses if not torch.isnan(l)) # type: ignore

def argmax_preds(logits: Float[Tensor, 'B L 64*13']) -> Float[Tensor, 'B L 64']:
  return segmented_argmax(logits, ends=LOGITS_ENDS)

def argmax_fens(logits: Float[Tensor, 'B L 64*13']) -> list[list[str]]:
  argmaxs = argmax_preds(logits)
  return I.ndmap(fen.decode_fen, argmaxs) # type: ignore

def metrics(sample_logits: Float[Tensor, 'L 64*13'], true_fens: Sequence[str]) -> fen.Metrics:
  pred_fens = argmax_fens(sample_logits)
  return fen.metrics(fen_labs=true_fens, fen_preds=pred_fens[0])

class Metrics(TypedDict):
  acc: float
  intra_acc: float
  seq_acc: float
  consecutive_correct: float
  pre_mask_acc: NotRequired[float]
  post_mask_acc: NotRequired[float]

def pt_metrics(
  y_pred: Int[Tensor, 'B L 64'], y_true: Int[Tensor, 'B L 64'],
  *, ignore_idx: int = -100, first_masks: Int[Tensor, 'B L'] | None = None
) -> Metrics:
  y_pred = y_pred.clone()
  y_pred[y_true == ignore_idx] = ignore_idx
  consecutive_mean = float(np.mean([consecutive_eq(p, l) for p, l in zip(y_pred, y_true)]))
  
  out = Metrics(
    acc=accuracy(y_pred, y_true).item(),
    intra_acc=intra_accuracy(y_pred, y_true).item(),
    seq_acc=consecutive_mean / y_true.size(1),
    consecutive_correct=consecutive_mean,
  )
  
  if first_masks is not None:
    pre_acc = pre_bound_accuracy(y_pred, y_true, bounds=first_masks)
    if pre_acc is not None:
      out['pre_mask_acc'] = pre_acc.item()
    post_acc =  post_bound_accuracy(y_pred, y_true, bounds=first_masks)
    if post_acc is not None:
      out['post_mask_acc'] = post_acc.item()

  return out