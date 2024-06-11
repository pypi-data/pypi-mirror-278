import requests
from dotenv import load_dotenv

from camalis.exceptions import CamalisApiException

load_dotenv()


class BaseCamalisClient:
    token = None
    base_url = ''
    element_id = None

    def __init__(self, api_url, token, element_id):
        self.base_url = api_url
        self.token = token
        self.element_id = element_id

    def _check_status(self, response):
        if response.status_code in [200, 201]:
            return response.json()

        if response.status_code == 400:
            raise CamalisApiException(response.json()['detail'])

        if response.status_code == 401:
            raise CamalisApiException('Token is invalid')

        raise CamalisApiException(f'Error, status code: {response.status_code}')

    def request_post(self, url, json):
        response = requests.post(f'{self.base_url}{url}', json=json, headers={
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'X-Origem': 'integracao'
        })

        return self._check_status(response)

    def request_get(self, url):
        response = requests.get(f'{self.base_url}{url}', headers={
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'X-Origem': 'integracao'
        })
        return self._check_status(response)
