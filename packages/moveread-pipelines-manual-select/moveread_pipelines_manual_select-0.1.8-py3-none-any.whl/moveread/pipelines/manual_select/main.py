from typing import Generic, TypeVar, NamedTuple
from dataclasses import dataclass
from haskellian import either as E
from q.api import ReadQueue, WriteQueue, ReadError
from .types import Task, Result, Selected, Recorrect, Rectangle

State = TypeVar('State')

def make_item(entry: tuple[str, tuple[Task, State]]) -> tuple[str, Task]:
  id, (task, *_) = entry
  return id, task

class Queues(NamedTuple, Generic[State]):
  inp: ReadQueue[tuple[Task, State]]
  out: WriteQueue[tuple[Result, State]]
  """Images to recorrect before selecting (i.e. too distorted)"""

@dataclass
class SelectAPI(Generic[State]):
  """API to manage manual correction of images, with state forwarding
  - Supports sending images to 'recorrect'. I.e. declaring them as too distorted for the grid to be accurately selected
  """

  Qin: ReadQueue[tuple[Task, State]]
  Qout: WriteQueue[tuple[Result, State]]

  @classmethod
  def of(cls, queues: Queues[State]) -> 'SelectAPI[State]':
    return cls(queues.inp, queues.out)

  def items(self):
    return self.Qin.items().map(lambda e: e.fmap(make_item))
  
  @E.do[ReadError]()
  async def select(self, id: str, grid_coords: Rectangle):
    _, state = (await self.Qin.read(id)).unsafe()
    (await self.Qout.push(id, (Selected(grid_coords=grid_coords), state))).unsafe()
    (await self.Qin.pop(id)).unsafe()

  @E.do[ReadError]()
  async def recorrect(self, id: str):
    _, state = (await self.Qin.read(id)).unsafe()
    (await self.Qout.push(id, (Recorrect(), state))).unsafe()
    (await self.Qin.pop(id)).unsafe()