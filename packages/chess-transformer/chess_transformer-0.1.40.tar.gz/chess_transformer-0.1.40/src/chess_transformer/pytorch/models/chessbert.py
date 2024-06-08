from typing import Mapping
from jaxtyping import Int
import torch
from torch import nn, Tensor
from transformers import BertConfig, BertModel

class ChessBert(nn.Module):
  def __init__(
    self, *, vocab_size: int, max_len: int = 512,
    hidden_size: int = 768, attention_heads: int = 12,
    pad_token_id: int, heads: Mapping[str, int] = { 'uci': 36, 'fen': 64*13 }
  ):
    super().__init__()
    # BERT configuration
    self.config = BertConfig(
      vocab_size=vocab_size,
      max_position_embeddings=max_len,
      hidden_size=hidden_size,
      num_attention_heads=attention_heads,
      pad_token_id=pad_token_id
    )
    self.bert = BertModel(self.config)
    self.heads = nn.ModuleDict({
      head: nn.Linear(hidden_size, num_classes)
      for head, num_classes in heads.items()
    })

  def forward(
    self, input_ids: Int[Tensor, 'batch maxlen'],
    *, attention_mask: Int[Tensor, 'batch maxlen'] | None = None
  ):
    # Get BERT outputs
    outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
    sequence_output = outputs.last_hidden_state  # Shape: (batch_size, seq_len, hidden_size)
    return { head: self.heads[head](sequence_output) for head in self.heads }
  

  def insert_token(self, idx: int):
    """Insert new token in the model's vocabulary, at the given `idx`"""
    config = self.config
    new_vocab_size = config.vocab_size + 1
    new_word_embed = nn.Embedding(new_vocab_size, config.hidden_size, padding_idx=config.pad_token_id)
    old_embed = self.bert.embeddings.word_embeddings.weight
    with torch.no_grad():
      new_word_embed.weight[:idx] = old_embed[:idx]
      new_word_embed.weight[idx] = torch.mean(old_embed, dim=0)
      new_word_embed.weight[idx+1:] = old_embed[idx:]
    
    config.vocab_size = new_vocab_size
    self.config = config
    self.bert.embeddings.word_embeddings = new_word_embed

  def append_token(self):
    """Append new token in the model's vocabulary"""
    self.insert_token(self.config.vocab_size-1)