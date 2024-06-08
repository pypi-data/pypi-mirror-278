from typing import Sequence, TypedDict
import numpy as np
from haskellian import dicts as D
from ..metrics import accuracy, seq_accuracy, correct_count

class Metrics(TypedDict):
  acc: float
  seq_acc: float
  correct_len: int
  # fen_accs: Sequence[float]
  """Accuracy within each FEN (i.e. proportion of correct squares)"""

def metrics(*, fen_preds: Sequence[str], fen_labs: Sequence[str]) -> Metrics:
  return Metrics(
    acc=accuracy(labs=fen_labs, preds=fen_preds),
    seq_acc=seq_accuracy(labs=fen_labs, preds=fen_preds),
    correct_len=correct_count(labs=fen_labs, preds=fen_preds),
    # fen_accs=[accuracy(labs=l, preds=p) for l, p in zip(fen_labs, fen_preds)]
  )

def batch_metrics(*, fen_preds: Sequence[Sequence[str]], fen_labs: Sequence[Sequence[str]]) -> Metrics:
  sample_metrics = [metrics(fen_labs=labs, fen_preds=preds) for labs, preds in zip(fen_labs, fen_preds)]
  return D.aggregate(np.mean, sample_metrics) # type: ignore
