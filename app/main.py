import os
import logging
import logging.config

module_path = os.path.dirname(os.path.abspath(__file__))
logging_config_path = os.path.join(module_path, 'logging.ini')
logging.config.fileConfig(fname=logging_config_path)

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from app.config.dependencies import get_program_translator, get_instrument_service
from app.instrument_service.abstract_instrument_service import AbstractInstrumentService
from app.model import Program, ExecutionResponse
from app.translation.abstract_program_translator import AbstractProgramTranslator

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/program", response_model=ExecutionResponse)
async def get_program_result(program: Program,
                             program_translator: AbstractProgramTranslator = Depends(get_program_translator),
                             instrument_service: AbstractInstrumentService = Depends(get_instrument_service)):
    """
    Runs a given program using a program translator and an instrument service
    :param program:
    :param program_translator:
    :param instrument_service:
    :return: Result of computation
    """
    instructions = program_translator.translate(program)
    result = await instrument_service.execute(instructions)
    return ExecutionResponse(result=result)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Generic exception handler
    :param request:
    :param exc:
    :return:
    """
    logger.error(f"Exception occurred while processing request", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! Something went wrong..."},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7070)
