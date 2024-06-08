from typing import Sequence, Mapping
from jaxtyping import Float, Int
from torch import Tensor
from .. import uci, fen

def metrics(
  uci_logits: Float[Tensor, 'L 36'],
  fen_logits: Float[Tensor, 'L 64*13'],
  *,
  true_ucis: Sequence[str],
  true_fens: Sequence[str],
) -> Mapping[str, float]:
  return {
    f'uci-{k}': v for k, v in uci.metrics(uci_logits, true_ucis).items()
  } | {
    f'fen-{k}': v for k, v in fen.metrics(fen_logits, true_fens).items()
  } # type: ignore

def pt_metrics(
  uci_logits: Float[Tensor, 'B L 36'],
  fen_logits: Float[Tensor, 'B L 64*13'],
  *,
  true_ucis: Int[Tensor, 'B L 5'],
  true_fens: Int[Tensor, 'B L 64'],
  ignore_idx: int = -100,
  first_masks: Int[Tensor, 'B L'] | None = None
) -> Mapping[str, float]:
  uci_preds = uci.argmax_preds(uci_logits)
  fen_preds = fen.argmax_preds(fen_logits)
  return {
    f'uci-{k}': v for k, v in uci.pt_metrics(uci_preds, true_ucis, ignore_idx=ignore_idx, first_masks=first_masks).items()
  } | {
    f'fen-{k}': v for k, v in fen.pt_metrics(fen_preds, true_fens, ignore_idx=ignore_idx, first_masks=first_masks).items()
  } # type: ignore