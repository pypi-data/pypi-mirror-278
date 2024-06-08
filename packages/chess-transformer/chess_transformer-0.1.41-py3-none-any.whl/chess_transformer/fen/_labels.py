from typing import Sequence, TypeAlias, Iterable
from haskellian import iter as I

piece_symbols = [None, 'P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
symbol_ids = { symbol: i for i, symbol in enumerate(piece_symbols) }

Label: TypeAlias = Sequence[int]

def parse_fen(board_fen: str) -> Label:
  output = []
  for row in board_fen.split(' ')[0].split('/'):
    for sq in row:
      if sq.isdigit():
        output.extend([0] * int(sq))
      else:
        output.append(symbol_ids[sq])
  return output

def decode_symbols(encoded_pos: Sequence[int]) -> Sequence[Sequence[str | None]]:
  return [
    [piece_symbols[code] for code in row]
    for row in I.batch(8, encoded_pos)
  ]

def merge_empties(row: Sequence[str | None]) -> Iterable[str]:
  spaces = 0
  for piece in row:
    if piece is None:
      spaces += 1
    else:
      if spaces > 0:
        yield str(spaces)
        spaces = 0
      yield piece
  if spaces > 0:
    yield str(spaces)

def decode_fen(pred: Sequence[int]) -> str:
  symbols = decode_symbols(pred)
  return '/'.join(
    ''.join(merge_empties(row))
    for row in symbols
  )

def viz_fen(pred: Sequence[int]) -> str:
  symbols = decode_symbols(pred)
  return '/'.join(
    ''.join((c or '.') for c in row)
    for row in symbols
  )

def labels(fens: Iterable[str]) -> Sequence[Label]:
  return [parse_fen(fen) for fen in fens]