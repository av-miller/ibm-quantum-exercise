import json
import os

import pytest

from app.model import Program, Operation
from app.translation.acme_program_translator import AcmeProgramTranslator

module_path = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(module_path, 'data', 'large_quantum_program_input.json')

empty_program = Program(id="0",
                        control_instrument="Acme",
                        initial_value=0,
                        operations=[])

test_program = Program(id="1",
                       control_instrument="Acme",
                       initial_value=10,
                       operations=[Operation(type="Sum", value=4),
                                   Operation(type="Mul", value=9),
                                   Operation(type="Div", value=6),
                                   Operation(type="Div", value=4),
                                   Operation(type="Div", value=1),
                                   Operation(type="Div", value=10)])


@pytest.fixture
def acme_translator():
    return AcmeProgramTranslator()


def test_acme_translation_empty(acme_translator):
    """
    Ensure empty program translates
    """
    acme_pulses = acme_translator.translate(empty_program)
    assert list(acme_pulses) == ['Acme_initial_state_pulse', 0]


def test_acme_translation_sum_mul_div(acme_translator):
    """
    Ensure a program consisting of known operation types translates correctly
    """
    acme_pulses = acme_translator.translate(test_program)
    assert list(acme_pulses) == ['Acme_initial_state_pulse', 10,
                                 'Acme_pulse_1', 'Acme_pulse_2', 4,
                                 'Acme_pulse_2', 'Acme_pulse_1', 'Acme_pulse_1', 9,
                                 'Acme_pulse_2', 'Acme_pulse_2', 6,
                                 'Acme_pulse_2', 'Acme_pulse_2', 4,
                                 'Acme_pulse_2', 'Acme_pulse_2', 1,
                                 'Acme_pulse_2', 'Acme_pulse_2', 10]


def test_acme_translator_does_not_choke(acme_translator):
    """
    Stress test
    """
    with open(test_data_path) as f:
        test_data = json.load(f)

    for p in test_data:
        acme_translator.translate(p)
