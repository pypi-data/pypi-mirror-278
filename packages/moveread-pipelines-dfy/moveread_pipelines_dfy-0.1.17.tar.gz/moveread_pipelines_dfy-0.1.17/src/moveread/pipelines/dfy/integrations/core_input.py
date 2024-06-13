from typing import Callable
from uuid import uuid4
from kv.api import KV
from q.api import WriteQueue
from dslog import Logger
from scoresheet_models import ModelID
from chess_pairings import gameId
from moveread.core import CoreAPI, Game
from ..spec import Input, GameId

def makeId(game: Game) -> GameId:
  if game.meta is None or game.meta.tournament is None:
    return gameId('tournament', 'a', '1', '1')
  t = game.meta.tournament
  return gameId(t.tournId or 'tournament', t.group or 'a', t.round or '1', t.board or '1')

def make_title(game: Game) -> str:
  gid = makeId(game)
  return f'{gid["tournId"]}: {gid["group"]}/{gid["round"]}/{gid["board"]}'

async def input_core(
  core: CoreAPI, Qin: WriteQueue[Input],
  *, images: KV[bytes],
  model_fn: Callable[[Game], ModelID] = lambda *_: 'llobregat23',
  gameId_fn: Callable[[Game], GameId] = makeId,
  title_fn: Callable[[Game], str] = make_title,
  num_games: int | None = None, shuffle: bool = True,
  logger = Logger.rich().prefix('[CORE INPUT]')
):
  """Input all images from `core` into `Qin` tasks
  - Actually, only images with `version == 0`
  - `model_fn`: determines the scoresheet model of each task
  - `state_fn`: determines an arbitrary tuple of JSON-serializable data to attach to each task
  """
  games = list((await core.games.keys()).unsafe())
  if shuffle:
    import random
    random.shuffle(games)
  for gameId in games[:num_games]:
    game = (await core.games.read(gameId)).unsafe()
    imgs = []
    for imgId, image in game.images:
      if imgId.version == 0:
        id = str(imgId)
        url = f'{id}/original_{uuid4()}.jpg'
        img = (await core.blobs.read(image.url)).unsafe()
        (await images.insert(url, img)).unsafe()
        imgs.append(url)

    task = Input(title=make_title(game), model=model_fn(game), gameId=gameId_fn(game), imgs=imgs)
    await Qin.push(gameId, task)
    logger(f'Inputted task "{gameId}". Task:', task)