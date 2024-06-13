import moveread.pipelines.manual_select as sel
from ..types import Correct, PreOutput
from ..spec_codegen import SelectPipeline

def pre(state: SelectPipeline.In) -> tuple[sel.Task, SelectPipeline.In]:
  return sel.Task(img=state.corrected, model=state.model), state

def post(entry: tuple[sel.Result, SelectPipeline.In]) -> SelectPipeline.Out:
  res, state = entry
  match res.tag:
    case 'selected':
      return PreOutput(state.select(res.grid_coords))
    case 'recorrect':
      return Correct.of(state)

def selection_api(Qin: SelectPipeline.QueueIn, Qout: SelectPipeline.QueueOut) -> sel.SelectAPI:
  return sel.SelectAPI(
    Qin.map(pre),
    Qout.premap(post)
  )