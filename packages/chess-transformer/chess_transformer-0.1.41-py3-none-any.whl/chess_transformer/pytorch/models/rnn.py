from typing import Mapping, Sequence
from jaxtyping import Int
from torch import nn, Tensor
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class ChessRNN(nn.Module):
  def __init__(
    self, *, vocab_size: int, embed_size: int = 256,
    hidden_sizes: Sequence[int] = [256, 512, 256],
    heads: Mapping[str, int] = { 'uci': 36, 'fen': 64*13 }
  ):
    super().__init__()
    self.embed = nn.Embedding(vocab_size, embed_size)
    self.bi_lstms = nn.ModuleList([
      nn.LSTM(input_size=embed_size if i == 0 else 2*hidden_sizes[i-1], hidden_size=hidden_sizes[i], bidirectional=True)
      for i in range(len(hidden_sizes))
    ])
    self.heads = nn.ModuleDict({
      head: nn.Linear(2*hidden_sizes[-1], num_classes)
      for head, num_classes in heads.items()
    })

  def forward(self, input_ids: Int[Tensor, 'batch maxlen'], seq_lens: Sequence[int]):
    x = self.embed(input_ids)
    packed = pack_padded_sequence(x, seq_lens, batch_first=True, enforce_sorted=False) # type: ignore
    for lstm in self.bi_lstms:
      packed, _ = lstm(packed)
    z = pad_packed_sequence(packed, batch_first=True)[0]
    return { k: head(z) for k, head in self.heads.items() }