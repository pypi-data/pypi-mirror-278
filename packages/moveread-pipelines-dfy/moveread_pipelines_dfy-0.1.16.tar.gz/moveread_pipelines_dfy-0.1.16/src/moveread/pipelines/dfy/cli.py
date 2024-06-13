from argparse import ArgumentParser
import os

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser()
  parser.add_argument('-b', '--base-path', required=True)
  parser.add_argument('--token', **env('TOKEN', default='secret'), type=str)

  parser.add_argument('--tfs-host', **env('TFS_HOST', required=False), type=str)
  parser.add_argument('--tfs-port', **env('TFS_PORT', required=False), type=str)
  parser.add_argument('--tfs-endpoint', **env('TFS_ENDPOINT', required=False), type=str)

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()

  import os
  from dslog import Logger
  base_path = os.path.join(os.getcwd(), args.base_path)
  
  logger = Logger.click().prefix('[DFY]')
  logger(f'Running preprocessing at "{base_path}"...')
  
  import asyncio
  from multiprocessing import Process
  import uvicorn
  from moveread.pipelines.dfy import Workflow, local_storage, local_queues
  import tf.serving as tfs

  queues = local_queues(base_path)
  params = local_storage(base_path)
  artifacts = Workflow.artifacts(**queues['internal'])(
    tfserving=tfs.Params(host=args.tfs_host, port=args.tfs_port, endpoint=args.tfs_endpoint),
    token=args.token, **params
  )

  ps = {
    id: Process(target=asyncio.run, args=(f,))
    for id, f in artifacts.processes.items()
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
  path = '/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/4.dfy/demo'
  os.makedirs(path, exist_ok=True)
  os.chdir(path)
  sys.argv.extend('-b internal/ --images images'.split(' '))
  main()