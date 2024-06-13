from asyncio import queues
from typing import Sequence, NamedTuple, Mapping
import os
from kv.fs import FilesystemKV
from kv.sqlite import SQLiteKV
from q.kv import QueueKV
import moveread.pipelines.preprocess as pre
from moveread.pipelines.game_preprocess import Game
from .spec import Result
from .main import Params
from .spec_codegen import Workflow

def local_queues(base_path: str, queues_relpath: str = 'queues.sqlite') -> Workflow.Queues:
  queues_path = os.path.join(base_path, queues_relpath)
  def make_queue(path: Sequence[str], type: type):
    return QueueKV.sqlite(type, queues_path, table='-'.join(path))
  
  Qout = make_queue(['output'], Result)
  return Workflow.make_queues(make_queue, Qout)

def local_storage(
  base_path: str, *,
  db_relpath: str = 'data.sqlite',
  images_relpath: str = 'images',
) -> Params:
  """Scaffold local storage for the DFY pipeline."""

  db_path = os.path.join(base_path, db_relpath)
  images_path = os.path.join(base_path, images_relpath)
  params = Params(
    images=FilesystemKV[bytes](images_path),
    games=SQLiteKV.validated(Game, db_path, 'games'),
    imgGameIds=SQLiteKV.at(db_path, 'game-ids'),
    received_imgs=SQLiteKV.validated(Mapping[str, pre.Result], db_path, 'received-imgs'),
    images_path=images_path,
  )

  return params