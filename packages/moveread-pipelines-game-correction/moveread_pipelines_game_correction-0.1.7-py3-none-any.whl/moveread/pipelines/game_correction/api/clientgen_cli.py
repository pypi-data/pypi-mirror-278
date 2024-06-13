import os
from argparse import ArgumentParser
from openapi_ts import generate_client
from ..api import fastapi
from .types import TYPESCRIPT

def main():

  parser = ArgumentParser()
  parser.add_argument('-p', '--package-path', help="Path to the typescript package's base folder", required=True)
  args = parser.parse_args()

  app = fastapi({}, '.') # type: ignore
  spec = app.openapi()
  path = os.path.abspath(args.package_path)
  generate_client(spec, path)

  with open(os.path.join(path, 'src', 'messages.ts'), 'w') as f:
    f.write(f'{TYPESCRIPT}')

  with open(os.path.join(path, 'src', 'index.ts'), 'a') as f:
    f.write("export * from './messages'\n")

if __name__ == '__main__':
  main()