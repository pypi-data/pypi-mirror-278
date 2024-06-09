from typing import Optional, Dict, Any

import requests


class Client:
    api_endpoint = 'https://api.monobank.ua/'

    def __init__(self, token: str, custom_headers: Optional[Dict[str, str]] = None):
        headers = {
            'X-Token': token
        }
        if custom_headers:
            headers.update(custom_headers)

        self.http_client = requests.Session()
        self.http_client.headers.update(headers)
        self.http_client.timeout = 5

        response = self.http_client.get(f'{self.api_endpoint}/api/merchant/details')
        data = self.get_data_from_response(response)

        if 'merchantId' in data and 'merchantName' in data:
            self.merchant_id = data['merchantId']
            self.merchant_name = data['merchantName']
        else:
            raise Exception('Cannot decode JSON response from Mono')

    def get_merchant_id(self) -> str:
        return self.merchant_id

    def get_merchant_name(self) -> str:
        return self.merchant_name

    def get_client(self) -> requests.Session:
        return self.http_client

    def get_public_key(self) -> str:
        response = self.get_client().get(f'{self.api_endpoint}/api/merchant/pubkey')
        data = self.get_data_from_response(response)
        if 'key' not in data:
            raise Exception('Invalid response from Mono API')
        return data['key']

    def get_merchant(self) -> Dict[str, Any]:
        response = self.get_client().get(f'{self.api_endpoint}/api/merchant/details')
        return self.get_data_from_response(response)

    def get_data_from_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code == 200:
            return response.json()
        else:
            data = response.json()
            if 'errorDescription' in data:
                raise Exception(data['errorDescription'], response.status_code)
            else:
                raise Exception(f'Unknown error response: {response.text}', response.status_code)