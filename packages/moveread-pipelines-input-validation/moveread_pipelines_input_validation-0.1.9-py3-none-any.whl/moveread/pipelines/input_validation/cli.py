from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-q', '--queues', required=True, help='Queues DB path')
  parser.add_argument('--images', required=True)

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()


  import os
  from dslog import Logger
  queues_path = os.path.join(os.getcwd(), args.queues)
  images_path = os.path.join(os.getcwd(), args.images)
  
  logger = Logger.click().prefix('[INPUT VAL]')
  logger(f'Running input validation...')
  logger(f'Images path: "{images_path}"')
  logger(f'Queues path: "{queues_path}"')
  
  from typing import Any
  import uvicorn
  from q.kv import QueueKV
  from moveread.pipelines.input_validation import Pipeline, Input, Result

  Qin = QueueKV.sqlite(Input, queues_path, 'input')
  Qout = QueueKV.sqlite(Result, queues_path, 'output')
  api = Pipeline.artifacts(Qin=Qin, Qout=Qout)(images_path=images_path, logger=logger)
  uvicorn.run(api, port=args.port, host=args.host)

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/input-validation/demo')
  sys.argv.extend('-q queues.sqlite --images images'.split(' '))
  main()