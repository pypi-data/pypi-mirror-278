from jaxtyping import Int
from typing import Mapping
from torch import nn, Tensor
from transformers import GPT2Config, GPT2Model

class ChessGPT2(nn.Module):
  def __init__(
    self, *, vocab_size: int, max_len: int = 512,
    hidden_size: int = 768, attention_heads: int = 12,
    pad_token_id: int, heads: Mapping[str, int] = { 'uci': 36, 'fen': 64*13 }
  ):
    super().__init__()
    self.config = GPT2Config(
      vocab_size=vocab_size,
      max_position_embeddings=max_len,
      hidden_size=hidden_size,
      num_attention_heads=attention_heads,
      pad_token_id=pad_token_id
    )
    self.gpt = GPT2Model(self.config)
    self.heads = nn.ModuleDict({
      head: nn.Linear(hidden_size, num_classes)
      for head, num_classes in heads.items()
    })

  def forward(
    self, input_ids: Int[Tensor, 'batch maxlen'],
    *, attention_mask: Int[Tensor, 'batch maxlen'] | None = None
  ):
    # Get BERT outputs
    outputs = self.gpt(input_ids=input_ids, attention_mask=attention_mask)
    sequence_output = outputs.last_hidden_state  # Shape: (batch_size, seq_len, hidden_size)
    return { head: self.heads[head](sequence_output) for head in self.heads }