from typing import Iterable

from app.translation.abstract_program_translator import AbstractProgramTranslator
from app.model import Program, Instruction, ArithmeticOperation
from app.translation.generic_pulse_generator import generate_program_pulses

initial_pulse = 'Madrid_initial_state_pulse'
pulse_1 = 'Madrid_pulse_1'
pulse_2 = 'Madrid_pulse_2'


def generate_initial_pulse(value: int) -> Iterable[Instruction]:
    yield from [value, initial_pulse]


def generate_sum_pulse(value: int) -> Iterable[Instruction]:
    yield from [value, pulse_1]


def generate_mul_pulse(value: int) -> Iterable[Instruction]:
    yield from [value, pulse_2, pulse_2]


def generate_div_pulse(value: int) -> Iterable[Instruction]:
    yield from [value, pulse_2, pulse_1]


op_pulse_mapping = {
    ArithmeticOperation.SUMMATION: generate_sum_pulse,
    ArithmeticOperation.MULTIPLICATION: generate_mul_pulse,
    ArithmeticOperation.DIVISION: generate_div_pulse
}


class MadridProgramTranslator(AbstractProgramTranslator):
    """
    Translates programs to Madrid pulse language.
    """
    def translate(self, program: Program) -> Iterable[Instruction]:
        yield from generate_program_pulses(program, generate_initial_pulse, op_pulse_mapping)


