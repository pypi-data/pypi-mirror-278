import unittest
from mono_pay import Client


class TestMonoPay(unittest.TestCase):
    def test_client_initialization(self):
        client = Client('token')
        self.assertIsNotNone(client.get_merchant_id())
        self.assertIsNotNone(client.get_merchant_name())


if __name__ == '__main__':
    unittest.main()
