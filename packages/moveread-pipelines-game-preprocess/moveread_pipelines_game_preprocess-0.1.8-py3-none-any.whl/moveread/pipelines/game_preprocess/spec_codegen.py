from typing import Unpack, TypedDict
from q.api import WriteQueue, ReadQueue, Queue
from pipeteer import MakeQueue, make_queues as _make_queues, PipelineQueues
from .spec import Result, workflow, Input, Preprocess, PreInput, PreResult

class PreinputPipeline:
  In = Input
  Out = PreInput
  QueueIn = ReadQueue[Input]
  QueueOut = WriteQueue[PreInput]
  Queues = PipelineQueues[Input, PreInput]

class JoinPipeline:
  In = PreResult
  Out = Result
  QueueIn = ReadQueue[PreResult]
  QueueOut = WriteQueue[Result]
  Queues = PipelineQueues[PreResult, Result]



class Workflow:
  class InternalQueues(TypedDict):
    preprocess: Preprocess.Queues
    preinput: PreinputPipeline.Queues  
    join: JoinPipeline.Queues  

  class Queues(TypedDict):
    Qin: Queue[Input]
    internal: 'Workflow.InternalQueues'

  @staticmethod
  def make_queues(make_queue: MakeQueue, output_queue: WriteQueue[Result]) -> Queues:
    return _make_queues(workflow, make_queue, output_queue) # type: ignore
  
  @staticmethod
  def artifacts(**queues: Unpack['Workflow.InternalQueues']):
    from .main import artifacts
    return artifacts(**queues)
    