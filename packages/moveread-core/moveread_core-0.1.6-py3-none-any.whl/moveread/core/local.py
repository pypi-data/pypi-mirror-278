import os
from .core import CoreAPI, Game
try:
  from kv.sqlite import SQLiteKV
  from kv.fs import FilesystemKV
except ImportError as e:
      raise ImportError('Install `moveread-core[local]` to run locally', e)

def LocalAPI(path: str, blobs_extension: str | None = None) -> CoreAPI:
  return CoreAPI(
    games=SQLiteKV.validated(Game, os.path.join(path, 'games.sqlite'), table='games'),
    blobs=FilesystemKV[bytes](os.path.join(path, 'blobs'), extension=blobs_extension)
  )

def DebugAPI(path: str, blobs_extension: str | None = None) -> CoreAPI:
  return CoreAPI(
    games=FilesystemKV.validated(Game, os.path.join(path, 'games')),
    blobs=FilesystemKV[bytes](os.path.join(path, 'blobs'), extension=blobs_extension)
  )