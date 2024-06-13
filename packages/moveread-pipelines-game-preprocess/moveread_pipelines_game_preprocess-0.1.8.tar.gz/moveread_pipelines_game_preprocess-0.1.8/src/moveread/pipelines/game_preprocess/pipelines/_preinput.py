import asyncio
from haskellian import either as E
from dslog import Logger
from kv.api import KV
from ..spec import Game, PreInput
from ..spec_codegen import PreinputPipeline as Preinput

async def preinput(
  Qin: Preinput.QueueIn, Qout: Preinput.QueueOut,
  *, games: KV[Game], imgGameIds: KV[str],
  logger = Logger.rich().prefix('[PREINPUT]')
):
  @E.do()
  async def input_one():
    gameId, task = (await Qin.read()).unsafe()
    imgIds = [f'{gameId}-{i}' for i in range(len(task.imgs))]
    (await games.insert(gameId, Game(model=task.model, imgIds=imgIds))).unsafe()
    E.sequence(await asyncio.gather(*[
      imgGameIds.insert(imgId, gameId)
      for imgId in imgIds
    ])).unsafe()
    E.sequence(await asyncio.gather(*[
      Qout.push(imgId, PreInput(model=task.model, img=img))
      for imgId, img in zip(imgIds, task.imgs)
    ])).unsafe()
    (await Qin.pop(gameId)).unsafe()
    logger(f'Pushed tasks from "{gameId}"', level='DEBUG')

  while True:
    r = await input_one()
    if r.tag == 'left':
      logger(r.value, level='ERROR')
      await asyncio.sleep(1)