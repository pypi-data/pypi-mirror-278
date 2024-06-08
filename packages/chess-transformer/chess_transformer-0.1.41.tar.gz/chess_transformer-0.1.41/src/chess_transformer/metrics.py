from typing import Iterable, Sequence, TypeVar
from itertools import zip_longest

A = TypeVar('A')

def accuracy(*, preds: Iterable[A], labs: Sequence[A]) -> float:
  return sum(1 for lab, pred in zip(labs, preds) if lab == pred) / len(labs)

def seq_accuracy(*, preds: Iterable[Sequence[A]], labs: Sequence[Sequence[A]]) -> float:
  for i, (lab, pred) in enumerate(zip_longest(labs, preds)):
    if lab != pred:
      return i / len(labs)
  return 1.0

def correct_count(*, preds: Iterable[A], labs: Iterable[A]) -> int:
  count = 0
  for p, l in zip(preds, labs):
    if p != l:
      break
    count += 1
  return count