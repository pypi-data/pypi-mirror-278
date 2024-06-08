from jaxtyping import Int
from torch import nn, Tensor
from transformers import T5Config, T5Model

class ChessT5(nn.Module):
  def __init__(
    self, *, vocab_size: int, max_len: int = 512,
    hidden_size: int = 256, attention_heads: int = 4,
    pad_token_id: int = 0
  ):
    super().__init__()
    # BERT configuration
    self.config = T5Config(
      vocab_size=vocab_size,
      max_position_embeddings=max_len,
      hidden_size=hidden_size,
      num_attention_heads=attention_heads,
      pad_token_id=pad_token_id
    )
    self.t5 = T5Model(self.config)
    self.fc = nn.Linear(hidden_size, 4 * 8 + 4)

  def forward(self, input_ids: Int[Tensor, 'batch maxlen']):
    # Get BERT outputs
    outputs = self.t5(input_ids=input_ids, decoder_input_ids=input_ids)
    sequence_output = outputs.last_hidden_state  # Shape: (batch_size, seq_len, hidden_size)
    return self.fc(sequence_output)  # Shape: (batch_size, seq_len, 4 * 8 + 4 = 36)