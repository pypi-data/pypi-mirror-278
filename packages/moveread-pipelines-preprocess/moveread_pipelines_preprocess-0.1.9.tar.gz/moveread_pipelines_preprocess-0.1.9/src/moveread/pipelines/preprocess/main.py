from typing_extensions import Mapping, Unpack, Coroutine, TypedDict, NotRequired
from dataclasses import dataclass
from dslog import Logger
from kv.api import KV
from fastapi import FastAPI
from .spec_codegen import Workflow
from .adapters import run_extract, run_reextract, \
  fastapi, correction_api, revalidation_api, validation_api, selection_api, \
  run_preoutput

class Params(TypedDict):
  images: KV[bytes]
  images_path: NotRequired[str | None]

@dataclass
class Artifacts:
  api: FastAPI
  processes: Mapping[str, Coroutine[None, None, None]]

def artifacts(**Qs: Unpack[Workflow.InternalQueues]):
  def _bound(*, logger: Logger = Logger.click().prefix('[PREPROCESS]'), images: KV[bytes], images_path: str | None = None):
    return Artifacts(
      api=fastapi(
        corr_api=correction_api(images=images, **Qs['correct']),
        val_api=validation_api(**Qs['validate']),
        reval_api=revalidation_api(**Qs['revalidate']),
        sel_api=selection_api(**Qs['select']),
        images_path=images_path, logger=logger.prefix('[API]')
      ),
      processes={
        'extract': run_extract(images=images, logger=logger.prefix('[EXTRACT]'), **Qs['extract']),
        'reextract': run_reextract(images=images, logger=logger.prefix('[REEXTRACT]'), **Qs['reextract']),
        'preoutput': run_preoutput(images=images, logger=logger.prefix('[PREOUTPUT]'), **Qs['preoutput']),
      }
    )
  return _bound