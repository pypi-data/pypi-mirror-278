import os
from fastapi import FastAPI, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from haskellian import either as E, Iter
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from .sdk import InputValidationSDK
from .types import Item, Result

def fastapi(
  sdk: InputValidationSDK, images_path: str | None = None,
  *, logger = Logger.click().prefix('[INPUT VALIDATION]')
):

  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER),
    )
  )

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  if images_path is not None:
    app.mount('/images', StaticFiles(directory=images_path))

  def images_base(req: Request):
    return '' if images_path is None else os.path.join(str(req.base_url), 'images')

  @app.get('/tasks')
  async def get_tasks(req: Request) -> list[Item]:
    images_path = images_base(req)
    tasks = await sdk.tasks().sync()
    errs = list(E.filter_lefts(tasks))
    if errs != []:
      logger('Errors reading tasks:', *errs, level='ERROR')
    return Iter(E.filter(tasks)).map(lambda t: t.at_url(images_path)).sync()

  @app.post('/validate')
  async def validate(taskId: str, result: Result, req: Request, res: Response):
    r = await sdk.validate(taskId, result.strip_url(images_base(req)))
    if r.tag == 'left':
      logger(f'Error validating result for task "{taskId}":', r.value, level='ERROR')
      if r.value.reason == 'inexistent-item':
        res.status_code = status.HTTP_404_NOT_FOUND
      else:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

  return app