from typing import TypeVar, Literal, Any
from q.api import Queue
from q.kv import QueueKV
from ..types import Input, Preds

T = TypeVar('T')
State = TypeVar('State')

def input_queue(path: str, StateType: type[State] = tuple[()], protocol: Literal['fs', 'sqlite'] = 'sqlite') -> Queue[tuple[Input, State]]:
  return QueueKV.at(tuple[Input, StateType], path, protocol)

def output_queue(path: str, StateType: type[State] = tuple[()], protocol: Literal['fs', 'sqlite'] = 'sqlite') -> Queue[tuple[Preds, State]]:
  return QueueKV.at(tuple[Preds, StateType], path, protocol)
