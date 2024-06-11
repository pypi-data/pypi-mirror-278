from datetime import datetime

from camalis.core import BaseCamalisClient
from camalis.exceptions import CamalisException
from camalis.utils import datetime_to_iso_string, iso_string_to_datetime


class Variable:
    _id = None
    _camalis: BaseCamalisClient = None

    def __init__(self, client: BaseCamalisClient, id):
        self._id = id
        self._camalis = client

    def historic(self, start_time: datetime, end_time: datetime):
        start = datetime_to_iso_string(start_time)
        end = datetime_to_iso_string(end_time)
        response = self._camalis.request_get(
            f'/variaveis/historico/?variavelId={self._id}&dataInicio={start}&dataFim={end}')

        if not response['status']:
            return response['detail']
        result = []
        for data in response['data']:
            result.append({
                'timestamp': iso_string_to_datetime(data['t']),
                'value': data['v'],
                'unit': data['u']
            })
        return result

    def statistics(self, start_time: datetime, end_time: datetime, interval_in_seconds=3600):
        response = self._camalis.request_post('/variaveis/historico/', {
            "dataInicio": datetime_to_iso_string(start_time),
            "dataFim": datetime_to_iso_string(end_time),
            "variavelId": self._id,
            "intervaloEmSegundos": interval_in_seconds
        })
        return response['statistics']

    def __str__(self):
        return f"Variable {self._id}"

    @property
    def id(self):
        return self._id

    def snapshot(self):
        response = self._camalis.request_get(f'/variaveis/snapshot/?variavelId={self._id}')
        if not response['status']:
            raise CamalisException(response['detail'])

        result = []
        for data in response['data']:
            result.append({
                'timestamp': iso_string_to_datetime(data['t']),
                'value': data['v'],
                'unit': data['u']
            })
        return result

    def write(self, value, created_at: datetime = None):
        start = datetime_to_iso_string(created_at)
        response = self._camalis.request_post('/variaveis/escrever/', {
            "variavelId": self._id,
            "timestamp": start,
            "valor": value
        })
        if not response['status']:
            raise CamalisException(response['detail'])
        return True
