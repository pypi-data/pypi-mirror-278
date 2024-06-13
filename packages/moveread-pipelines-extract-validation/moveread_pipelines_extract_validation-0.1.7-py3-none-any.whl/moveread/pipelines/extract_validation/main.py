from typing import NamedTuple, Literal, TypeVar, Generic
from dataclasses import dataclass
from haskellian import Either, Left, Right, either as E
from q.api import ReadQueue, WriteQueue, ReadError
from .types import Task, Annotation, Reannotation

State = TypeVar('State')

def make_item(entry: tuple[str, tuple[Task, State]]) -> tuple[str, Task]:
  id, (task, *_) = entry
  return id, task

Ann = TypeVar('Ann', Annotation, Reannotation)

class Queues(NamedTuple, Generic[State, Ann]):
  inp: ReadQueue[tuple[Task, State]]
  out: WriteQueue[tuple[Ann, State]]

# AnnotateResponse = Literal['OK', 'NOT_FOUND', 'BAD_ANNOTATION', 'SERVER_ERROR']
@dataclass
class BadAnnotation:
  detail: str | None = None
  reason: Literal['bad-anotation'] = 'bad-anotation'

ValidationErr = BadAnnotation | ReadError

@dataclass
class ValidationAPI(Generic[State, Ann]):

  Qin: ReadQueue[tuple[Task, State]]
  Qout: WriteQueue[tuple[Ann, State]]

  @classmethod
  def of(cls, queues: Queues[State, Ann]) -> 'ValidationAPI[State, Ann]':
    return cls(queues.inp, queues.out)

  def items(self):
    return self.Qin.items().map(lambda e: e.fmap(make_item))
  
  @E.do[ValidationErr]()
  async def annotate(self, id: str, annotation: Annotation):
    task, state = (await self.Qin.read(id)).unsafe()
    if task.already_corrected and annotation == 'perspective-correct':
      Left(BadAnnotation(f'Task is already corrected, but annotation is "perspective-correct"')).unsafe()

    (await self.Qout.push(id, (annotation, state))).unsafe() # type: ignore
    (await self.Qin.pop(id)).unsafe()