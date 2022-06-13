from dataclasses import dataclass
from enum import Enum
from typing import NewType, Union, List

from pydantic import BaseModel


@dataclass
class Operation:
    type: str
    value: int


class Program(BaseModel):
    id: str
    control_instrument: str
    initial_value: int
    operations: List[Operation]


Instruction = NewType("Instruction", Union[str, int])

Result = NewType("Result", int)


class ExecutionResponse(BaseModel):
    result: Result


class ArithmeticOperation(Enum):
    SUMMATION = 'Sum'
    MULTIPLICATION = 'Mul'
    DIVISION = 'Div'
