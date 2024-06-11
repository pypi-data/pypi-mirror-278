from camalis.core import BaseCamalisClient


class Event:
    _camalis: BaseCamalisClient = None

    def __init__(self, client: BaseCamalisClient):
        self._camalis = client
