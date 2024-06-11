import os

from camalis.core import BaseCamalisClient
from camalis.event import Event
from camalis.exceptions import CamalisAuthException, CamalisApiException
from camalis.state import State
from camalis.variable import Variable


class CamalisVariableClient:
    _camalis: BaseCamalisClient = None

    def __init__(self, client: BaseCamalisClient):
        self._camalis = client

    def _build_request(self, path=None, name=None):
        if path:
            return self._camalis.request_get(f'/variaveis/buscarPorPath/?path={path}')

        if self._camalis.element_id:
            raise CamalisApiException('Element ID is required')

        return self._camalis.request_get(
            f'/variaveis/buscarPorNome/?nome={name}&elementoId={self._camalis.element_id}')

    def get(self, name=None, path=None) -> Variable:
        response = self._build_request(path=path, name=name)
        if len(response['ids']) == 0:
            raise CamalisApiException('Variable not found')

        if len(response['ids']) > 1:
            raise CamalisApiException('Multiple variables found')

        return Variable(self._camalis, id=response['ids'][0])

    def list(self, path=None) -> list[Variable]:
        result = []
        response = self._build_request(path=path)
        if len(response['ids']) == 0:
            raise CamalisApiException('Variable not found')

        for variable_id in response['ids']:
            result.append(Variable(self._camalis, id=variable_id))
        return result


class Camalis(BaseCamalisClient):
    variable: CamalisVariableClient = None

    def __init__(self, api_url=None, token=None, element_id=None):
        request_token = os.environ.get('CAMALIS_TOKEN', token)
        camalis_url = os.environ.get('CAMALIS_API_URL', api_url)
        camalis_element_id = os.environ.get('CAMALIS_ELEMENTO_ID', element_id)

        if request_token is None:
            raise CamalisAuthException('Token is required')

        if camalis_url is None:
            raise CamalisAuthException('API URL is required')

        super().__init__(camalis_url, request_token, camalis_element_id)
        self.variable = CamalisVariableClient(self)

    def state(self) -> State:
        return State(self)

    def event(self) -> Event:
        return Event(self)
