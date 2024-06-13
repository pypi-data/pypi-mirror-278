from typing import Unpack, TypeAlias, TypedDict
import base64
import asyncio
from haskellian import iter as I, either as E, funcs as F
from kv.api import KV, ReadError as KVReadError
from q.api import ReadQueue, WriteQueue, Queue, ReadError as QReadError
import tf.serving as tfs
from dslog import Logger
from .types import Input, Preds

Err: TypeAlias = QReadError | KVReadError | tfs.PredictErr

async def run(
  Qin: ReadQueue[Input],
  Qout: WriteQueue[Preds], *,
  images: KV[bytes],
  logger = Logger.rich().prefix('[OCR PREDS]'),
  **params: Unpack[tfs.Params]
):
  """Runs predections by reading task images as keys of `images`. Appends a `State` entry first, then all `Preds`"""
  
  @E.do[Err]()
  async def run_one():
    id, task = (await Qin.read()).unsafe()
    logger(f'Predicting "{id}"')
    
    imgs = await asyncio.gather(*[
      asyncio.gather(*[images.read(url).then(E.unsafe) for url in ply_urls])
      for ply_urls in task.ply_boxes
    ])
    b64imgs = I.ndmap(F.flow(base64.urlsafe_b64encode, bytes.decode), imgs)

    results: Preds = []
    for i, batch in I.batch(8, b64imgs).enumerate():
      logger(f'"{id}": Batch {i}', level='DEBUG')
      preds = (await tfs.multipredict(batch, **params)).unsafe()
      results.extend(preds)
    
    logger(f'Done predicting "{id}"')
    (await Qout.push(id, results)).unsafe()
    (await Qin.pop(id)).unsafe()
  
  while True:
    res = await run_one()
    if res.tag == 'left':
      logger(f'Prediction error', res.value, level='ERROR')
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(0) # release the loop

class Params(tfs.Params):
  images: KV[bytes]

class Pipeline:
  class Queues(TypedDict):
    Qin: ReadQueue[Input]
    Qout: WriteQueue[Preds]

  @staticmethod
  def artifacts(**queues: Unpack['Pipeline.Queues']):
    async def _bound(*, images: KV[bytes], logger = Logger.rich().prefix('[OCR PREDS]'), **params: Unpack[tfs.Params]):
      return await run(**queues, images=images, logger=logger, **params)
    return _bound