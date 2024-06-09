from typing import Iterable
from pydantic import BaseModel, ConfigDict
from moveread.annotations import GameMeta, PlayerMeta, SheetMeta, ImageMeta
from .ids import SheetID, ImageID

class Box(BaseModel):
  model_config = ConfigDict(extra='forbid')
  url: str
  meta: dict | None = None

class Image(BaseModel):
  model_config = ConfigDict(extra='forbid')
  url: str
  boxes: list[Box] | None = None
  meta: ImageMeta | None = None

class Sheet(BaseModel):
  model_config = ConfigDict(extra='forbid')
  images: list[Image]
  meta: SheetMeta | None = None

class Player(BaseModel):
  model_config = ConfigDict(extra='forbid')
  sheets: list[Sheet]
  meta: PlayerMeta | None = None

class Game(BaseModel):
  model_config = ConfigDict(extra='forbid')
  id: str
  players: list[Player]
  meta: GameMeta | None = None

  @property
  def sheets(self) -> Iterable[tuple[SheetID, Sheet]]:
    for i, player in enumerate(self.players):
      for j, sheet in enumerate(player.sheets):
        yield SheetID(self.id, i, j), sheet

  @property
  def images(self) -> Iterable[tuple[ImageID, Image]]:
    for sheetId, sheet in self.sheets:
      for version, image in enumerate(sheet.images):
        yield sheetId.imageId(version), image
  