from typing import Literal
from pydantic import BaseModel
from moveread.annotations import ModelID, Rectangle

class Task(BaseModel):
  img: str
  model: ModelID

class Selected(BaseModel):
  tag: Literal['selected'] = 'selected'
  grid_coords: Rectangle

class Recorrect(BaseModel):
  tag: Literal['recorrect'] = 'recorrect'

Result = Selected | Recorrect