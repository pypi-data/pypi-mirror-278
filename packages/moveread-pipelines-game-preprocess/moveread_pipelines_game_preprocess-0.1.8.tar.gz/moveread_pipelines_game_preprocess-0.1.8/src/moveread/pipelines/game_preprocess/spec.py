from typing import Sequence
from pydantic import BaseModel
from pipeteer import Pipeline, Workflow
from scoresheet_models import ModelID
import moveread.pipelines.preprocess as pre
Preprocess = pre.Workflow

PreInput = pre.Input
PreInput.__name__ = 'PreInput'

PreResult = pre.Result
PreResult.__name__ = 'PreResult'

class Input(BaseModel):
  model: ModelID 
  imgs: Sequence[str]

class Game(BaseModel):
  model: ModelID
  imgIds: Sequence[str]

class Result(BaseModel):
  preprocessed_imgs: Sequence[PreResult]

workflow = Workflow[Input, Result](
  'preinput', Result,
  pipelines=dict(
    preinput=Pipeline(Input, PreInput),
    preprocess=pre.workflow,
    join=Pipeline(PreResult, Result)
  )
)

def codegen():
  workflow.codegen(__file__, overwrite=True)
