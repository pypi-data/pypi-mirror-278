from typing import TypeVar, Literal, Sequence
from collections import defaultdict
from itertools import zip_longest
from haskellian import either as E, iter as I
from q.api import ReadQueue, WriteQueue, ReadError
import game_prediction2 as gp
from .types import Item, CorrectResult, BadlyPreprocessed, MetaItem, Result, Input, Annotations, no_na


S = TypeVar('S')
PredictErr = Literal['NOT_FOUND', 'BAD_TASK']

def crop_corrects(ply_preds: Sequence[Sequence[S]], end_corrects: Sequence[int|None]) -> Sequence[Sequence[S]]:
  player_preds = I.transpose(ply_preds)
  limited_preds = [preds[:end] for preds, end in zip_longest(player_preds, end_corrects)]
  return I.transpose_ragged(limited_preds)

class CorrectionAPI:

  def __init__(self, Qin: ReadQueue[Input], Qout: WriteQueue[Result]):
    self._Qin = Qin
    self._Qout = Qout
    self._annotations: dict[str, Sequence[Annotations]] = {}
    self._manual_ucis: defaultdict[str, dict[int, str]] = defaultdict(dict[int, str])

  def _make_meta(self, entry: tuple[str, Input]) -> MetaItem:
    id, task = entry
    return MetaItem(id=id, title=task.title, details=task.details)
  
  def _make_item(self, id: str, task: Input) -> Item:
    ann = self._annotations.get(id)
    manual = self._manual_ucis.get(id)
    return Item(id=id, ply_boxes=task.ply_boxes, annotations=ann, manual_ucis=manual, title=task.title, details=task.details)

  def items(self):
    return self._Qin.items().map(lambda e: e.fmap(self._make_meta))
  
  @E.do[ReadError]()
  async def item(self, id: str):
    item = (await self._Qin.read(id)).unsafe()
    return self._make_item(id, item)
  
  @E.do[ReadError]()
  async def correct(self, id: str, pgn: Sequence[str], early: bool, annotations: Sequence[Annotations]):
    (await self._Qin.read(id)).unsafe()
    res = CorrectResult(annotations=annotations, pgn=pgn, early=early)
    await self._Qout.push(id, Result(res))
    await self._Qin.pop(id)
  
  @E.do[ReadError]()
  async def repreprocess(self, id: str):
    (await self._Qin.read(id)).unsafe()
    await self._Qout.push(id, Result(BadlyPreprocessed()))
    await self._Qin.pop(id)
  
  def annotate(self, id: str, annotations: Sequence[Annotations]):
    self._annotations[id] = annotations

  def manual_move(self, id: str, ply: int, uci: str):
    self._manual_ucis[id] |= { ply: uci }

  @E.do[ReadError]()
  async def predict(self, id: str, fen: str | None = None):
    task = (await self._Qin.read(id)).unsafe()
    anns = self._annotations.get(id)
    manual_ucis = self._manual_ucis[id]
    pred_anns = [a.for_preds() for a in anns] if anns is not None else None
    corr_preds = crop_corrects(task.ocrpreds, [no_na(ann.end_correct) for ann in anns or []])

    return gp.manual_predict(corr_preds, manual_ucis, pred_anns, fen=fen)