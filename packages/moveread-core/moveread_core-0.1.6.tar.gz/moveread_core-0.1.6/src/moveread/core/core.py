import re
from typing import Sequence, TypeVar, Literal
from dataclasses import dataclass
from kv.api import KV, ReadError
from haskellian import either as E, promise as P, Left, Right
from .models import Game

T = TypeVar('T')

@dataclass
class CoreAPI:

  games: KV[Game]
  blobs: KV[bytes]

  @classmethod
  def of(cls, games_conn_str: str, blobs_conn_str: str) -> 'CoreAPI':
    return cls(KV.of(games_conn_str, Game), KV[bytes].of(blobs_conn_str))

  @classmethod
  def at(cls, path: str, blobs_extension: str | None = None) -> 'CoreAPI':
    from .local import LocalAPI
    return LocalAPI(path, blobs_extension)
  
  @classmethod
  def debug(cls, path: str, blobs_extension: str | None = None) -> 'CoreAPI':
    from .local import DebugAPI
    return DebugAPI(path, blobs_extension)

  @E.do[ReadError]()
  async def copy(self, fromId: str, other: 'CoreAPI', toId: str, *, overwrite: bool = False) -> None:
    game = (await self.games.read(fromId)).unsafe()

    if not overwrite:
      tasks = [other.blobs.has(img.url) for _, img in game.images]
      results = E.sequence(await P.all(tasks)).unsafe()
      if any(results):
        Left(ExistentBlobs([img.url for (_, img), exists in zip(game.images, results) if exists])).unsafe()

    if (await other.games.has(toId)).unsafe():
      Left(ExistentGame()).unsafe()

    img_tasks = [self.blobs.copy(img.url, other.blobs, img.url) for _, img in game.images]
    E.sequence(await P.all(img_tasks)).unsafe()
    (await other.games.insert(toId, game)).unsafe()

@dataclass
class ExistentBlobs:
  blobs: Sequence[str]
  reason: Literal['existent-blobs'] = 'existent-blobs'

@dataclass
class ExistentGame:
  reason: Literal['existent-game'] = 'existent-game'