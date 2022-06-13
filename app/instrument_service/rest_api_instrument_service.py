from typing import Iterable

import aiohttp

from app.instrument_service.abstract_instrument_service import AbstractInstrumentService
from app.model import Instruction, Result


class RestApiInstrumentService(AbstractInstrumentService):
    """
    Enables executing instructions on instruments that expose REST API
    """
    def __init__(self, load_url: str, run_url: str):
        self.load_url = load_url
        self.run_url = run_url

    async def execute(self, instructions: Iterable[Instruction]) -> Result:
        """
        Makes an asynchronous REST API request to load a program consisted of provided instructions and then invokes
        run REST API asynchronously with the program name returned from the load request.
        :param instructions: A set of instructions to be executed on an instrument
        :return: Result of computation
        """
        async with aiohttp.ClientSession() as session:

            request = {
                "program_code": list(instructions)
            }

            async with session.post(self.load_url, json=request) as resp:
                load_response = await resp.json()
                program_id = load_response['program_id']

            async with session.get(f'{self.run_url}/{program_id}') as resp:
                run_response = await resp.json()
                result = run_response['result']

        return result

