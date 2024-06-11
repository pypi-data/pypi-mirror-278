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

    def get(self, name=None, path=None) -> Variable:
        if path is None and name is None:
            raise CamalisApiException('Name or path is required')

        if path and name:
            raise CamalisApiException('Only one parameter is allowed')

        response = None

        url = '/variaveis/'
        if name:
            if self._camalis.element_id is None:
                raise CamalisApiException('ElementId is required')

            url = f'{url}buscarPorNome/?nome={name}&elementoId={self._camalis.element_id}'
            response = self._camalis.request_get(url=url)

        if path:
            url = f'{url}buscarPorPath/?path={path}'
            response = self._camalis.request_get(url=url)

        if len(response['ids']) == 0:
            raise CamalisApiException('Variable not found')

        if len(response['ids']) > 1:
            raise CamalisApiException('Multiple variables found')

        return Variable(self._camalis, id=response['ids'][0])

    def list(self, path=None) -> list[Variable]:
        if path is None and self._camalis.element_id is None:
            raise CamalisApiException('Path or element_id is required')

        url = f'/variaveis/buscarPorPath/?path={path}' \
            if path else f'/variaveis/buscarPorNome/?nome=&elementoId={self._camalis.element_id}'
        response = self._camalis.request_get(url=url)
        if len(response['ids']) == 0:
            return []

        result = []
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
