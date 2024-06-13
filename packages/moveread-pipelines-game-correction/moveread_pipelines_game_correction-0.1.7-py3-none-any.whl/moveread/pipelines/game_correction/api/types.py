from typing import Literal
from pydantic import BaseModel
from game_prediction2 import Pred

class Preds(BaseModel):
  reqId: str
  tag: Literal['preds'] = 'preds'
  preds: list[Pred]

class Done(BaseModel):
  reqId: str
  tag: Literal['done'] = 'done'

Message = Preds | Done

TYPESCRIPT = \
"""export type AutoPred = {
  tag: 'predicted'
  san: string
  prob: number
}

export type ManualPred = {
  tag: 'manual'
  san: string
}

export type Pred = AutoPred | ManualPred

export type Preds = {
  tag: 'preds'
  reqId: string
  preds: Pred[]
}

export type Done = {
  tag: 'done'
  reqId: string
}

export type Message = Preds | Done
"""