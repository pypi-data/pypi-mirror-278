from typing import TypeAlias, Iterable, Sequence, Literal

promotion_ids = dict(n=0, b=1, r=2, q=3)
def encode_promotion(piece: Literal['n', 'b', 'r', 'q']) -> int:
  return promotion_ids[piece]

def encode_uci(e2e4q: str, *, ignore_idx: int = -100) -> tuple[int, int, int, int, int]:
  from_file = ord(e2e4q[0]) - ord('a')
  from_rank = int(e2e4q[1]) - 1
  to_file = ord(e2e4q[2]) - ord('a')
  to_rank = int(e2e4q[3]) - 1
  promotion = encode_promotion(e2e4q[4]) if len(e2e4q) == 5 else ignore_idx # type: ignore
  return from_file, from_rank, to_file, to_rank, promotion

Label: TypeAlias = tuple[int, int, int, int, int]

def labels(ucis: Iterable[str], *, ignore_idx: int = -100) -> Sequence[Label]:
  """`ignore_idx`: used for promotion when none"""
  return [encode_uci(uci, ignore_idx=ignore_idx) for uci in ucis]


def decode_file(file: int):
  return chr(file + ord('a'))

def decode_rank(rank: int):
  return str(rank + 1)

def decode_promotion(promotion: int):
  for piece, idx in promotion_ids.items():
    if idx == promotion:
      return piece
  return 'q'

def decode_uci(from_file: int, from_rank: int, to_file: int, to_rank: int, promotion: int, *, ignore_idx: int = -100):
  ff = decode_file(from_file)
  fr = decode_rank(from_rank)
  tf = decode_file(to_file)
  tr = decode_rank(to_rank)
  prom = decode_promotion(promotion) if promotion != ignore_idx else ''
  return f'{ff}{fr}{tf}{tr}{prom}'

def decode(uci_labs: Iterable[Label], *, ignore_idx: int = -100) -> Sequence[str]:
  return [decode_uci(*uci, ignore_idx=ignore_idx) for uci in uci_labs]