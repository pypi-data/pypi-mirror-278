from typing import Literal, Mapping, TypeAlias, Iterable, Sequence
import chess_notation as cn
from .sans import legal_sans, sort_key

SpecialToken: TypeAlias = Literal['[PAD]', '[CLS]', '[SEP]', '[MASK]']
PAD: TypeAlias = Literal['[PAD]']
MASK: TypeAlias = Literal['[MASK]']
Vocabulary: TypeAlias = Mapping[str | SpecialToken, int]

def remove_symbols(san: str) -> str:
  """Remove check and mate symbols from a SAN move"""
  return san.replace('+', '').replace('#', '')

def make_vocab(words: Iterable[str]) -> Vocabulary:
  return { word: i for i, word in enumerate(words) }

def legal(
  with_symbols: bool = False, *,
  with_full_discriminators: bool = True,
  pre_tokens: Sequence[str] = ['[PAD]'],
  post_tokens: Sequence[str] = [],
) -> Vocabulary:
  """Vocabulary containing all legal SAN moves
  - `with_symbols`: whether to include `+` and `#` (triples the size of the vocabulary, though)
  """
  legals = legal_sans(with_symbols=with_symbols, with_full_discriminators=with_full_discriminators)
  return make_vocab(list(pre_tokens) + legals + list(post_tokens))

def invert(vocab: Vocabulary) -> Mapping[int, str]:
  return { i: word for word, i in vocab.items() }

default_motions = cn.MotionStyles(castles=[], pawn_captures=cn.UNIQ_PAWN_CAPTURES, piece_captures=cn.UNIQ_PIECE_CAPTURES)

def legal_styled(
  with_symbols: bool = False, *,
  with_full_discriminators: bool = True,
  motions: cn.MotionStyles = default_motions,
  effects: cn.KingEffectStyles = cn.KingEffectStyles(),
  languages: Sequence[cn.Language] = cn.LANGUAGES,
  special_tokens: Sequence[str] = ['[PAD]', '[UNK]'],
) -> Vocabulary:
  """All legal sans, styled. Size 60953 with default parameters
  - Legal SANs come first, then all representations
  """
  legal = legal_sans(with_symbols=with_symbols, with_full_discriminators=with_full_discriminators)
  words = set()
  for san in legal:
    words |= cn.all_representations(san, motions=motions, effects=effects, languages=languages)
  new_words = words - set(legal)
  sorted_words = sorted(new_words, key=sort_key)
  return make_vocab(list(special_tokens) + legal + sorted_words)
  

def extend_styled(vocab: Vocabulary, *, with_symbols: bool = False, with_full_discriminators: bool = True) -> Vocabulary:
  """Add 'dxe' mapping to 'de' and 'de4' mapping to 'dxe4'"""
  new_vocab = dict(vocab).copy()
  legals = legal_sans(with_symbols=with_symbols, with_full_discriminators=False) # pawn captures can't have full discriminators
  for word in legals:
    if cn.styles.is_pawn_capture(word):
      de = cn.styles.pawn_capture(word, 'de')
      dxe = cn.styles.pawn_capture(word, 'dxe')
      de4 = cn.styles.pawn_capture(word, 'de4')
      dxe4 = cn.styles.pawn_capture(word, 'dxe4')
      new_vocab[dxe] = new_vocab[de]
      new_vocab[de4] = new_vocab[dxe4]

  return new_vocab