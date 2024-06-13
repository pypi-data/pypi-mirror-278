from typing import Sequence, NamedTuple
from haskellian import iter as I, either as E, promise as P
from kv.api import KV, ReadError
from scoresheet_models import ModelID
from moveread.core import CoreAPI, Game, GameMeta, Player, Sheet, PlayerMeta, SheetMeta, Image
from moveread.pipelines.preprocess import Result as PreprocessResult
from moveread.annotations import Tournament, StylesNA
from ..spec import Result

def output_sheet(preprocessed: PreprocessResult, model: ModelID, tournId: str) -> tuple[Sheet, Sequence[str]]:
  og = preprocessed.original
  corr = preprocessed.corrected
  images = [
    Image(url=f'{tournId}/{og.img}', meta=og.meta),
    Image(url=f'{tournId}/{corr.img}', meta=corr.meta),
  ]
  return Sheet(images=images, meta=SheetMeta(model=model)), [og.img, corr.img]

class Output(NamedTuple):
  game: Game
  images: Sequence[str]

def output_game(key: str, result: Result) -> Output:
  ann = result.annotations[0]
  styles = StylesNA(pawn_capture=ann.pawn_capture, piece_capture=ann.piece_capture)
  tournId = result.gameId['tournId']
  sheets, nested_imgs = I.unzip(output_sheet(img, result.model, tournId) for img in result.preprocessed_imgs)
  imgs = I.flatten(nested_imgs).sync()

  game = Game(
    id=f'{tournId}/{key}',
    meta=GameMeta(pgn=result.pgn, early=result.early, tournament=Tournament(**result.gameId)),
    players=[Player(
      meta=PlayerMeta(language=ann.lang, end_correct=ann.end_correct, styles=styles),
      sheets=sheets
    )]
  )

  return Output(game, imgs)

@E.do[ReadError]()
async def output_one(
  core: CoreAPI, key: str, result: Result, *, images: KV[bytes]
):
  game, imgs = output_game(key, result)
  tournId = result.gameId['tournId']
  tasks = [images.copy(url, core.blobs, f'{tournId}/{url}') for url in imgs]
  E.sequence(await P.all(tasks)).unsafe()
  (await core.games.insert(game.id, game)).unsafe()