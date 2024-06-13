from pipeteer import Workflow, Pipeline
from .types import Result, Input, Validate, Correct, Reextract, Revalidate, Select, PreOutput, Output

workflow = Workflow[Input, Result](
  'extract', Result,
  pipelines=dict(
    extract=Pipeline(Input, Validate, Correct),
    validate=Pipeline(Validate, PreOutput, Correct, Select),
    correct=Pipeline(Correct, Input, Reextract),
    reextract=Pipeline(Reextract, Revalidate, Select),
    revalidate=Pipeline(Revalidate, PreOutput, Select),
    select=Pipeline(Select, PreOutput, Correct),
    preoutput=Pipeline(PreOutput, Result)
  )
)

def codegen():
  workflow.codegen(__file__, overwrite=True)

if __name__ == '__main__':
  codegen()