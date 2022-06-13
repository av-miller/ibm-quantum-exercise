import json
import os

import pytest

from app.model import Program, Operation
from app.translation.madrid_program_translator import MadridProgramTranslator

module_path = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(module_path, 'data', 'large_quantum_program_input.json')

empty_program = Program(id="0",
                        control_instrument="Madrid",
                        initial_value=-1,
                        operations=[])

test_program = Program(id="1",
                       control_instrument="Acme",
                       initial_value=0,
                       operations=[Operation(type="Div", value=96),
                                   Operation(type="Mul", value=74),
                                   Operation(type="Sum", value=345),
                                   Operation(type="Sum", value=3)])


@pytest.fixture
def madrid_translator():
    return MadridProgramTranslator()


def test_madrid_translation_empty(madrid_translator):
    """
    Ensure empty program translates
    """
    acme_pulses = madrid_translator.translate(empty_program)
    assert list(acme_pulses) == [-1, 'Madrid_initial_state_pulse']


def test_madrid_translation_sum_mul_div(madrid_translator):
    """
    Ensure a program consisting of known operation types translates correctly
    """
    acme_pulses = madrid_translator.translate(test_program)
    assert list(acme_pulses) == [0, 'Madrid_initial_state_pulse',
                                 96, 'Madrid_pulse_2', 'Madrid_pulse_1',
                                 74, 'Madrid_pulse_2', 'Madrid_pulse_2',
                                 345, 'Madrid_pulse_1',
                                 3, 'Madrid_pulse_1']


def test_madrid_translator_does_not_choke(madrid_translator):
    """
    Stress test
    """
    with open(test_data_path) as f:
        test_data = json.load(f)

    for p in test_data:
        madrid_translator.translate(p)
