import asyncio
from typing import Mapping
from haskellian import either as E
from dslog import Logger
from kv.api import KV
from ..spec import Game, Result
from ..spec_codegen import JoinPipeline as Join

async def join(
  Qin: Join.QueueIn, Qout: Join.QueueOut, *,
  logger: Logger = Logger.of(print).prefix('[JOIN]'),
  received_imgs: KV[Mapping[str, Join.In]],
  games: KV[Game], imgGameIds: KV[str],
):
  @E.do()
  async def run_one():
    imgId, result = (await Qin.read()).unsafe()
    gameId = (await imgGameIds.read(imgId)).mapl(lambda err: f'Error reading image "{imgId}" gameId: {err}').unsafe()
    logger(f'Received "{imgId}" for "{gameId}"', level='DEBUG')
    game, received = await asyncio.gather(
      games.read(gameId).then(lambda e: e.mapl(lambda err: f'Error reading buffered game: {err}').unsafe()),
      received_imgs.read(gameId).then(E.get_or({})),
    )

    received_now = dict(received) | { imgId: result }
    receivedIds = set(imgId for imgId, _ in received_now.items())
    requiredIds = set(game.imgIds)
    logger('Received:', receivedIds, 'Required', requiredIds, level='DEBUG')

    if receivedIds == requiredIds:
      next = Result(preprocessed_imgs=[received_now[id] for id in game.imgIds])
      (await Qout.push(gameId, next)).unsafe()
      _, e = await asyncio.gather(
        games.delete(gameId).then(E.unsafe),
        received_imgs.delete(gameId),
      )
      if e.tag == 'left' and e.value.reason != 'inexistent-item':
        e.unsafe()
      logger(f'Joined results for {gameId}')
    else:
      (await received_imgs.insert(gameId, received_now)).unsafe()
    
    (await imgGameIds.delete(imgId)).unsafe()
    (await Qin.pop(imgId)).unsafe()

  while True:
    r = await run_one()
    if r.tag == 'left':
      logger(r.value, level='ERROR')
      await asyncio.sleep(1)
    