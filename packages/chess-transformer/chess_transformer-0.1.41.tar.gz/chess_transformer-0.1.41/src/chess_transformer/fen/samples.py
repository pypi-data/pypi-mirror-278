from typing import NamedTuple, Sequence
from ..vocab import Vocabulary
from ._labels import labels, Label

class Sample(NamedTuple):
  input_ids: Sequence[int]
  labs: Sequence[Label]

def parse_sample(
  inputs: str, fens: str, *,
  vocab: Vocabulary
) -> Sample:
	clean_inputs = inputs.strip('\n').replace('+', '').replace('#', '').split(' ')
	input_ids = [vocab[inp] for inp in clean_inputs]
	labs = labels(fens.strip('\n').split(' '))
	return Sample(input_ids, labs)