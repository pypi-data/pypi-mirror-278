from typing import Literal
from pydantic import BaseModel

class Task(BaseModel):
  contoured: str
  already_corrected: bool

Reannotation = Literal['incorrect', 'correct']
Annotation = Reannotation | Literal['perspective-correct']
