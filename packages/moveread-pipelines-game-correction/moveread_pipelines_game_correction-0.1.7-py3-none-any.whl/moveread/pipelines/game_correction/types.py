from typing import Literal, Self, Sequence
import os
from pydantic import BaseModel, RootModel, Field
from pipeteer import Pipeline
from game_prediction2 import Annotations as PredAnnotations
from chess_notation.language import Language
from chess_notation.styles import PawnCapture, PieceCapture

NA = Literal['N/A']
def no_na(value):
  if value != 'N/A':
    return value

class Annotations(BaseModel):
  lang: Language | NA | None = None
  pawn_capture: PawnCapture | NA | None = None
  piece_capture: PieceCapture | NA | None = None
  end_correct: int | None = None

  def for_preds(self) -> 'PredAnnotations':
    """Convert to `game_correction.Annotations` (replaces `'N/A'`s with `None`s)"""
    return PredAnnotations(
      lang=no_na(self.lang),
      pawn_capture=no_na(self.pawn_capture),
      piece_capture=no_na(self.piece_capture),
    )
  
class Meta(BaseModel):
  title: str | None = None
  details: str | None = None

class BaseInput(Meta):
  ply_boxes: Sequence[Sequence[str]]
  annotations: Sequence[Annotations] | None = None

  def at_url(self, images_path: str) -> 'Self':
    copy = self.model_copy()
    copy.ply_boxes = [
      [os.path.join(images_path, box) for box in boxes]
      for boxes in self.ply_boxes
    ]
    return copy

class Input(BaseInput):
  ocrpreds: Sequence[Sequence[Sequence[tuple[str, float]]]]
  """BATCH x PLAYERS x TOP_PREDS x (word, logprob)"""

class CorrectResult(BaseModel):
  tag: Literal['correct'] = 'correct'
  annotations: Sequence[Annotations]
  pgn: Sequence[str]
  early: bool

class BadlyPreprocessed(BaseModel):
  tag: Literal['badly-preprocessed'] = 'badly-preprocessed'

class Result(RootModel):
  root: CorrectResult | BadlyPreprocessed = Field(discriminator='tag')

class MetaItem(Meta):
  id: str

class Item(BaseInput):
  id: str
  pgn: Sequence[str] | None = None
  manual_ucis: dict[int, str] | None = None

pipeline = Pipeline(Input, Result)