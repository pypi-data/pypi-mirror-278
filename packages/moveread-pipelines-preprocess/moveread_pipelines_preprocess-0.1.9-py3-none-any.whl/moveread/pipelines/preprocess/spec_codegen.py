from typing import Unpack, TypedDict
from q.api import WriteQueue, ReadQueue, Queue
from pipeteer import MakeQueue, make_queues as _make_queues, PipelineQueues
from .spec import Input, Select, Correct, Reextract, Result, workflow, Validate, PreOutput, Revalidate

class ExtractPipeline:
  In = Input
  Out = Validate | Correct
  QueueIn = ReadQueue[Input]
  QueueOut = WriteQueue[Validate | Correct]
  Queues = PipelineQueues[Input, Validate | Correct]

class ValidatePipeline:
  In = Validate
  Out = PreOutput | Correct | Select
  QueueIn = ReadQueue[Validate]
  QueueOut = WriteQueue[PreOutput | Correct | Select]
  Queues = PipelineQueues[Validate, PreOutput | Correct | Select]

class CorrectPipeline:
  In = Correct
  Out = Input | Reextract
  QueueIn = ReadQueue[Correct]
  QueueOut = WriteQueue[Input | Reextract]
  Queues = PipelineQueues[Correct, Input | Reextract]

class ReextractPipeline:
  In = Reextract
  Out = Revalidate | Select
  QueueIn = ReadQueue[Reextract]
  QueueOut = WriteQueue[Revalidate | Select]
  Queues = PipelineQueues[Reextract, Revalidate | Select]

class RevalidatePipeline:
  In = Revalidate
  Out = PreOutput | Select
  QueueIn = ReadQueue[Revalidate]
  QueueOut = WriteQueue[PreOutput | Select]
  Queues = PipelineQueues[Revalidate, PreOutput | Select]

class SelectPipeline:
  In = Select
  Out = PreOutput | Correct
  QueueIn = ReadQueue[Select]
  QueueOut = WriteQueue[PreOutput | Correct]
  Queues = PipelineQueues[Select, PreOutput | Correct]

class PreoutputPipeline:
  In = PreOutput
  Out = Result
  QueueIn = ReadQueue[PreOutput]
  QueueOut = WriteQueue[Result]
  Queues = PipelineQueues[PreOutput, Result]



class Workflow:
  class InternalQueues(TypedDict):
    extract: ExtractPipeline.Queues  
    validate: ValidatePipeline.Queues  
    correct: CorrectPipeline.Queues  
    reextract: ReextractPipeline.Queues  
    revalidate: RevalidatePipeline.Queues  
    select: SelectPipeline.Queues  
    preoutput: PreoutputPipeline.Queues  

  class Queues(TypedDict):
    Qin: Queue[Input]
    internal: 'Workflow.InternalQueues'

  @staticmethod
  def make_queues(make_queue: MakeQueue, output_queue: WriteQueue[Result]) -> Queues:
    return _make_queues(workflow, make_queue, output_queue) # type: ignore
  
  @staticmethod
  def artifacts(**queues: Unpack['Workflow.InternalQueues']):
    from .main import artifacts
    return artifacts(**queues)
    