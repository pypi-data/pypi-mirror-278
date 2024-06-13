from functools import partial
from uuid import uuid4
from haskellian import Left, Right
from dslog import Logger
from kv.api import KV
import moveread.pipelines.auto_extraction as extr
from ..types import Input, Extracted, Validate, Correct, Select, Revalidate
from ..spec_codegen import ExtractPipeline as Extract, ReextractPipeline as Reextract

async def pre_extr(images: KV[bytes], inp: Extract.In, already_corrected: bool) -> tuple[extr.Task, Extract.In]:
  img = (await images.read(inp.img)).unsafe()
  task = extr.Task(model=inp.model, already_corrected=already_corrected, img=img)
  return task, inp

async def store_extr(images: KV[bytes], id: str, res: extr.Ok, inp: Input) -> Extracted:
  corr = f'{id}/corrected_{uuid4()}.jpg'
  cont = f'{id}/contoured_{uuid4()}.jpg'
  (await images.insert(corr, res.corrected)).unsafe()
  (await images.insert(cont, res.contoured)).unsafe()
  return inp.extract(
    corners=res.perspective_corners, corrected=corr,
    contoured=cont, contours=res.contours
  )

async def post_extr(
  images: KV[bytes], id: str, entry: tuple[extr.Result, Extract.In],
) -> Extract.Out:
  result, inp = entry
  match result:
    case Left():
      return Correct.of(inp)
    case Right(ok):
      next_state = await store_extr(images, id, ok, inp)
      return Validate.of(next_state)
    
async def pre_rextr(images: KV[bytes], inp: Reextract.In, already_corrected: bool) -> tuple[extr.Task, Reextract.In]:
  img = (await images.read(inp.corrected)).unsafe()
  task = extr.Task(model=inp.model, already_corrected=already_corrected, img=img)
  return task, inp
    
async def store_rextr(images: KV[bytes], id: str, res: extr.Ok, inp: Reextract.In) -> Extracted:
  cont = f'{id}/re-contoured_{uuid4()}.jpg'
  (await images.insert(cont, res.contoured)).unsafe()
  return inp.re_extract(contoured=cont, contours=res.contours)

async def post_rextr(
  images: KV[bytes], id: str, entry: tuple[extr.Result, Reextract.In],
) -> Reextract.Out:
  result, inp = entry
  match result:
    case Left():
      return Select.of(inp)
    case Right(ok):
      next_state = await store_rextr(images, id, ok, inp)
      return Revalidate.of(next_state)


async def run_extract(
  Qin: Extract.QueueIn, Qout: Extract.QueueOut,  
  *, images: KV[bytes], logger = Logger.rich().prefix('[EXTRACT]')
):
  await extr.run(
    Qin.amap(partial(pre_extr, images, already_corrected=False)),
    Qout.apremap_kv(partial(post_extr, images)),
    logger=logger
  )

async def run_reextract(
  Qin: Reextract.QueueIn, Qout: Reextract.QueueOut,
  *, images: KV[bytes], logger = Logger.rich().prefix('[RE-EXTRACT]')
):
  await extr.run(
    Qin.amap(partial(pre_rextr, images, already_corrected=True)),
    Qout.apremap_kv(partial(post_rextr, images)),
    logger=logger
  )

__all__ = ['run_extract', 'run_reextract']