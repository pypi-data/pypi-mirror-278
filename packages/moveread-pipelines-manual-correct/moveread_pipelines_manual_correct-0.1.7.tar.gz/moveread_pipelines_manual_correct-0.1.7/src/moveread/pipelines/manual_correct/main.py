from ast import Is
from typing import TypeVar, Generic, NamedTuple
from dataclasses import dataclass
from haskellian import either as E
from q.api import ReadQueue, WriteQueue, ReadError
from .types import Task, Corrected, Rotated, Result, Corners, Rotation

State = TypeVar('State')

def make_item(entry: tuple[str, tuple[Task, State]]) -> tuple[str, Task]:
  id, (task, *_) = entry
  return id, task

class Queues(NamedTuple, Generic[State]):
  inp: ReadQueue[tuple[Task, State]]
  out: WriteQueue[tuple[Result, State]]

@dataclass
class CorrectionAPI(Generic[State]):
  """API to manage manual correction of images, with state forwarding"""

  Qin: ReadQueue[tuple[Task, State]]
  Qout: WriteQueue[tuple[Result, State]]

  @classmethod
  def of(cls, queues: Queues[State]) -> 'CorrectionAPI[State]':
    return cls(queues.inp, queues.out)

  def items(self):
    return self.Qin.items().map(lambda e: e.fmap(make_item))
  
  @E.do[ReadError]()
  async def correct(self, id: str, corners: Corners):
    _, state = (await self.Qin.read(id)).unsafe()
    (await self.Qout.push(id, (Corrected(corners=corners), state))).unsafe()
    (await self.Qin.pop(id)).unsafe()
  
  @E.do[ReadError]()
  async def rotate(self, id: str, rotation: Rotation):
    _, state = (await self.Qin.read(id)).unsafe()
    (await self.Qout.push(id, (Rotated(rotation=rotation), state))).unsafe()
    (await self.Qin.pop(id)).unsafe()
