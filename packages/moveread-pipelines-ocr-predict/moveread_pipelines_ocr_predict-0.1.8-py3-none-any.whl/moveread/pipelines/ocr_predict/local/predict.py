from typing import Any, Literal, Unpack
import asyncio
from kv.fs import FilesystemKV
from moveread.pipelines.ocr_predict import run, local
from tf.serving import Params
from dslog import Logger

def run_predict(
  input_path: str,
  output_path: str,
  images_path: str, *,
  protocol: Literal['sqlite', 'fs'] = 'sqlite',
  logger = Logger.empty(),
  **params: Unpack[Params]
):
  Qin = local.input_queue(input_path, Any, protocol) # type: ignore
  Qout = local.output_queue(output_path, Any, protocol) # type: ignore
  images = FilesystemKV[bytes](images_path)
  asyncio.run(run(Qin, Qout, images=images, logger=logger, **params))