from abc import ABC, abstractmethod
from typing import Iterable

from app.model import Instruction, Result


class AbstractInstrumentService(ABC):
    """
    This is a blueprint for talking to control instrument services
    """
    @abstractmethod
    async def execute(self, instructions: Iterable[Instruction]) -> Result:
        """
        Should execute a sequence of instructions and provide result back.
        :param instructions: Instructions to be run on an instrument
        :return: Result of the computation
        """
        pass
