from typing import TypedDict, Sequence
import chess_utils as cu
from ..vocab import Vocabulary
from .. import fen, uci

class Sample(TypedDict):
  input_ids: Sequence[int]
  ucis: Sequence[uci.Label]
  fens: Sequence[fen.Label]

def parse_sample(
  inputs: str, ucis: str | None = None, fens: str | None = None, *,
  vocab: Vocabulary, ignore_idx: int = -100
) -> Sample:
  sans = inputs.strip().replace('+', '').replace('#', '').split()
  input_ids = [vocab[san] for san in sans]
  parsed_ucis = cu.sans2ucis(sans) if ucis is None else ucis.strip().split()
  uci_labs = uci.labels(parsed_ucis, ignore_idx=ignore_idx)
  parsed_fens = cu.sans2fens(sans) if fens is None else fens.strip().split()
  fen_labs = fen.labels(parsed_fens)
  return Sample(input_ids=input_ids, ucis=uci_labs, fens=fen_labs)