from typing import Callable, TypeVar
from uuid import uuid4
from kv.api import KV
from q.api import WriteQueue
from dslog import Logger
from moveread.core import CoreAPI, Game
from ..types import Input, GameId

def gameId(game: Game) -> GameId:
  if game.meta is None or game.meta.tournament is None:
    return GameId(group='a', round=1, board=1)
  t = game.meta.tournament
  return GameId(group=t.group or 'a', round=t.round or 1, board=t.board or 1)

S = TypeVar('S')

async def input_core(
  core: CoreAPI, Qin: WriteQueue[tuple[Input, S]],
  *, images: KV[bytes],
  gameId_fn: Callable[[Game], GameId] = gameId,
  state_fn: Callable[[Game], S] = lambda *_: '',
  num_games: int | None = None, shuffle: bool = True,
  logger = Logger.rich().prefix('[CORE INPUT]')
):
  """Input all images from `core` into `Qin` tasks
  - Actually, only images with `version == 0`
  - `model_fn`: determines the scoresheet model of each task
  - `state_fn`: determines an arbitrary tuple of JSON-serializable data to attach to each task
  """
  games = list((await core.games.keys()).unsafe())
  if shuffle:
    import random
    random.shuffle(games)
  for gameId in games[:num_games]:
    game = (await core.games.read(gameId)).unsafe()
    imgs = []
    for imgId, image in game.images:
      if imgId.version == 0:
        id = str(imgId)
        url = f'{id}/original_{uuid4()}.jpg'
        img = (await core.blobs.read(image.url)).unsafe()
        (await images.insert(url, img)).unsafe()
        imgs.append(url)

    state = state_fn(game)
    task = Input(gameId=gameId_fn(game), imgs=imgs)
    await Qin.push(gameId, (task, state))
    logger(f'Inputted task "{gameId}". Task:', task)