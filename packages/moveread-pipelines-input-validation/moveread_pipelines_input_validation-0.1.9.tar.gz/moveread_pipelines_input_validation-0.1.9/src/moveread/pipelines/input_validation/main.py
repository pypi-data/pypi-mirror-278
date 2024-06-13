from typing import NotRequired, TypedDict, Unpack
from dslog import Logger
from q.api import ReadQueue, WriteQueue, Queue
from .types import Input, Result
from .sdk import InputValidationSDK
from .api import fastapi

class Params(TypedDict):
  images_path: NotRequired[str | None]

class Pipeline:
  class Queues(TypedDict):
    Qin: ReadQueue[Input]
    Qout: WriteQueue[Result]

  @staticmethod
  def artifacts(**queues: Unpack['Pipeline.Queues']):
    
    def _bound(*, images_path: str | None = None, logger = Logger.click().prefix('[INPUT VAL]')):
      sdk = InputValidationSDK(**queues)
      return fastapi(sdk, images_path, logger=logger)
    
    return _bound