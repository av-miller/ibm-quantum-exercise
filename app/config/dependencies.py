from fastapi import Depends

from app.config.settings import Settings
from app.constants import acme_instrument_name, madrid_instrument_name
from app.instrument_service.abstract_instrument_service import AbstractInstrumentService
from app.instrument_service.rest_api_instrument_service import RestApiInstrumentService
from app.model import Program
from app.translation.abstract_program_translator import AbstractProgramTranslator
from app.translation.acme_program_translator import AcmeProgramTranslator
from app.translation.madrid_program_translator import MadridProgramTranslator


class UnsupportedInstrumentException(Exception):
    pass


def get_settings():
    return Settings()


def get_program_translator(program: Program) -> AbstractProgramTranslator:
    if program.control_instrument.lower() == acme_instrument_name:
        return AcmeProgramTranslator()
    elif program.control_instrument.lower() == madrid_instrument_name:
        return MadridProgramTranslator()
    else:
        raise UnsupportedInstrumentException(f"Instrument '{program.control_instrument}' is not supported")


def get_instrument_service(program: Program,
                           settings: Settings = Depends(get_settings)) -> AbstractInstrumentService:
    if program.control_instrument.lower() == acme_instrument_name:
        return RestApiInstrumentService(load_url=settings.acme_load_url,
                                        run_url=settings.acme_run_url)
    elif program.control_instrument.lower() == madrid_instrument_name:
        return RestApiInstrumentService(load_url=settings.madrid_load_url,
                                        run_url=settings.madrid_run_url)
    else:
        raise UnsupportedInstrumentException(f"Instrument '{program.control_instrument}' is not supported")
