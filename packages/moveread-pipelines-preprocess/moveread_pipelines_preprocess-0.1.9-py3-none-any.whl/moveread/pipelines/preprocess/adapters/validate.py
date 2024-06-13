import moveread.pipelines.extract_validation as val
from ..types import PreOutput, Correct, Select
from ..spec_codegen import ValidatePipeline as Validate, RevalidatePipeline as Revalidate

In = Validate.In | Revalidate.In

def pre(state: In) -> tuple[val.Task, In]:
  return val.Task(contoured=state.contoured, already_corrected=state.confirmed), state

def next_task_val(ann: val.Annotation, state: Validate.In) -> Validate.Out:
  match ann:
    case 'correct': return PreOutput(state.ok())
    case 'incorrect': return Correct.of(state)
    case 'perspective-correct': return Select.of(state)

def post_val(entry: tuple[val.Annotation, Validate.In]) -> Validate.Out:
  ann, state = entry
  return next_task_val(ann, state)

def next_task_reval(ann: val.Reannotation, state: Revalidate.In) -> Revalidate.Out:
  match ann:
    case 'correct': return PreOutput(state.ok())
    case 'incorrect': return Select.of(state)

def post_reval(entry: tuple[val.Reannotation, Revalidate.In]) -> Revalidate.Out:
  ann, state = entry
  return next_task_reval(ann, state)

def validation_api(Qin: Validate.QueueIn, Qout: Validate.QueueOut) -> val.ValidationAPI:
  return val.ValidationAPI(
    Qin.map(pre),
    Qout.premap(post_val)
  )

def revalidation_api(Qin: Revalidate.QueueIn, Qout: Revalidate.QueueOut) -> val.ValidationAPI:
  return val.ValidationAPI(
    Qin.map(pre),
    Qout.premap(post_reval)
  )
