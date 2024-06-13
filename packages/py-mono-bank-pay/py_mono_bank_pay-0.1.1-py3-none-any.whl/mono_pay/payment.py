from typing import Optional, Dict, Any

from .client import Client


class Payment:

    def __init__(self, client: Client):
        self.client = client

    def create(self, amount: int, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if amount < 1:
            raise Exception('Amount must be a natural number')
        if options is None:
            options = {}
        options['amount'] = amount

        response = self.client.get_client().post(f'{self.client.api_endpoint}/api/merchant/invoice/create', json=options)
        return self.client.get_data_from_response(response)

    def info(self, invoice_id: str) -> Dict[str, Any]:
        response = self.client.get_client().get(f'{self.client.api_endpoint}/api/merchant/invoice/status', params={'invoiceId': invoice_id})
        return self.client.get_data_from_response(response)

    def refund(self, invoice_id: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if options is None:
            options = {}
        options['invoiceId'] = invoice_id

        response = self.client.get_client().post(f'{self.client.api_endpoint}/api/merchant/invoice/cancel', json=options)
        return self.client.get_data_from_response(response)

    def cancel(self, invoice_id: str) -> Dict[str, Any]:
        response = self.client.get_client().post(f'{self.client.api_endpoint}/api/merchant/invoice/remove', json={'invoiceId': invoice_id})
        return self.client.get_data_from_response(response)

    def success_details(self, invoice_id: str) -> Dict[str, Any]:
        response = self.client.get_client().get(f'{self.client.api_endpoint}/api/merchant/invoice/payment-info', params={'invoiceId': invoice_id})
        return self.client.get_data_from_response(response)

    def capture_hold(self, invoice_id: str, amount: Optional[int] = None) -> Dict[str, Any]:
        body = {'invoiceId': invoice_id}
        if amount is not None:
            body['amount'] = amount

        response = self.client.get_client().post(f'{self.client.api_endpoint}/api/merchant/invoice/finalize', json=body)
        return self.client.get_data_from_response(response)

    def items(self, from_timestamp: int, to_timestamp: Optional[int] = None) -> Dict[str, Any]:
        params = {'from': from_timestamp}
        if to_timestamp is not None:
            params['to'] = to_timestamp

        response = self.client.get_client().get(f'{self.client.api_endpoint}/api/merchant/statement', params=params)
        data = self.client.get_data_from_response(response)
        return data.get('list', [])

    def create_with_card_token(self, card_token: str, amount: int, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if amount < 1:
            raise Exception('Amount must be a natural number')
        if options is None:
            options = {}
        options['amount'] = amount
        options['cardToken'] = card_token

        response = self.client.get_client().post(f'{self.client.api_endpoint}/api/merchant/wallet/payment', json=options)
        return self.client.get_data_from_response(response)

    def list_card_tokens(self, wallet_id: str) -> Dict[str, Any]:
        response = self.client.get_client().get(f'{self.client.api_endpoint}/api/merchant/wallet', params={'walletId': wallet_id})
        data = self.client.get_data_from_response(response)
        return data.get('wallet', [])

    def delete_card_token(self, card_token: str) -> None:
        response = self.client.get_client().delete(f'{self.client.api_endpoint}/api/merchant/wallet/card', params={'cardToken': card_token})
        self.client.get_data_from_response(response)