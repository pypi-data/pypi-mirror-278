import requests
import pandas as pd


class ClientBuilder:
    def __init__(self, endpoint: str):
        if endpoint == "":
            raise ValueError("::: endpoint param is mandatory :::")
        else:
            self.endpoint = endpoint

    def _response_to_json(self):
        response = requests.get(self.endpoint)

        if response.ok:
            return response.json()
        else:
            raise ConnectionError(response.status_code)

    def to_dataframe(self):
        df = pd.DataFrame([self._response_to_json()])
        return df
