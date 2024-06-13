from typing import Unpack, TypedDict
from q.api import ReadQueue, WriteQueue, Queue
from dslog import Logger
from .types import Result, Input
from .sdk import CorrectionAPI
from .api import fastapi

class Pipeline:
  class Queues(TypedDict):
    Qin: ReadQueue[Input]
    Qout: WriteQueue[Result]
  
  @staticmethod
  def artifacts(**queues: Unpack[Queues]):
    def _bound(*, images_path: str | None = None, logger = Logger.click().prefix('[GAME CORRECTION]')):
      sdk = CorrectionAPI(**queues)
      return fastapi(sdk, images_path=images_path, logger=logger)
    return _bound