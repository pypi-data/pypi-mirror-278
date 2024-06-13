import os
from typing import Sequence
from typing_extensions import TypedDict
from pydantic import BaseModel
from pipeteer import Pipeline

class GameId(TypedDict):
  group: str
  round: str
  board: str

class Input(BaseModel):
  gameId: GameId
  imgs: Sequence[str]

class Item(Input):
  taskId: str

  def at_url(self, base_url: str) -> 'Item':
    copy = self.model_copy()
    copy.imgs = [os.path.join(base_url, img) for img in self.imgs]
    return copy

class Result(BaseModel):
  gameId: GameId
  imgs: Sequence[str]

  def strip_url(self, base_url: str) -> 'Result':
    copy = self.model_copy()
    copy.imgs = [img.replace(base_url, '').strip('/') for img in self.imgs]
    return copy
  
pipeline = Pipeline(Input, Result)