from app.model import ArithmeticOperation


class UnsupportedOperationException(Exception):
    pass


def generate_program_pulses(program, initial_pulse_generator, operation_pulse_generator_map):
    yield from initial_pulse_generator(program.initial_value)

    for op in program.operations:
        operation_type = ArithmeticOperation(op.type)
        operation_generator = operation_pulse_generator_map.get(operation_type)
        if not operation_generator:
            raise UnsupportedOperationException(f"Operation '{op.type}' is supported")
        yield from operation_generator(op.value)
