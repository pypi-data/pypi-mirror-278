from dataclasses import dataclass

@dataclass
class GameID:
  gameId: str

  def playerId(self, player: int = 0) -> 'PlayerID':
    return PlayerID(gameId=self.gameId, player=player)

@dataclass
class PlayerID(GameID):
  player: int

  def sheetId(self, page: int = 0) -> 'SheetID':
    return SheetID(gameId=self.gameId, player=self.player, page=page)
  
  def __str__(self):
    return f'{self.gameId}-{self.player}'

@dataclass
class SheetID(PlayerID):
  page: int

  def imageId(self, version: int = 0) -> 'ImageID':
    return ImageID(gameId=self.gameId, player=self.player, page=self.page, version=version)

  def __str__(self):
    return f'{self.gameId}-{self.player}-{self.page}'

@dataclass
class ImageID(SheetID):
  version: int = 0

  def boxId(self, idx: int) -> 'BoxID':
    return BoxID(gameId=self.gameId, player=self.player, page=self.page, version=self.version, idx=idx)
  
  def __str__(self):
    return f'{self.gameId}/{self.player}-{self.page}-{self.version}'

@dataclass
class BoxID(ImageID):
  idx: int = 0

ID = GameID | PlayerID | SheetID | ImageID | BoxID