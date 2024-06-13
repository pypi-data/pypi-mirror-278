from typing import Literal
import asyncio
import os
from pydantic import BaseModel
from fastapi import FastAPI, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from haskellian import iter as I, either as E, Left, Right
import moveread.pipelines.manual_correct as corr
import moveread.pipelines.manual_select as sel
import moveread.pipelines.extract_validation as val

class CorrectItem(corr.Task):
  tag: Literal['correct'] = 'correct'
  id: str

  @classmethod
  def of(cls, images_path: str):
    def inner(item: tuple[str, corr.Task]) -> CorrectItem:
      id, task = item
      return CorrectItem(img=os.path.join(images_path, task.img), id=id)
    return inner
  
class SelectItem(sel.Task):
  tag: Literal['select'] = 'select'
  id: str

  @classmethod
  def of(cls, images_path: str):
    def inner(item: tuple[str, sel.Task]) -> SelectItem:
      id, task = item
      return SelectItem(img=os.path.join(images_path, task.img), id=id, model=task.model)
    return inner

class ValidationItem(val.Task):
  tag: Literal['validate'] = 'validate'
  id: str

  @classmethod
  def of(cls, images_path: str):
    def inner(item: tuple[str, val.Task]) -> ValidationItem:
      id, task = item
      return ValidationItem(contoured=os.path.join(images_path, task.contoured), id=id, already_corrected=task.already_corrected)
    return inner

Item = CorrectItem | SelectItem | ValidationItem
AnnotateResponse = Literal['OK', 'NOT_FOUND', 'BAD_ANNOTATION', 'SERVER_ERROR']

def fastapi(
  *, corr_api: corr.CorrectionAPI,
  val_api: val.ValidationAPI,
  reval_api: val.ValidationAPI,
  sel_api: sel.SelectAPI,
  images_path: str | None = None,
  logger = Logger.rich().prefix('[MANUAL API]')
) -> FastAPI:
  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER)
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
    os.makedirs(images_path, exist_ok=True)
    app.mount('/images', StaticFiles(directory=images_path))

  @app.get('/items')
  async def get_items(r: Request) -> list[Item]:
    base = os.path.join(str(r.base_url), 'images') if images_path is not None else ''
    tasks = (
      corr_api.items().map(lambda e: e | CorrectItem.of(base)).sync(),
      sel_api.items().map(lambda e: e | SelectItem.of(base)).sync(),
      reval_api.items().map(lambda e: e | ValidationItem.of(base)).sync(),
      val_api.items().map(lambda e: e | ValidationItem.of(base)).sync(),
    )
    all = I.flatten(await asyncio.gather(*tasks)).sync()
    errs = list(E.filter_lefts(all))
    if errs != []:
      logger('Errors reading tasks:', *errs, level='ERROR')
    return list(E.filter(all))
  
  class CorrectParams(BaseModel):
    corners: corr.Corners
  
  @app.post('/correct')
  async def correct(id: str, params: CorrectParams, r: Response) -> bool:
    x = await corr_api.correct(id, params.corners)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error correcting item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  class RotateParams(BaseModel):
    rotation: corr.Rotation
  
  @app.post('/rotate')
  async def rotate(id: str, params: RotateParams, r: Response) -> bool:
    x = await corr_api.rotate(id, params.rotation)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error rotating item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  class SelectParams(BaseModel):
    gridCoords: sel.Rectangle
  
  @app.post('/select')
  async def select(id: str, params: SelectParams, r: Response) -> bool:
    x = await sel_api.select(id, params.gridCoords)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error selecting item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  @app.post('/recorrect')
  async def recorrect(id: str, r: Response) -> bool:
    x = await sel_api.recorrect(id)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error recorrecting item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  @app.post('/annotate')
  async def annotate(id: str, annotation: val.Annotation, r: Response) -> AnnotateResponse:
    match await val_api.annotate(id, annotation):
      case Right():
        return 'OK'
      case Left(err):
        if err.reason == 'inexistent-item':
          r.status_code = status.HTTP_404_NOT_FOUND
          return 'NOT_FOUND'
        elif err.reason == 'bad-annotation':
          r.status_code = status.HTTP_400_BAD_REQUEST
          return 'BAD_ANNOTATION'
        else:
          logger(f'Error annotating item {id}', err, level='ERROR')
          r.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
          return 'SERVER_ERROR'
        
  @app.post('/reannotate')
  async def reannotate(id: str, annotation: val.Reannotation, r: Response) -> AnnotateResponse:
    match await reval_api.annotate(id, annotation):
      case Right():
        return 'OK'
      case Left(err):
        if err.reason == 'inexistent-item':
          r.status_code = status.HTTP_404_NOT_FOUND
          return 'NOT_FOUND'
        elif err.reason == 'bad-annotation':
          r.status_code = status.HTTP_400_BAD_REQUEST
          return 'BAD_ANNOTATION'
        else:
          logger(f'Error reannotating item {id}', err, level='ERROR')
          r.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
          return 'SERVER_ERROR'
  
  return app