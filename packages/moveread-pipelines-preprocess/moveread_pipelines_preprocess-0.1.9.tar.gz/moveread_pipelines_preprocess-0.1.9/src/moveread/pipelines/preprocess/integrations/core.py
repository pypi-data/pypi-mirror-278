from typing import Callable
from uuid import uuid4
from kv.api import KV
from q.api import WriteQueue
from dslog import Logger
from scoresheet_models import ModelID
from moveread.core import CoreAPI, Game, ImageID
from moveread.pipelines.preprocess import Input

async def input_core(
  core: CoreAPI, Qin: WriteQueue[Input],
  *, images: KV[bytes],
  model_fn: Callable[[Game, ImageID], ModelID] = lambda *_: 'llobregat23',
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
    for imgId, image in game.images:
      if imgId.version == 0:
        id = str(imgId)
        url = f'{id}/original_{uuid4()}.jpg'
        img = (await core.blobs.read(image.url)).unsafe()
        (await images.insert(url, img)).unsafe()
        task = Input(model=model_fn(game, imgId), img=url)
        await Qin.push(id, task)
        logger(f'Inputted task "{id}". Task:', task)