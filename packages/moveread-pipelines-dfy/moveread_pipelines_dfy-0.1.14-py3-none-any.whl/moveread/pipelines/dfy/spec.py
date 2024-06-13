from typing import Sequence, Literal
from pydantic import BaseModel
from haskellian import Iter
from pipeteer import Pipeline, Workflow, Stateful
from scoresheet_models import ModelID
from chess_pairings import GameId, gameId
import moveread.pipelines.input_validation as inpval
import moveread.pipelines.preprocess as prep
import moveread.pipelines.game_preprocess as gamepre
import moveread.pipelines.ocr_predict as ocr
import moveread.pipelines.game_correction as gamecorr

Inputval = inpval.Pipeline
Preprocess = gamepre.Workflow
Ocr = ocr.Pipeline
Gamecorr = gamecorr.Pipeline

class BaseInput(BaseModel):
  title: str
  gameId: GameId
  model: ModelID
  imgs: Sequence[str]

  def preprocess(self, preprocessed_imgs: Sequence[prep.Result]) -> 'Preprocessed':
    ply_boxes = Iter(preprocessed_imgs) \
      .flatmap(lambda img: img.boxes) \
      .map(lambda box: [box]) \
      .sync() # OCR expects multiple boxes per ply
    return Preprocessed(preprocessed_imgs=preprocessed_imgs, gameId=self.gameId, model=self.model, imgs=self.imgs, ply_boxes=ply_boxes, title=self.title)

class Input(BaseInput):
  state: Literal['input'] = 'input'
  def pre(self) -> inpval.Input:
    return inpval.Input(gameId=self.gameId, imgs=self.imgs)


class PreprocessInput(BaseInput):
  state: Literal['preprocess'] = 'preprocess'

  @classmethod
  def post(cls, state: 'Input', result: inpval.Result) -> 'PreprocessInput':
    gid = gameId(state.gameId['tournId'], **result.gameId)
    title = state.title if gid == state.gameId else f'Changed to: {gid["group"]}/{gid["round"]}/{gid["board"]} from'
    return PreprocessInput(gameId=gid, model=state.model, imgs=result.imgs, title=title)

  def pre(self) -> gamepre.Input:
    return gamepre.Input(model=self.model, imgs=self.imgs)

class BasePreprocessed(BaseInput):
  ply_boxes: Sequence[Sequence[str]]
  preprocessed_imgs: Sequence[prep.Result]

class Preprocessed(BasePreprocessed):
  state: Literal['preprocessed'] = 'preprocessed'
  @classmethod
  def post(cls, state: PreprocessInput, result: gamepre.Result) -> 'Preprocessed':
    return state.preprocess(result.preprocessed_imgs)

  def pre(self) -> 'ocr.Input':
    return ocr.Input(ply_boxes=self.ply_boxes)

  def predict(self, ocrpreds: ocr.Preds) -> 'Predicted':
    return Predicted(ocrpreds=ocrpreds, gameId=self.gameId, model=self.model, imgs=self.imgs, preprocessed_imgs=self.preprocessed_imgs, ply_boxes=self.ply_boxes, title=self.title)

class BasePredicted(BasePreprocessed):
  ocrpreds: ocr.Preds

class Predicted(BasePredicted):
  state: Literal['predicted'] = 'predicted' # type: ignore

  @classmethod
  def post(cls, state: Preprocessed, result: ocr.Preds) -> 'Predicted':
    return state.predict(result)

  def pre(self) -> 'gamecorr.Input':
    return gamecorr.Input(ply_boxes=self.ply_boxes, ocrpreds=self.ocrpreds, title=self.title)

  def correct(self, res: gamecorr.CorrectResult) -> 'Result':
    return Result(
      ocrpreds=self.ocrpreds, gameId=self.gameId, model=self.model,
      imgs=self.imgs, preprocessed_imgs=self.preprocessed_imgs, ply_boxes=self.ply_boxes,
      annotations=res.annotations, pgn=res.pgn, early=res.early, title=self.title
    )

State = Input | Preprocessed | Predicted

class Result(BasePredicted, gamecorr.CorrectResult):
  
  @classmethod
  def post(cls, state: Predicted, result: gamecorr.Result) -> 'Result | Input':
    if result.root.tag == 'correct':
      return state.correct(result.root)
    else:
      return Input(gameId=state.gameId, model=state.model, imgs=state.imgs, title=state.title)

workflow = Workflow(
  'inputval', Result,
  pipelines=dict(
    inputval=Stateful(Input, [PreprocessInput], inpval.pipeline, Input.pre, PreprocessInput.post),
    preprocess=Stateful(PreprocessInput, [Preprocessed], gamepre.workflow, PreprocessInput.pre, Preprocessed.post),
    ocr=Stateful(Preprocessed, [Predicted], ocr.pipeline, Preprocessed.pre, Predicted.post),
    gamecorr=Stateful(Predicted, [Result, Input], gamecorr.pipeline, Predicted.pre, Result.post),
  )
)

def codegen():
  workflow.codegen(__file__, overwrite=True)