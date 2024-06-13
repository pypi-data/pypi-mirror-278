from typing import Unpack, TypedDict
from q.api import WriteQueue, Queue
from pipeteer import MakeQueue, make_queues as _make_queues
from .spec import Preprocessed, PreprocessInput, Input, Result, Preprocess, Ocr, Predicted, Inputval, Gamecorr, workflow

class InputvalStateful:
  class Queues(TypedDict):
    Qin: Queue[Input]
    internal: 'Inputval.Queues'
    
class PreprocessStateful:
  class Queues(TypedDict):
    Qin: Queue[PreprocessInput]
    internal: 'Preprocess.Queues'
    
class OcrStateful:
  class Queues(TypedDict):
    Qin: Queue[Preprocessed]
    internal: 'Ocr.Queues'
    
class GamecorrStateful:
  class Queues(TypedDict):
    Qin: Queue[Predicted]
    internal: 'Gamecorr.Queues'
    

class Workflow:
  class InternalQueues(TypedDict):
    inputval: InputvalStateful.Queues
    preprocess: PreprocessStateful.Queues
    ocr: OcrStateful.Queues
    gamecorr: GamecorrStateful.Queues

  class Queues(TypedDict):
    Qin: WriteQueue[Input]
    internal: 'Workflow.InternalQueues'

  @staticmethod
  def make_queues(make_queue: MakeQueue, output_queue: WriteQueue[Result]) -> Queues:
    return _make_queues(workflow, make_queue, output_queue) # type: ignore
  
  @staticmethod
  def artifacts(**queues: Unpack['Workflow.InternalQueues']):
    from .main import artifacts
    return artifacts(**queues)
    