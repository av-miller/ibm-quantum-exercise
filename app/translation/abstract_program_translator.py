from abc import ABC, abstractmethod
from typing import Iterable

from app.model import Program, Instruction


class AbstractProgramTranslator(ABC):
    """
    A blueprint for a program translator to a set of instructions for a control instrument.
    """
    @abstractmethod
    def translate(self, program: Program) -> Iterable[Instruction]:
        """
        Should translate a program into a sequence of control instrument instructions.
        :param program: A program to translate
        :return: A sequence of instructions in control instrument language (pulses).
        """
        pass
