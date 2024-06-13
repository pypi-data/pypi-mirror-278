from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('--images', required=True, type=str)
  parser.add_argument('-i', '--input', required=True, type=str)
  parser.add_argument('-o', '--output', required=True, type=str)

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()

  import os
  from dslog import Logger

  images = os.path.join(os.getcwd(), args.images)
  inp = os.path.join(os.getcwd(), args.input)
  out = os.path.join(os.getcwd(), args.output)

  logger = Logger.click().prefix('[GAME CORRECTION]')
  logger(f'Running API...')
  logger(f'- Input path: "{inp}"')
  logger(f'- Output path: "{out}"')
  logger(f'- Images path: "{images}"')
  os.makedirs(images, exist_ok=True)

  from typing import Any
  import uvicorn
  from q.kv import QueueKV
  from moveread.pipelines.game_correction import Pipeline, Input, Result

  Qin = QueueKV.sqlite(Input, inp)
  Qout = QueueKV.sqlite(Result, out)
  api = Pipeline.artifacts(Qin=Qin, Qout=Qout)(images_path=images, logger=logger)
  uvicorn.run(api, port=args.port, host=args.host)
  
if __name__ == '__main__':
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/1d.game-correction')
  import sys
  sys.argv.extend('-p 8001 -i demo/in -o demo/out --protocol sqlite --images /home/m4rs/mr-github/rnd/robust-extraction/demo/boxes/'.split(' '))
  main()