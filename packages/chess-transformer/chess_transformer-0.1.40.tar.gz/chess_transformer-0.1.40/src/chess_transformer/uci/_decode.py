from typing import Iterable
import chess

def decode_ucis(ucis: Iterable[str]) -> Iterable[str]:
  """Parses UCIs that may always have promotion to SANs. Ignores promotion if not needed"""
  board = chess.Board()
  for uci in ucis:
    try:
      move = chess.Move.from_uci(uci[:4])
      if not board.is_legal(move):
        move = chess.Move.from_uci(uci)
        if not board.is_legal(move):
          return
        
      yield board.san(move)
      board.push(move)

    except chess.InvalidMoveError:
      return