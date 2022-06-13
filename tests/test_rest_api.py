import pytest
from fastapi.testclient import TestClient

from app.main import app

test_request_template = {
    "id": "abcdefghijkl",
    "initial_value": 10,
    "operations": [
        {
            "type": "Sum",
            "value": 120
        },
        {
            "type": "Mul",
            "value": 3
        },
        {
            "type": "Div",
            "value": 2
        }
    ]
}

client = TestClient(app)

# NOTE: I could probably parameterize below two tests as they are very similar, but I chose not to because
# implementations for two different things usually tend to diverge over time, and we may need to have more differences
# in test resulting in having to change parameterized test back into two tests. In other words, I anticipate that
# parameterized test case will become tech debt.


@pytest.mark.asyncio
def test_get_program_result_madrid(aioresponses):
    """
    Ensure that result from Madrid control instrument gets returned to the user
    :param aioresponses: AIOHTTP mock allowing me to stub out responses
    :return:
    """
    aioresponses.post('https://madrid.com/program/load', status=200, payload={'program_id': 'MadridProgramId1'})
    aioresponses.get('https://madrid.com/program/run/MadridProgramId1', status=200, payload={'result': 195})

    test_request_template['control_instrument'] = 'MADRID'
    response = client.post('/program', json=test_request_template)

    assert response.json()['result'] == 195


@pytest.mark.asyncio
def test_get_program_result_acme(aioresponses):
    """
    Ensure that result from Acme control instrument gets returned to the user
    :param aioresponses: AIOHTTP mock allowing me to stub out responses
    :return:
    """
    aioresponses.post('https://acme.com/load_program', status=200, payload={'program_id': 'AcmeProgramId1'})
    aioresponses.get('https://acme.com/run_program/AcmeProgramId1', status=200, payload={'result': 195})

    test_request_template['control_instrument'] = 'ACME'
    response = client.post('/program', json=test_request_template)

    assert response.json()['result'] == 195


@pytest.mark.asyncio
def test_get_program_result_blah(aioresponses):
    with pytest.raises(Exception):
        aioresponses.post('https://blah.com/load_program', status=200, payload={'program_id': 'blahProgramId1'})
        aioresponses.get('https://blah.com/run_program/blahProgramId1', status=200, payload={'result': 195})

        test_request_template['control_instrument'] = 'blah'
        client.post('/program', json=test_request_template)
