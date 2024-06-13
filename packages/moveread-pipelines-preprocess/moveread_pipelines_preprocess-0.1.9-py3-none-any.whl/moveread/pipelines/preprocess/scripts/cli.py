from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-q', '--queues', required=True)
  parser.add_argument('--images', required=True)

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()

  import os
  from dslog import Logger
  queues_path = os.path.join(os.getcwd(), args.queues)
  images_path = os.path.join(os.getcwd(), args.images)
  
  logger = Logger.click().prefix('[PREPROCESS]')
  logger(f'Running preprocessing...')
  logger(f'Images path: "{images_path}"')
  logger(f'Queues path: "{queues_path}"')
  
  from typing import Sequence
  import asyncio
  from multiprocessing import Process
  from kv.fs import FilesystemKV
  from q.kv import QueueKV
  import uvicorn
  from moveread.pipelines.preprocess import Workflow, Result

  def make_queue(path: Sequence[str], type: type):
    return QueueKV.sqlite(type, queues_path, table='-'.join(path))
  
  images = FilesystemKV[bytes](images_path)

  Qout = QueueKV.sqlite(Result, queues_path, table='output')
  Qs = Workflow.make_queues(make_queue, Qout)
  artifacts = Workflow.artifacts(**Qs['internal'])(images=images, images_path=images_path)

  ps = {
    id: Process(target=asyncio.run, args=(f,)) for id, f in artifacts.processes.items()
  } | {
    'api': Process(target=uvicorn.run, args=(artifacts.api,), kwargs={'host': args.host, 'port': args.port})
  }
  for id, p in ps.items():
    p.start()
    logger(f'Process "{id}" started at PID {p.pid}')
  for p in ps.values():
    p.join()

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/2.preprocess/demo')
  sys.argv.extend('-q queues.sqlite --images images'.split(' '))
  main()