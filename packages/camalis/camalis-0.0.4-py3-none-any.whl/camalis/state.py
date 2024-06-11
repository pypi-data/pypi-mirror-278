import json
import os
from types import SimpleNamespace

from camalis.core import BaseCamalisClient


class State:
    _camalis: BaseCamalisClient = None
    _execution_id: str = None

    def __init__(self, client: BaseCamalisClient):
        self._camalis = client
        execution_id = os.environ.get('CAMALIS_EXECUCAO_ID', None)
        if execution_id is None:
            raise Exception('Execution ID is required')

        self._execution_id = execution_id

    def load(self):
        response = self._camalis.request_get(f'/estado/{self._execution_id}')
        return SimpleNamespace(**json.loads(response))

    def save(self, state):
        self._camalis.request_post('/estado/', {
            'execucaoId': self._execution_id,
            "estado": state
        })
