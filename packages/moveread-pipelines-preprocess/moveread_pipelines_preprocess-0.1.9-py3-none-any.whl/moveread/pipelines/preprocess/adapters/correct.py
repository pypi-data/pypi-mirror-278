from functools import partial
from uuid import uuid4
from kv.api import KV
import pure_cv as vc
import robust_extraction as re
import moveread.pipelines.manual_correct as corr
from ..types import Input, Reextract
from ..spec_codegen import CorrectPipeline


def pre(state: Input) -> tuple[corr.Task, Input]:
  return corr.Task(img=state.img), state

async def store_corrected(
  images: KV[bytes], id: str, state: Input, res: corr.Corrected
):
  img = vc.decode((await images.read(state.img)).unsafe())
  mat = re.correct_perspective(img, res.corners) # type: ignore
  corr_img = vc.encode(mat, '.jpg') # type: ignore
  corr = f'{id}/manually-corrected_{uuid4()}.jpg'
  (await images.insert(corr, corr_img)).unsafe()
  return state.correct(res.corners, corr)

async def store_rotated(
  images: KV[bytes], id: str, state: Input, res: corr.Rotated
):
    img = vc.decode((await images.read(state.img)).unsafe())
    mat = vc.rotate(img, res.rotation)
    rot_img = vc.encode(mat, '.jpg') # type: ignore
    rotated = f'{id}/rotated_{uuid4()}.jpg'
    (await images.insert(rotated, rot_img)).unsafe()
    return state.rotate(res.rotation, rotated)

async def post(images: KV[bytes], id: str, entry: tuple[corr.Result, Input]) -> CorrectPipeline.Out:
  res, state = entry
  match res.tag:
    case 'corrected':
      return Reextract.of(await store_corrected(images, id, state, res))
    case 'rotated':
      return await store_rotated(images, id, state, res)

def correction_api(*, Qin: CorrectPipeline.QueueIn, Qout: CorrectPipeline.QueueOut, images: KV[bytes]) -> corr.CorrectionAPI:
  return corr.CorrectionAPI(
    Qin.map(pre), # type: ignore (so dumb...)
    Qout.apremap_kv(partial(post, images))
  )