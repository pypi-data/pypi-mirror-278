from typing import Sequence, TypedDict
import numpy as np
from haskellian import dicts as D
from ..metrics import accuracy, seq_accuracy, correct_count

class Metrics(TypedDict):
  acc: float
  seq_acc: float
  correct_len: int
  from_sq_acc: float
  to_sq_acc: float

def metrics(*, uci_preds: Sequence[str], uci_labs: Sequence[str]) -> Metrics:
  clean_preds = [p[:len(l)] for p, l in zip(uci_preds, uci_labs)]
  acc = accuracy(labs=uci_labs, preds=clean_preds)
  seq_acc = seq_accuracy(labs=uci_labs, preds=clean_preds)

  corr_len = correct_count(labs=uci_labs, preds=clean_preds)

  from_sq_preds = [p[0:2] for p in clean_preds]
  from_sq_labs = [l[0:2] for l in uci_labs]
  from_sq_acc = accuracy(labs=from_sq_labs, preds=from_sq_preds)

  to_sq_preds = [p[2:4] for p in clean_preds]
  to_sq_labs = [l[2:4] for l in uci_labs]
  to_sq_acc = accuracy(labs=to_sq_labs, preds=to_sq_preds)

  return Metrics(acc=acc, seq_acc=seq_acc, correct_len=corr_len, from_sq_acc=from_sq_acc, to_sq_acc=to_sq_acc)

def batch_metrics(*, uci_preds: Sequence[Sequence[str]], uci_labs: Sequence[Sequence[str]]) -> Metrics:
  sample_metrics = [metrics(uci_labs=labs, uci_preds=preds) for labs, preds in zip(uci_labs, uci_preds)]
  return D.aggregate(np.mean, sample_metrics) # type: ignore
