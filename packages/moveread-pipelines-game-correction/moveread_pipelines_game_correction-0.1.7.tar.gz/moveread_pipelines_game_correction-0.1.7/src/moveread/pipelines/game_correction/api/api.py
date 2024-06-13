import os
import asyncio
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse
from haskellian import ManagedAsync, AsyncIter, Iter, either as E
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from ..types import Item, MetaItem, Annotations
from ..sdk import CorrectionAPI
from .types import Preds, Done, Message

def fastapi(
  sdk: CorrectionAPI, images_path: str | None = None, *,
  logger = Logger.click().prefix('[GAME CORRECTION]')
):

  outputs: dict[str, ManagedAsync[Message]] = {}
  requestIds: dict[str, str] = {}

  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER),
    )
  )
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  if images_path is not None:
    app.mount('/images', StaticFiles(directory=images_path))

  @app.get('/items', response_model_exclude_none=True)
  async def get_items() -> list[MetaItem]:
    all = await sdk.items().sync()
    return Iter(E.filter(all)).sync()
  
  @app.get('/item', response_model_exclude_none=True)
  async def get_item(id: str, req: Request, res: Response) -> Item | None:
    item = (await sdk.item(id)).get_or(None)
    if item is None:
      res.status_code = status.HTTP_404_NOT_FOUND
    elif images_path is None:
      return item
    else:
      base_path = os.path.join(str(req.base_url), 'images')
      return item.at_url(base_path)

  @app.post('/annotate')
  def annotate(id: str, annotations: list[Annotations]):
    sdk.annotate(id, annotations)

  @app.post('/move')
  def manual_move(id: str, ply: int, uci: str):
    sdk.manual_move(id, ply, uci)

  class CorrectParams(BaseModel):
    pgn: list[str]
    early: bool
    annotations: list[Annotations]

  @app.post('/confirm')
  async def confirm(id: str, p: CorrectParams, r: Response) -> bool:
    res = await sdk.correct(id, pgn=p.pgn, early=p.early, annotations=p.annotations)
    ok = res.tag == 'right'
    if not ok:
      r.status_code = status.HTTP_404_NOT_FOUND
    return ok
  
  @app.post('/repreprocess')
  async def repreprocess(id: str, r: Response) -> bool:
    res = await sdk.repreprocess(id)
    ok = res.tag == 'right'
    if not ok:
      r.status_code = status.HTTP_404_NOT_FOUND
    return ok
  
  @app.post('/predict')
  async def predict(gameId: str, userId: str, reqId: str, fen: str | None = None):

    if not userId in outputs:
      outputs[userId] = ManagedAsync()
    requestIds[userId] = reqId

    either = await sdk.predict(gameId, fen)
    if either.tag == 'left':
      outputs[userId].push(Done(reqId=reqId))
      return Response(either.value, status_code=404)
    
    for ps in either.value:
      if requestIds[userId] != reqId:
        outputs[userId].push(Done(reqId=reqId))
        return print(f'{reqId} got canceled')
      outputs[userId].push(Preds(reqId=reqId, preds=list(ps)))
      await asyncio.sleep(0) # yield control to the event loop, to force result streaming
    outputs[userId].push(Done(reqId=reqId))

  @app.get('/preds')
  async def preds(userId: str):
    if not userId in outputs:
      outputs[userId] = ManagedAsync()
    return EventSourceResponse(AsyncIter(outputs[userId]).map(lambda m: m.model_dump_json()))

  return app