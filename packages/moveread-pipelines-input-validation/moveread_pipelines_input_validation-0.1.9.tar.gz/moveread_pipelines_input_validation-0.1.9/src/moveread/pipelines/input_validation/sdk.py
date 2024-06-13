from dataclasses import dataclass
from q.api import ReadQueue, WriteQueue, ReadError
from haskellian import either as E
from .types import Input, Item, Result

def make_item(entry: tuple[str, Input]):
  id, task = entry
  return Item(gameId=task.gameId, imgs=task.imgs, taskId=id)

@dataclass
class InputValidationSDK:

  Qin: ReadQueue[Input]
  Qout: WriteQueue[Result]

  def tasks(self):
    return self.Qin.items().map(lambda e: e.fmap(make_item))
  
  @E.do[ReadError]()
  async def validate(self, taskId: str, result: Result):
    (await self.Qin.read(taskId)).unsafe()
    (await self.Qout.push(taskId, result)).unsafe()
    (await self.Qin.pop(taskId)).unsafe()