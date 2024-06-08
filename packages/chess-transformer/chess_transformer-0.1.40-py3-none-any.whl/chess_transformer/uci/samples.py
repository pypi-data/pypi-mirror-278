from typing import NamedTuple, Sequence
import chess_utils as cu
from ..vocab import Vocabulary
from ._labels import labels, Label

class Sample(NamedTuple):
  input_ids: Sequence[int]
  labs: Sequence[Label]

def parse_sample(
  inputs: str, ucis: str | None = None, *,
  vocab: Vocabulary, ignore_idx: int = -100
) -> Sample:
	sans = inputs.strip('\n').replace('+', '').replace('#', '').split(' ')
	input_ids = [vocab[san] for san in sans]
	parsed_ucis = cu.sans2ucis(sans) if ucis is None else ucis.strip('\n').split(' ')
	labs = labels(parsed_ucis, ignore_idx=ignore_idx)
	return Sample(input_ids, labs)