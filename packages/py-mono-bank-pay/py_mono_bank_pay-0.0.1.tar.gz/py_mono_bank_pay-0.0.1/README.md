# py_mono_bank_pay

A client library for Monobank merchant API.

## Installation

Install the package using pip:

```sh
pip install py_mono_bank_pay
```

## Usage

from py_mono_bank_pay import Client, Payment, Webhook

###### Initialize Client

client = Client('your_token')

###### Use the Client

merchant_id = client.get_merchant_id()

merchant_name = client.get_merchant_name()

print(f'Merchant ID: {merchant_id}, Merchant Name: {merchant_name}')

###### Initialize Payment

payment = Payment(client)

invoice = payment.create(1000)

print(invoice)

###### Initialize Webhook

webhook = Webhook(client)

is_verified = webhook.verify()

print(is_verified)


##License
This project is licensed under the MIT License - see the LICENSE file for details.