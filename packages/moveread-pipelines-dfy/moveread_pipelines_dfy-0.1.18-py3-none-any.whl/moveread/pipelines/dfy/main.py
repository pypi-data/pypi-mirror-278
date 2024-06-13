from typing import Unpack, Mapping, Coroutine, NotRequired
import os
from dataclasses import dataclass
from dslog import Logger
from haskellian import kwargs as kw
from fastapi import FastAPI
import tf.serving as tfs
import moveread.pipelines.input_validation as inpval
import moveread.pipelines.game_preprocess as gamepre
import moveread.pipelines.ocr_predict as ocr
import moveread.pipelines.game_correction as gamecorr
from .spec_codegen import Workflow

@dataclass
class Artifacts:
  api: FastAPI
  processes: Mapping[str, Coroutine[None, None, None]]

class Params(gamepre.Params):
  tfserving: NotRequired[tfs.Params]
  token: NotRequired[str]

def artifacts(**queues: Unpack[Workflow.InternalQueues]):

  def _bound(logger = Logger.click().prefix('[DFY]'), **params: Unpack[Params]):

    inpval_api = inpval.Pipeline.artifacts(**queues['inputval']['internal'])(logger=logger.prefix('[INPUT VAL]'), images_path=params.get('images_path'))

    gamepre_params = kw.take(gamepre.Params, params)
    gamepre_artifs = gamepre.Workflow.artifacts(**queues['preprocess']['internal']['internal'])(logger=logger.prefix('[GAME PREPROCESS]'), **gamepre_params)

    run_ocr = ocr.Pipeline.artifacts(**queues['ocr']['internal'])(logger=logger.prefix('[OCR PREDICT]'), images=params['images'], **params.get('tfserving', {}))
    
    gamecorr_api = gamecorr.Pipeline.artifacts(**queues['gamecorr']['internal'])(logger=logger.prefix('[GAME CORRECTION]'), images_path=params.get('images_path'))

    api = FastAPI()

    api.mount('/inputval', inpval_api)
    api.mount('/preprocess', gamepre_artifs.api)
    api.mount('/gamecorr', gamecorr_api)

    images_path = params.get('images_path')
    if images_path is not None:
      from fastapi.staticfiles import StaticFiles
      api.mount('/images', StaticFiles(directory=images_path))

    return Artifacts(
      api=api, processes={
        f'preprocess-{id}': proc
        for id, proc in gamepre_artifs.processes.items()
      } | { 'ocr': run_ocr }
    )
  
  return _bound