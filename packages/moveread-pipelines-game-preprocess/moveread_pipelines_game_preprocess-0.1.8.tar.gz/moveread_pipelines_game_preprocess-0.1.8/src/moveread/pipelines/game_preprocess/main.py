from typing_extensions import Unpack, NotRequired, TypedDict, Mapping
from dslog import Logger
from kv.api import KV
import moveread.pipelines.preprocess as pre
from .spec import Game
from .spec_codegen import Workflow
from .pipelines import preinput, join

class Params(TypedDict):
  games: KV[Game]
  imgGameIds: KV[str]
  received_imgs: KV[Mapping[str, pre.Result]]
  images: KV[bytes]
  images_path: NotRequired[str | None]

class Artifacts(pre.Artifacts):
  ...

def artifacts(**queues: Unpack[Workflow.InternalQueues]):
  
  def _bound(
    *, logger: Logger = Logger.click().prefix('[GAME PREPROCESS]'),
    images: KV[bytes], images_path: str | None = None,
    games: KV[Game], imgGameIds: KV[str],
    received_imgs: KV[Mapping[str, pre.Result]]
  ) -> Artifacts:
    
    artifacts = pre.Workflow.artifacts(**queues['preprocess']['internal'])(
      logger=logger.prefix('[PREPROCESS]'), images=images,
      images_path=images_path
    )

    artifacts.processes = { f'preprocess-{id}': ps for id, ps in artifacts.processes.items() }

    artifacts.processes['preinput'] = preinput(
      logger=logger.prefix('[PREINPUT]'), games=games, imgGameIds=imgGameIds,
      **queues['preinput']
    )

    artifacts.processes['join'] = join(
      logger=logger.prefix('[JOIN]'), games=games, imgGameIds=imgGameIds,
      received_imgs=received_imgs, **queues['join']
    )

    return Artifacts(processes=artifacts.processes, api=artifacts.api)
  
  return _bound